#!/usr/bin/env python3
"""Reference exporter for .design files (design.v1).

Emits the artifacts declared under `exports`:
  css             CSS custom properties (:root + theme modes per mode_strategy)
  tailwind        Tailwind v4 @theme file (namespaced variables)
  dtcg            W3C Design Tokens (DTCG) JSON for cleanly-mappable groups
  shadcn_registry shadcn registry item (registry:theme) from integrations.shadcn
  frame_md        HyperFrames frame.md (DESIGN.md-shaped video-frame companion + motion/sound)

Usage:
  python scripts/export_design.py <file.design> [--out-dir DIR] [--only css,dtcg,...]

Paths come from the file's `exports` section (resolved relative to the .design
file); --out-dir redirects everything into one directory (basenames kept).
The .design file stays normative — these outputs are generated artifacts.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

import yaml

REF_RE = re.compile(r"\{tokens\.([A-Za-z0-9_.\-]+)\}")
CAMEL_RE = re.compile(r"(?<=[a-z0-9])([A-Z])")

# groups whose bare-number leaves mean pixels in CSS
PX_GROUPS = {"spacing", "radius", "breakpoint"}
# groups skipped by the Tailwind exporter (no @theme namespace)
TW_NAMESPACE = {
    "color": "color",
    "spacing": "spacing",
    "radius": "radius",
    "breakpoint": "breakpoint",
    "elevation": "shadow",
}


def kebab(name: str) -> str:
    return CAMEL_RE.sub(r"-\1", str(name)).lower().replace(".", "-").replace("_", "-")


def css_value(group: str, value, prefix: str) -> str:
    if isinstance(value, (int, float)) and group in PX_GROUPS:
        value = f"{value}px"
    text = str(value)
    return REF_RE.sub(lambda m: f"var(--{prefix}{kebab(m.group(1))})", text)


def flatten(node, path=()):
    """Yield (path_tuple, leaf) for every scalar/list leaf in a token tree."""
    if isinstance(node, dict):
        for key, val in node.items():
            yield from flatten(val, path + (str(key),))
    else:
        yield path, node


def flatten_tokens(tokens: dict, prefix: str) -> dict[str, str]:
    """Token tree -> ordered {--var-name: css-value}."""
    out: dict[str, str] = {}
    for group, tree in (tokens or {}).items():
        if not isinstance(tree, dict):
            continue
        for path, leaf in flatten(tree, (group,)):
            if isinstance(leaf, list):  # font stacks
                leaf = ", ".join(str(x) for x in leaf)
            if isinstance(leaf, (int, float)) and path[-1] == "fontSize":
                leaf = f"{leaf}px"  # weight/line-height stay unitless
            name = "--" + prefix + "-".join(kebab(p) for p in path)
            out[name] = css_value(path[0], leaf, prefix)
    return out


def mode_overrides(doc: dict, prefix: str) -> dict[str, dict[str, str]]:
    modes = ((doc.get("themes") or {}).get("modes")) or {}
    return {
        mode: flatten_tokens((spec or {}).get("tokens") or {}, prefix)
        for mode, spec in modes.items()
    }


def export_css(doc: dict, cfg: dict) -> str:
    prefix = cfg.get("prefix") or ""
    strategy = cfg.get("mode_strategy", "data-attribute")
    attribute = cfg.get("attribute", "data-theme")
    selector = cfg.get("selector", ":root")

    base = flatten_tokens(doc.get("tokens") or {}, prefix)
    overrides = mode_overrides(doc, prefix)
    default_mode = (doc.get("themes") or {}).get("default")
    if default_mode in overrides:
        base.update(overrides.pop(default_mode))

    def block(sel: str, variables: dict[str, str], indent: str = "") -> str:
        lines = [f"{indent}{sel} {{"]
        lines += [f"{indent}  {k}: {v};" for k, v in variables.items()]
        lines.append(f"{indent}}}")
        return "\n".join(lines)

    parts = [f"/* generated from {doc.get('name', '.design')} v{doc.get('version', '?')} — do not edit; the .design file is normative */"]
    parts.append(block(selector, base))
    for mode, variables in overrides.items():
        if not variables:
            continue
        if strategy in ("media-query", "both") and mode == "dark":
            parts.append(f"@media (prefers-color-scheme: dark) {{\n{block(selector, variables, '  ')}\n}}")
        if strategy in ("data-attribute", "both"):
            parts.append(block(f'{selector}[{attribute}="{mode}"]', variables))
    if strategy == "both" and overrides:
        # explicit light toggle must beat the OS media query
        reasserted = {k: base[k] for vars_ in overrides.values() for k in vars_ if k in base}
        if reasserted:
            parts.append(block(f'{selector}[{attribute}="light"]', reasserted))
    return "\n\n".join(parts) + "\n"


def export_tailwind(doc: dict, cfg: dict) -> str:
    prefix = ""
    lines = ["/* generated Tailwind v4 theme — import into your CSS after tailwindcss */", "@theme {"]
    tokens = doc.get("tokens") or {}
    for group, namespace in TW_NAMESPACE.items():
        tree = tokens.get(group)
        if not isinstance(tree, dict):
            continue
        for path, leaf in flatten(tree, ()):
            if isinstance(leaf, list):
                leaf = ", ".join(str(x) for x in leaf)
            name = "--" + namespace + "-" + "-".join(kebab(p) for p in path)
            lines.append(f"  {name}: {css_value(group, leaf, prefix)};")
    for role, spec in (tokens.get("typography") or {}).items():
        if isinstance(spec, dict) and spec.get("fontFamily"):
            fam = spec["fontFamily"]
            if isinstance(fam, list):
                fam = ", ".join(str(x) for x in fam)
            lines.append(f"  --font-{kebab(role)}: {fam};")
    for name, spec in ((tokens.get("motion") or {}).get("easing") or {}).items():
        lines.append(f"  --ease-{kebab(name)}: {spec};")
    lines.append("}")
    return "\n".join(lines) + "\n"


DTCG_TYPES = {"color": "color", "spacing": "dimension", "radius": "dimension",
              "breakpoint": "dimension", "opacity": "number", "zIndex": "number"}


def export_dtcg(doc: dict, cfg: dict) -> dict:
    tokens = doc.get("tokens") or {}
    out: dict = {}

    def leaf_token(group: str, leaf):
        if isinstance(leaf, str) and REF_RE.fullmatch(leaf.strip()):
            return {"$value": "{" + leaf.strip()[8:-1] + "}"}  # {tokens.x.y} -> {x.y}
        dtype = DTCG_TYPES[group]
        value = leaf
        if dtype == "dimension" and isinstance(leaf, (int, float)):
            value = f"{leaf}px"
        return {"$type": dtype, "$value": value}

    for group, dtype in DTCG_TYPES.items():
        tree = tokens.get(group)
        if not isinstance(tree, dict):
            continue
        target = out.setdefault(group, {})
        for path, leaf in flatten(tree, ()):
            node = target
            for part in path[:-1]:
                node = node.setdefault(part, {})
            node[path[-1]] = leaf_token(group, leaf)
    typography = tokens.get("typography")
    if isinstance(typography, dict):
        target = out.setdefault("typography", {})
        for role, spec in typography.items():
            if isinstance(spec, dict):
                value = dict(spec)
                if isinstance(value.get("fontFamily"), str):
                    value["fontFamily"] = [value["fontFamily"]]
                if isinstance(value.get("fontSize"), (int, float)):
                    value["fontSize"] = f"{value['fontSize']}px"
                target[role] = {"$type": "typography", "$value": value}
    return out


FRAME_REF_RE = re.compile(r"\{tokens\.(color|typography|spacing|radius|motion|sound)\.")
FRAME_GROUPS = {"color": "colors", "typography": "typography", "spacing": "spacing",
                "radius": "radii", "motion": "motion", "sound": "sound"}


def export_frame_md(doc: dict, cfg: dict) -> str:
    """HyperFrames frame.md: DESIGN.md-shaped frontmatter + body (SPEC §7.4).

    Colors, typography, spacing, radii carry over verbatim; motion and sound ride
    along as extra frontmatter groups. Composition is left to the frame author.
    """
    tokens = doc.get("tokens") or {}
    name = doc.get("name", "brand")
    aspect = cfg.get("aspect", "16:9")

    def rewrite(value):
        # {tokens.color.x} -> {colors.x}; nested groups keep their dot path
        if isinstance(value, str):
            return FRAME_REF_RE.sub(lambda m: "{" + FRAME_GROUPS[m.group(1)] + ".", value)
        if isinstance(value, dict):
            return {k: rewrite(v) for k, v in value.items()}
        if isinstance(value, list):
            return [rewrite(v) for v in value]
        return value

    front: dict = {
        "version": "alpha",
        "name": f"{name} — Frame (video / frame layer)",
        "description": f"Video-first companion to {name}'s .design v{doc.get('version', '?')}. "
                       f"Generated — the .design file is normative; composition is the frame author's.",
        "unit": f"the frame — {aspect} primary",
    }
    for group, key in FRAME_GROUPS.items():
        tree = tokens.get(group)
        if isinstance(tree, dict) and tree:
            front[key] = rewrite(tree)
    bags: dict = {}
    for cid, comp in (doc.get("components") or {}).items():
        if not isinstance(comp, dict):
            continue
        if isinstance(comp.get("tokens"), dict):
            for vid, bag in comp["tokens"].items():
                if isinstance(bag, dict):
                    bags[vid if vid.startswith(cid) else f"{cid}-{vid}"] = rewrite(bag)
        elif any(k in comp for k in ("backgroundColor", "textColor", "background", "foreground")):
            bags[cid] = rewrite({k: v for k, v in comp.items() if not isinstance(v, (dict, list))})
    if bags:
        front["components"] = bags

    lines = ["---", yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=100).rstrip(), "---", ""]
    lines += [f"# {front['name']}", ""]
    overview = (doc.get("overview") or (doc.get("rationale") or {}).get("overview") or "").strip()
    lines += ["## Overview", "", overview or f"Brand tokens for {name}, reframed with the {aspect} frame as the unit.", ""]
    intent = doc.get("intent") or {}
    if intent:
        lines += ["## The Frame", "",
                  f"- **Reference:** {intent.get('reference', '')}",
                  f"- **Direction:** {intent.get('direction', '')}",
                  f"- **Signature:** {intent.get('signature', '')}",
                  f"- **Primary:** {aspect}. Author frame-relative sizes in `cqw`/`cqh`; never `vw`.", ""]
    motion = tokens.get("motion")
    if isinstance(motion, dict):
        lines += ["## Motion", "", "Pacing and dwell inherit `motion.*` in the frontmatter — extend those tokens, never a parallel set.",
                  (doc.get("rationale") or {}).get("motion", "").strip(), ""]
    sound = tokens.get("sound")
    if isinstance(sound, dict):
        lines += ["## Sound", "",
                  f"Material: {sound.get('material', '—')}. Transients land on the contact frame "
                  f"(lag ≤ {sound.get('sync-lag-max', '30ms')}, never leading). Holds are silence.",
                  (doc.get("rationale") or {}).get("sound", "").strip(), ""]
    cons = doc.get("constraints") or {}
    rat = doc.get("rationale") or {}
    dos = list(cons.get("always") or []) + list(rat.get("dos") or [])
    donts = list(cons.get("never") or []) + list(rat.get("donts") or [])
    if dos or donts:
        lines += ["## Composition Rules", ""]
        if dos:
            lines += ["### Do", ""] + [f"- {d}" for d in dos] + [""]
        if donts:
            lines += ["### Don't", ""] + [f"- {d}" for d in donts] + [""]
    lines += ["## Known Gaps", "",
              "- Layout, frame treatments, and beat structure are authored per video — this file carries brand, timing, and sound only.",
              "- Regenerate from `.design` after token edits; do not hand-edit values here.", ""]
    return "\n".join(lines)


def export_shadcn_registry(doc: dict, cfg: dict) -> dict:
    shadcn = ((doc.get("integrations") or {}).get("shadcn")) or {}
    css_vars = shadcn.get("css_vars") or {}
    item = {
        "$schema": "https://ui.shadcn.com/schema/registry-item.json",
        "name": f"{doc.get('name', 'brand')}-theme",
        "type": cfg.get("type", "registry:theme"),
        "title": f"{doc.get('name', 'brand')} theme",
        "description": doc.get("description", ""),
        "cssVars": {
            mode: {k: str(v) for k, v in (vars_ or {}).items()}
            for mode, vars_ in css_vars.items()
        },
    }
    if shadcn.get("radius") and "theme" not in item["cssVars"]:
        item["cssVars"]["theme"] = {"radius": str(shadcn["radius"])}
    return item


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=pathlib.Path)
    parser.add_argument("--out-dir", type=pathlib.Path, default=None)
    parser.add_argument("--only", default=None, help="comma list: css,tailwind,dtcg,shadcn_registry,frame_md")
    args = parser.parse_args()

    doc = yaml.safe_load(args.file.read_text(encoding="utf-8"))
    exports = doc.get("exports") or {}
    only = set(args.only.split(",")) if args.only else None
    handlers = {
        "css": (export_css, "tokens.css", False),
        "tailwind": (export_tailwind, "tailwind.theme.css", False),
        "dtcg": (export_dtcg, "tokens.json", True),
        "shadcn_registry": (export_shadcn_registry, "brand-theme.json", True),
        "frame_md": (export_frame_md, "frame.md", False),
    }

    wrote = 0
    for key, (handler, default_name, is_json) in handlers.items():
        if only is not None and key not in only:
            continue
        cfg = exports.get(key)
        if cfg is None and only is None:
            continue
        cfg = cfg or {}
        result = handler(doc, cfg)
        declared = cfg.get("path")
        if args.out_dir is not None:
            target = args.out_dir / (pathlib.Path(declared).name if declared else default_name)
        elif declared:
            target = (args.file.parent / declared).resolve()
        else:
            print(f"skip {key}: no exports.{key}.path and no --out-dir")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(result, indent=2) + "\n" if is_json else result
        target.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {key:16} {target}")
        wrote += 1

    if not wrote:
        print("nothing exported (no exports.* declared; use --only + --out-dir to force)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
