#!/usr/bin/env python3
"""Validate all .design files against the schema and core SPEC §19 lint rules.

Usage: python scripts/lint_design.py
Exit code 0 = all files pass (warnings allowed), 1 = any error.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]

REF_RE = re.compile(r"\{(tokens\.[A-Za-z0-9_.\-]+)\}")
ANY_REF_RE = re.compile(r"\{((?:tokens|components)\.[A-Za-z0-9_.\-]+)\}")
MAX_REF_DEPTH = 10
MAX_NEST_DEPTH = 20


def resolve_path(doc: dict, dotted: str):
    node = doc
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def token_refs_in(value) -> list[str]:
    if isinstance(value, str):
        return REF_RE.findall(value)
    if isinstance(value, dict):
        return [r for v in value.values() for r in token_refs_in(v)]
    if isinstance(value, list):
        return [r for v in value for r in token_refs_in(v)]
    return []


def nesting_depth(node, depth=0) -> int:
    if not isinstance(node, dict):
        return depth
    return max((nesting_depth(v, depth + 1) for v in node.values()), default=depth)


HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
ALIAS_PAIRS = [("background", "backgroundColor"), ("foreground", "textColor"), ("radius", "rounded")]
DUTIES = ("read", "follow", "update", "verify", "precedence")
FG_BG_PAIRS = [
    ("foreground", "background"),
    ("primary-foreground", "primary"),
    ("secondary-foreground", "secondary"),
    ("muted-foreground", "muted"),
    ("accent-foreground", "accent"),
    ("card-foreground", "card"),
    ("popover-foreground", "popover"),
    ("sidebar-foreground", "sidebar"),
]


def hex_to_rgb(value: str):
    m = HEX_RE.match(value.strip())
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def contrast_ratio(fg: str, bg: str):
    a, b = hex_to_rgb(fg), hex_to_rgb(bg)
    if a is None or b is None:
        return None

    def lum(rgb):
        chan = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2]

    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def resolve_color(doc: dict, value):
    """Follow a single-ref chain to a concrete string when possible."""
    for _ in range(MAX_REF_DEPTH):
        if not isinstance(value, str):
            return None
        stripped = value.strip()
        if REF_RE.fullmatch(stripped):
            value = resolve_path(doc, stripped[1:-1])
            continue
        return stripped
    return None


def lint(path: pathlib.Path, validator: Draft202012Validator) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(doc, dict):
        return [f"file does not parse as a single YAML mapping (got {type(doc).__name__})"], []

    for err in validator.iter_errors(doc):
        errors.append(f"schema: {'/'.join(map(str, err.absolute_path))}: {err.message[:140]}")

    agent = doc.get("agent") if isinstance(doc.get("agent"), dict) else {}
    instructions = str(agent.get("instructions") or "").strip()
    if not instructions:
        errors.append("missing agent.instructions (file must be self-contained)")
    else:
        missing_duties = [
            d for d in DUTIES if not re.search(rf"\b{d}\b", instructions, re.IGNORECASE)
        ]
        if missing_duties:
            warnings.append(
                "agent.instructions may not cover duties: " + ", ".join(missing_duties)
            )

    intent = doc.get("intent")
    if isinstance(intent, dict) and not (intent.get("reference") or "").strip():
        errors.append("intent present without intent.reference")

    components = doc.get("components") if isinstance(doc.get("components"), dict) else {}

    def check_bag(bag: dict, where: str):
        for a, b in ALIAS_PAIRS:
            if a in bag and b in bag and bag[a] != bag[b]:
                errors.append(f"{where}: alias collision {a} vs {b} with different values")
        fg = resolve_color(doc, bag.get("textColor") or bag.get("foreground"))
        bg = resolve_color(doc, bag.get("backgroundColor") or bag.get("background"))
        if fg and bg:
            ratio = contrast_ratio(fg, bg)
            if ratio is not None and ratio < 3.0:
                warnings.append(f"{where}: contrast {ratio:.2f}:1 below 3:1 ({fg} on {bg})")

    for cid, comp in components.items():
        if not isinstance(comp, dict):
            continue
        if comp.get("variants") and not (comp.get("when") or comp.get("when_not")):
            errors.append(f"components.{cid}: variants without when/when_not")
        if "tokens" in comp and isinstance(comp["tokens"], dict):
            for vid, bag in comp["tokens"].items():
                if isinstance(bag, dict) and "disabled" not in vid:  # WCAG exempts disabled controls
                    check_bag(bag, f"components.{cid}.tokens.{vid}")
        elif any(k in comp for k in ("backgroundColor", "textColor", "background", "foreground")):
            check_bag(comp, f"components.{cid}")

    shadcn = ((doc.get("integrations") or {}).get("shadcn") or {})
    for mode, vars_map in (shadcn.get("css_vars") or {}).items():
        if not isinstance(vars_map, dict):
            continue
        for fg_key, bg_key in FG_BG_PAIRS:
            if fg_key in vars_map and bg_key in vars_map:
                ratio = contrast_ratio(str(vars_map[fg_key]), str(vars_map[bg_key]))
                if ratio is not None and ratio < 3.0:
                    warnings.append(
                        f"integrations.shadcn.css_vars.{mode}: {fg_key}/{bg_key} contrast {ratio:.2f}:1 below 3:1"
                    )

    tokens = doc.get("tokens") if isinstance(doc.get("tokens"), dict) else {}
    if nesting_depth(tokens) > MAX_NEST_DEPTH:
        errors.append(f"tokens nesting exceeds depth {MAX_NEST_DEPTH}")

    omitted_raw = doc.get("omitted") if isinstance(doc.get("omitted"), list) else []
    omitted = {
        str(o.get("section") if isinstance(o, dict) else o)
        for o in omitted_raw
    }

    def omitted_covers(*names: str) -> bool:
        """True when any omitted entry names the section or a parent of it."""
        return any(
            entry == name or name.startswith(entry + ".")
            for entry in omitted
            for name in names
        )

    color = tokens.get("color") if isinstance(tokens.get("color"), dict) else {}
    if "primary" not in color and not omitted_covers("tokens.color.primary", "colors"):
        warnings.append("no tokens.color.primary (add or declare in omitted)")
    if not tokens.get("typography") and not omitted_covers("tokens.typography", "typography"):
        warnings.append("no tokens.typography (add or declare in omitted)")

    # orphan color tokens: never referenced anywhere in the document (summary warning only)
    if isinstance(color, dict) and color:
        raw = path.read_text(encoding="utf-8")
        orphans = [
            k for k, v in color.items()
            if not isinstance(v, dict)
            and not re.search(rf"tokens\.color\.{re.escape(str(k))}(?![\w-])", raw)
        ]
        if len(orphans) > max(3, len(color) // 2):
            warnings.append(
                f"{len(orphans)}/{len(color)} color tokens never referenced "
                f"(e.g. {', '.join(orphans[:5])})"
            )

    # component references ({components.X}): valid when X resolves as a dot path,
    # names a component, or names a variant inside any component's tokens map
    component_names = set(components)
    for comp in components.values():
        if isinstance(comp, dict) and isinstance(comp.get("tokens"), dict):
            component_names |= set(comp["tokens"].keys())
    for section in ("tokens", "components", "themes", "integrations"):
        for ref in set(ANY_REF_RE.findall(str(doc.get(section) or ""))):
            if not ref.startswith("components."):
                continue
            target_name = ref.split(".", 1)[1]
            if resolve_path(doc, ref) is None and target_name.split(".")[0] not in component_names:
                warnings.append(f"{section}: unresolved component reference {{{ref}}}")

    # broken / deep token references (search normative fields)
    for section in ("tokens", "components", "themes", "integrations"):
        for ref in set(token_refs_in(doc.get(section))):
            seen: list[str] = []
            current = ref
            for _ in range(MAX_REF_DEPTH + 1):
                target = resolve_path(doc, current)
                if target is None:
                    errors.append(f"{section}: broken reference {{{ref}}}")
                    break
                if isinstance(target, str) and REF_RE.fullmatch(target.strip()):
                    nxt = target.strip()[1:-1]
                    if nxt in seen:
                        errors.append(f"{section}: circular reference {{{ref}}}")
                        break
                    seen.append(nxt)
                    current = nxt
                    continue
                break
            else:
                errors.append(f"{section}: reference chain deeper than {MAX_REF_DEPTH} at {{{ref}}}")

    return errors, warnings


def main() -> int:
    schema = json.loads((ROOT / "schema" / "design.v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    files = (
        sorted(ROOT.glob("examples/*.design"))
        + sorted(ROOT.glob("templates/*.design"))
        + sorted(ROOT.glob("skills/design/examples/*.design"))
    )
    if not files:
        print("no .design files found")
        return 1

    failed = False
    for path in files:
        rel = path.relative_to(ROOT)
        try:
            errors, warnings = lint(path, validator)
        except Exception as exc:  # keep linting the remaining files
            errors, warnings = [f"lint crashed: {type(exc).__name__}: {exc}"], []
        for w in warnings:
            print(f"WARN  {rel}: {w}")
        for e in errors:
            print(f"ERROR {rel}: {e}")
        if errors:
            failed = True
        else:
            print(f"OK    {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
