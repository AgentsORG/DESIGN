#!/usr/bin/env python3
"""Convert getdesign.md / awesome-design-md DESIGN.md files into design.v1 .design examples.

Preserves DESIGN.md frontmatter tokens AND markdown body sections (rationale)
so the designing process does not lose prose guidance.
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(r"C:\PROJECTS\AgentsORG\DESIGN")

PROP_ALIASES = {
    "backgroundColor": "backgroundColor",
    "textColor": "textColor",
    "rounded": "rounded",
    "typography": "typography",
    "padding": "padding",
    "size": "size",
    "height": "height",
    "width": "width",
    # tolerate if sources already used aliases
    "background": "backgroundColor",
    "foreground": "textColor",
    "radius": "rounded",
}


def extract_fm(text: str) -> tuple[str | None, str]:
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S | re.M)
    if not m:
        m = re.search(r"---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def parse_simple_yaml_frontmatter(fm: str) -> dict:
    """Lightweight scrape of DESIGN.md YAML frontmatter."""
    data: dict = {
        "colors": {},
        "typography": {},
        "rounded": {},
        "spacing": {},
        "components": {},
        "meta": {},
        "omitted": [],
    }
    for key in ("name", "description", "version"):
        m = re.search(rf"^{key}:\s*[\"']?(.*?)[\"']?\s*$", fm, re.M)
        if m:
            data["meta"][key] = m.group(1).strip().strip('"')

    section = None
    current_comp = None
    current_typo = None
    for line in fm.splitlines():
        if re.match(r"^colors:\s*$", line):
            section = "colors"
            current_comp = current_typo = None
            continue
        if re.match(r"^typography:\s*$", line):
            section = "typography"
            current_comp = current_typo = None
            continue
        if re.match(r"^rounded:\s*$", line):
            section = "rounded"
            current_comp = current_typo = None
            continue
        if re.match(r"^spacing:\s*$", line):
            section = "spacing"
            current_comp = current_typo = None
            continue
        if re.match(r"^components:\s*$", line):
            section = "components"
            current_comp = current_typo = None
            continue
        if re.match(r"^omitted:\s*$", line):
            section = "omitted"
            current_comp = current_typo = None
            continue
        if re.match(r"^[a-zA-Z].*:\s*$", line) and not line.startswith(" "):
            section = None
            current_comp = current_typo = None
            continue

        if section == "omitted":
            m = re.match(r"^\s+-\s+(.+)\s*$", line)
            if m:
                data["omitted"].append(m.group(1).strip().strip('"'))
            continue

        if section == "colors":
            m = re.match(r"^\s+([A-Za-z0-9_-]+):\s*[\"']?([^\"'#\n]+|#[0-9A-Fa-f]+)[\"']?\s*$", line)
            if m:
                data["colors"][m.group(1)] = m.group(2).strip().strip('"')
        elif section in ("rounded", "spacing"):
            m = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.+)\s*$", line)
            if m:
                data[section][m.group(1)] = m.group(2).strip().strip('"')
        elif section == "typography":
            m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
            if m:
                current_typo = m.group(1)
                data["typography"][current_typo] = {}
                continue
            if current_typo:
                m2 = re.match(r"^\s{4}([A-Za-z0-9_-]+):\s*(.+)\s*$", line)
                if m2:
                    data["typography"][current_typo][m2.group(1)] = m2.group(2).strip().strip('"')
        elif section == "components":
            m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
            if m:
                current_comp = m.group(1)
                data["components"][current_comp] = {}
                continue
            if current_comp:
                m2 = re.match(r"^\s{4}([A-Za-z0-9_-]+):\s*(.+)\s*$", line)
                if m2:
                    data["components"][current_comp][m2.group(1)] = m2.group(2).strip().strip('"')
    return data


SECTION_ALIASES = {
    "overview": "overview",
    "brand & style": "overview",
    "brand and style": "overview",
    "colors": "colors",
    "typography": "typography",
    "layout": "layout",
    "layout & spacing": "layout",
    "layout and spacing": "layout",
    "elevation & depth": "elevation",
    "elevation and depth": "elevation",
    "elevation": "elevation",
    "shapes": "shapes",
    "components": "components",
    "do's and don'ts": "dos_donts",
    "dos and don'ts": "dos_donts",
    "do’s and don’ts": "dos_donts",
    "dos and donts": "dos_donts",
    "responsive behavior": "responsive",
    "responsive": "responsive",
    "iteration guide": "iteration",
    "known gaps": "known_gaps",
    "iconography": "iconography",
    "motion": "motion",
    "accessibility": "accessibility",
}


def parse_markdown_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current:
                sections[current] = "\n".join(buf).strip()
            title = m.group(1).strip().lower().rstrip(":").strip()
            # Known alias or slugify unknown headings so nothing is dropped
            current = SECTION_ALIASES.get(title) or re.sub(r"[^a-z0-9]+", "_", title).strip("_")
            buf = []
            continue
        if current is not None:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()
    return sections


def extract_dos_donts(text: str) -> tuple[list[str], list[str]]:
    dos: list[str] = []
    donts: list[str] = []
    mode = None  # "do" | "dont" under ### Do / ### Don't headings
    for line in text.splitlines():
        h = re.match(r"^###\s+(.+?)\s*$", line)
        if h:
            ht = h.group(1).strip().lower()
            if ht.startswith("don't") or ht.startswith("dont") or ht == "don'ts" or ht == "donts":
                mode = "dont"
            elif ht.startswith("do") or ht == "dos":
                mode = "do"
            else:
                mode = None
            continue
        s = line.strip()
        raw = re.sub(r"^[-*•]\s*", "", s).strip()
        if not raw:
            continue
        low = raw.lower()
        if low.startswith("don't ") or low.startswith("dont ") or low.startswith("do not "):
            donts.append(re.sub(r"^(don't|dont|do not)\s+", "", raw, flags=re.I).strip())
        elif low.startswith("do "):
            dos.append(re.sub(r"^do\s+", "", raw, flags=re.I).strip())
        elif mode == "dont" and s.startswith(("-", "*", "•")):
            donts.append(re.sub(r"^(don't|dont|do not)\s+", "", raw, flags=re.I).strip())
        elif mode == "do" and s.startswith(("-", "*", "•")):
            dos.append(re.sub(r"^do\s+", "", raw, flags=re.I).strip())
    return dos, donts


def yaml_quote(s: str) -> str:
    if s is None:
        return '""'
    s = str(s)
    if re.search(r'[:#\[\]{},&*?|>!%@`]', s) or s.startswith(" ") or s.endswith(" ") or "\n" in s:
        return json.dumps(s)
    if s == "" or s.lower() in ("true", "false", "null") or re.match(r"^-?\d", s):
        return json.dumps(s)
    return s


def rewrite_refs(val: str) -> str:
    return (
        val.replace("{colors.", "{tokens.color.")
        .replace("{rounded.", "{tokens.radius.")
        .replace("{typography.", "{tokens.typography.")
        .replace("{spacing.", "{tokens.spacing.")
        .replace("{component.", "{components.")
    )


def typo_to_block(name: str, obj: dict) -> str:
    lines = [f"    {name}:"]
    for k in (
        "fontFamily",
        "fontSize",
        "fontWeight",
        "lineHeight",
        "letterSpacing",
        "fontFeature",
        "fontVariation",
    ):
        if k in obj:
            lines.append(f"      {k}: {yaml_quote(obj[k])}")
    return "\n".join(lines)


def emit_literal_block(key: str, text: str, indent: int = 2) -> list[str]:
    """Emit a YAML literal block scalar."""
    pad = " " * indent
    lines = [f"{pad}{key}: |"]
    if not text.strip():
        lines.append(f"{pad}  ")
        return lines
    for ln in text.splitlines():
        lines.append(f"{pad}  {ln}")
    return lines


def build_shadcn_map(colors: dict) -> dict:
    c = colors

    def pick(*keys, default=None):
        for k in keys:
            if k in c:
                return c[k]
        return default

    light = {
        "background": pick("canvas", "background", "neutral", "surface", default="#ffffff"),
        "foreground": pick("ink", "text", "foreground", default="#0a0a0a"),
        "card": pick("surface-1", "surface", "card", "canvas", default="#ffffff"),
        "card-foreground": pick("ink", "text", "foreground", default="#0a0a0a"),
        "popover": pick("surface-1", "surface", "canvas", default="#ffffff"),
        "popover-foreground": pick("ink", "text", default="#0a0a0a"),
        "primary": pick("primary", default="#0a0a0a"),
        "primary-foreground": pick("on-primary", default="#ffffff"),
        "secondary": pick("secondary", "surface-2", "surface-1", default="#f4f4f5"),
        "secondary-foreground": pick("ink", "text", default="#0a0a0a"),
        "muted": pick("surface-2", "surface-1", "muted", default="#f4f4f5"),
        "muted-foreground": pick("ink-muted", "ink-subtle", "mute", "body-muted", default="#71717a"),
        "accent": pick("surface-2", "accent", default="#f4f4f5"),
        "accent-foreground": pick("ink", "text", default="#0a0a0a"),
        "destructive": pick("danger", "destructive", "error", "semantic-error", default="#dc2626"),
        "border": pick("hairline", "border", default="#e4e4e7"),
        "input": pick("hairline", "border", "input", default="#e4e4e7"),
        "ring": pick("primary-focus", "primary", "ring", default="#0a0a0a"),
    }
    canvas = (pick("canvas") or "").lower()
    is_dark = canvas in ("#000", "#000000", "#010102", "#0a0a0a") or (
        canvas.startswith("#") and len(canvas) >= 7 and int(canvas[1:3], 16) < 40
    )
    return {"light": light, "is_dark_marketing": is_dark}


def emit_property_bag(props: dict, indent: int) -> list[str]:
    pad = " " * indent
    lines = []
    for pk, pv in props.items():
        key = PROP_ALIASES.get(pk, pk)
        pv2 = rewrite_refs(str(pv))
        lines.append(f"{pad}{key}: {yaml_quote(pv2)}")
    return lines


BRANDS = {
    "vercel": {
        "file": ".tmp-vercel-DESIGN.md",
        "slug": "vercel",
        "getdesign": "https://getdesign.md/vercel/design-md",
        "site": "https://vercel.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/vercel/DESIGN.md",
        "intent_ref": "Vercel marketing — black/white precision, Geist, maximal restraint",
    },
    "stripe": {
        "file": ".tmp-stripe-DESIGN.md",
        "slug": "stripe",
        "getdesign": "https://getdesign.md/stripe/design-md",
        "site": "https://stripe.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/stripe/DESIGN.md",
        "intent_ref": "Stripe marketing — signature purple gradients, weight-300 elegance, fintech clarity",
    },
    "notion": {
        "file": ".tmp-notion-DESIGN.md",
        "slug": "notion",
        "getdesign": "https://getdesign.md/notion/design-md",
        "site": "https://notion.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/notion/DESIGN.md",
        "intent_ref": "Notion — warm minimalism, serif headings, soft surfaces, workspace calm",
    },
    "apple": {
        "file": ".tmp-apple-DESIGN.md",
        "slug": "apple",
        "getdesign": "https://getdesign.md/apple/design-md",
        "site": "https://apple.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/apple/DESIGN.md",
        "intent_ref": "Apple marketing — premium whitespace, SF Pro, cinematic product photography",
    },
    "linear": {
        "file": ".tmp-linear.app-DESIGN.md",
        "slug": "linear",
        "getdesign": "https://getdesign.md/linear.app/design-md",
        "site": "https://linear.app",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md",
        "intent_ref": "Linear.app — ultra-minimal dark SaaS, lavender accent, product screenshots as hero",
    },
    "supabase": {
        "file": ".tmp-supabase-DESIGN.md",
        "slug": "supabase",
        "getdesign": "https://getdesign.md/supabase/design-md",
        "site": "https://supabase.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/supabase/DESIGN.md",
        "intent_ref": "Supabase — dark emerald developer platform, code-first documentation aesthetic",
    },
}


def emit_design(slug: str, cfg: dict, data: dict, sections: dict[str, str]) -> str:
    colors = data["colors"]
    typo = data["typography"]
    rounded = data["rounded"]
    spacing = data["spacing"]
    comps = data["components"]
    meta = data["meta"]
    sh = build_shadcn_map(colors)

    overview = sections.get("overview") or meta.get("description") or cfg["intent_ref"]
    # truncate description one-liner
    desc = meta.get("description") or overview
    if len(desc) > 220:
        desc = desc[:217].rstrip() + "..."

    dos, donts = [], []
    if "dos_donts" in sections:
        dos, donts = extract_dos_donts(sections["dos_donts"])

    lines: list[str] = []
    lines.append("schema: design.v1")
    lines.append(f"name: {slug}")
    lines.append("version: 1.0.0")
    lines.append("status: refine")
    lines.append(f"description: {yaml_quote(desc)}")
    lines.append("")
    lines.append("$schema: https://raw.githubusercontent.com/AgentsORG/DESIGN/main/schema/design.v1.schema.json")
    lines.append("")
    lines.append("agent:")
    lines.append("  skill: design")
    lines.append("  instructions: |")
    lines.append("    READ this file before UI work. Source: getdesign.md / DESIGN.md analysis.")
    lines.append("    FOLLOW tokens, components (property bags), rationale.*, and constraints.")
    lines.append("    Component props use DESIGN.md names (backgroundColor, textColor, rounded, …).")
    lines.append("    If integrations.shadcn is present, map tokens into CSS variables.")
    lines.append("    UPDATE in place; ask before changing locked paths.")
    lines.append("    Not affiliated with the brand; independent visual analysis.")
    lines.append("")
    lines.extend(emit_literal_block("overview", overview, indent=0))
    lines.append("")
    lines.append("intent:")
    lines.append(f"  reference: {yaml_quote(cfg['intent_ref'])}")
    lines.append("  density: comfortable")
    lines.append("  trust: high")
    lines.append("  energy: medium")
    lines.append("  playfulness: low")
    lines.append("")
    lines.append("targets:")
    lines.append("  - web")
    lines.append("")
    lines.append("sources:")
    lines.append("  - type: url")
    lines.append(f"    ref: {cfg['getdesign']}")
    lines.append("    note: getdesign.md curated DESIGN.md analysis")
    lines.append("  - type: url")
    lines.append(f"    ref: {cfg['site']}")
    lines.append("  - type: file")
    lines.append(f"    path: {cfg['upstream']}")
    lines.append("    note: Upstream DESIGN.md (awesome-design-md)")
    lines.append("  - type: other")
    lines.append("    note: Independent analysis — not affiliated with the brand")
    lines.append("")

    # tokens
    lines.append("tokens:")
    lines.append("  color:")
    for k, v in colors.items():
        lines.append(f"    {k}: {yaml_quote(v)}")
    if typo:
        lines.append("  typography:")
        for name, obj in typo.items():
            lines.append(typo_to_block(name, obj))
    if spacing:
        lines.append("  spacing:")
        if "unit" not in spacing and "base" not in spacing:
            lines.append("    unit: 8")
        for k, v in spacing.items():
            lines.append(f"    {k}: {yaml_quote(v)}")
    if rounded:
        lines.append("  radius:")
        for k, v in rounded.items():
            lines.append(f"    {k}: {yaml_quote(v)}")
    # elevation placeholder note — detailed treatments live in rationale.elevation
    lines.append("  elevation:")
    lines.append('    note: "See rationale.elevation for brand depth model; add concrete shadow tokens as they stabilize."')
    lines.append("")

    lock_keys = []
    for k in ("primary", "canvas", "ink", "background"):
        if k in colors:
            lock_keys.append(f"tokens.color.{k}")
    if lock_keys:
        lines.append("locked:")
        for k in lock_keys[:3]:
            lines.append(f"  - {k}")
        lines.append("")

    # components — preserve ALL DESIGN.md entries
    # Prefer catalog grouping for button-* while also retaining flat keys via tokens
    lines.append("components:")
    button_vars = [c for c in comps if c.startswith("button")]
    other = [c for c in comps if not c.startswith("button")]

    if button_vars:
        lines.append("  button:")
        lines.append('    description: "Button family from DESIGN.md component tokens"')
        lines.append('    when: ["primary and secondary actions", "CTAs documented in rationale.components"]')
        lines.append('    when_not: ["inventing off-system button chrome", "more than one filled primary per view unless brand allows"]')
        lines.append("    variants:")
        for c in button_vars:
            lines.append(f"      - {c}")  # keep full DESIGN.md key for lossless round-trip
        # derive states from suffix
        states = sorted(
            {
                s
                for c in button_vars
                for s in ("default", "hover", "active", "focus", "disabled", "pressed")
                if c.endswith("-" + s) or s == "default"
            }
        )
        lines.append(f"    states: [{', '.join(states)}]")
        lines.append("    tokens:")
        for c in button_vars:
            lines.append(f"      {c}:")
            lines.extend(emit_property_bag(comps[c], indent=8))

    for c in other:
        props = comps[c]
        lines.append(f"  {c}:")
        lines.append('    description: "DESIGN.md component token group"')
        lines.append('    when: ["as documented in rationale.components and getdesign analysis"]')
        lines.append('    when_not: ["decorative misuse outside brand patterns"]')
        # flat DESIGN.md bags also mirrored under tokens.default for catalog form
        lines.append("    variants: [default]")
        lines.append("    tokens:")
        lines.append("      default:")
        lines.extend(emit_property_bag(props, indent=8))
        # also emit DESIGN.md-native top-level sibling for lossless interop
        # (agents can read either). We keep catalog form as primary to avoid duplicate
        # root keys with same name — property bag is under tokens.default.
    lines.append("")

    # rationale — full DESIGN.md body sections (canonical + extras)
    lines.append("rationale:")
    canonical = (
        "overview",
        "colors",
        "typography",
        "layout",
        "elevation",
        "shapes",
        "components",
        "responsive",
        "iteration",
        "known_gaps",
        "iconography",
        "motion",
        "accessibility",
    )
    emitted = set()
    for key in canonical:
        if key in sections and sections[key].strip():
            lines.extend(emit_literal_block(key, sections[key], indent=2))
            emitted.add(key)
    # Any other ## sections (never drop)
    for key, text in sections.items():
        if key in emitted or key == "dos_donts":
            continue
        if text and text.strip():
            lines.extend(emit_literal_block(key, text, indent=2))
    if dos:
        lines.append("  dos:")
        for d in dos:
            lines.append(f"    - {yaml_quote(d)}")
    if donts:
        lines.append("  donts:")
        for d in donts:
            lines.append(f"    - {yaml_quote(d)}")
    if "dos_donts" in sections and not dos and not donts:
        lines.extend(emit_literal_block("dos_donts_raw", sections["dos_donts"], indent=2))
    lines.append("")

    if data.get("omitted"):
        lines.append("omitted:")
        for o in data["omitted"]:
            lines.append(f"  - {yaml_quote(o)}")
        lines.append("")

    # shadcn
    lines.append("integrations:")
    lines.append("  shadcn:")
    lines.append("    enabled: true")
    lines.append("    style: new-york")
    lines.append("    css_variables: true")
    lines.append("    base_color: neutral")
    lines.append("    css: app/globals.css")
    lines.append("    components_json: ./components.json")
    lines.append("    aliases:")
    lines.append('      components: "@/components"')
    lines.append('      utils: "@/lib/utils"')
    lines.append('      ui: "@/components/ui"')
    radius_base = rounded.get("md") or rounded.get("lg") or "0.5rem"
    lines.append(f"    radius: {yaml_quote(radius_base)}")
    lines.append("    css_vars:")
    mode = "dark" if sh["is_dark_marketing"] else "light"
    lines.append(f"      {mode}:")
    for k, v in sh["light"].items():
        lines.append(f"        {k}: {yaml_quote(v)}")
    lines.append("    map_from_tokens:")
    lines.append("      background: tokens.color.canvas|tokens.color.surface|tokens.color.background")
    lines.append("      foreground: tokens.color.ink|tokens.color.text|tokens.color.foreground")
    lines.append("      primary: tokens.color.primary")
    lines.append("      primary-foreground: tokens.color.on-primary")
    lines.append("      border: tokens.color.hairline|tokens.color.border")
    lines.append("      ring: tokens.color.primary-focus|tokens.color.primary")
    lines.append("")

    lines.append("policy:")
    lines.append("  if_missing: ask")
    lines.append("  hierarchy: [typography, spacing, contrast, color]")
    lines.append("  reuse:")
    lines.append("    prefer_existing_components: true")
    lines.append("  accessibility:")
    lines.append("    contrast: AA")
    lines.append("    focus_visible: required")
    lines.append("")

    lines.append("constraints:")
    lines.append("  always:")
    lines.append("    - use semantic tokens from this file; never invent off-brand hex")
    lines.append("    - bind every listed component property (backgroundColor, textColor, typography, rounded, padding, size, height, width)")
    lines.append("    - read rationale.layout / rationale.elevation / rationale.shapes before inventing chrome")
    lines.append("    - when shadcn is enabled, apply integrations.shadcn.css_vars to globals.css")
    lines.append("    - prefer catalog components over one-off controls")
    for d in dos[:8]:
        lines.append(f"    - {yaml_quote(d)}")
    lines.append("  never:")
    lines.append("    - generic purple-on-white AI chrome unrelated to this brand")
    lines.append("    - dropping DESIGN.md component variants or rationale during restyle")
    for d in donts[:8]:
        lines.append(f"    - {yaml_quote(d)}")
    lines.append("")

    lines.append("examples:")
    lines.append("  good:")
    lines.append(f"    - ref: {cfg['site']}")
    lines.append("      note: Live brand marketing / product surfaces")
    lines.append(f"    - ref: {cfg['getdesign']}")
    lines.append("      note: Source DESIGN.md analysis")
    lines.append("")
    lines.append("provenance:")
    lines.append("  owner: AgentsORG")
    lines.append('  last_reviewed: "2026-08-05"')
    lines.append("  source_material:")
    lines.append(f"    - {cfg['getdesign']}")
    lines.append(f"    - {cfg['upstream']}")
    lines.append(f"    - {cfg['site']}")
    lines.append("    - https://github.com/google-labs-code/design.md/blob/main/docs/spec.md")
    lines.append("")
    return "\n".join(lines)


def main():
    out_dir = ROOT / "examples"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.design"):
        old.unlink()
        print("removed", old.name)

    for slug, cfg in BRANDS.items():
        src = ROOT / cfg["file"]
        text = src.read_text(encoding="utf-8")
        fm, body = extract_fm(text)
        if not fm:
            print("NO FM", slug)
            continue
        data = parse_simple_yaml_frontmatter(fm)
        sections = parse_markdown_sections(body)
        content = emit_design(slug, cfg, data, sections)
        dest = out_dir / f"{slug}.design"
        dest.write_text(content, encoding="utf-8")
        print(
            "wrote",
            dest.name,
            "colors=",
            len(data["colors"]),
            "typo=",
            len(data["typography"]),
            "comps=",
            len(data["components"]),
            "rationale=",
            list(sections.keys()),
        )


if __name__ == "__main__":
    main()
