#!/usr/bin/env python3
"""Convert getdesign.md / awesome-design-md DESIGN.md files into design.v1 .design examples.

Preserves DESIGN.md frontmatter tokens AND markdown body sections (rationale)
so the designing process does not lose prose guidance.
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Some upstream analyses obfuscate brand names; examples use the real name
# consistently (non-affiliation is covered by NOTICE.md and sources notes).
BRAND_NAME_FIXES = {
    "Stripi": "Stripe",
    "Supabaze": "Supabase",
}

SELF_CONTAINED_INSTRUCTIONS = """You are holding a .design living visual contract (schema design.v1).
If the AgentsORG `design` skill is installed, activate it - then still obey THIS file as source of truth.
If the skill is absent, follow these instructions exactly.

READ
- Load this file before any UI generation or restyle. Large file? Normative core first
  (intent, constraints, policy/decisions, tokens, components, themes, voice, locked); rationale on demand.
- Order: overview/intent -> constraints -> policy/decisions -> tokens -> voice -> rationale -> components/patterns -> integrations -> locked.
- Tokens and structured rules are normative. Rationale is judgment when tokens under-specify.

FOLLOW (generate or edit UI)
- Calibrate treatment per surface: patterns.<name>.treatment > intent.treatment
  (utilitarian = restrained product craft; editorial = distinctive identity).
- Prefer catalog components; obey when / when_not and decisions.* (first match wins).
- Bind every listed component property (backgroundColor, textColor, typography, rounded, padding, size, height, width).
- Never invent raw hex/spacing/radius when a token exists.
- Apply patterns.*; enforce constraints.always / never; apply voice.* to all UI copy.
- Concentrate boldness in intent.signature; keep everything around it quiet.
- Themes: generate for the active mode (themes.default); modes are designed, never inverted.
- Match the project's existing styling stack - do not switch stacks.
- If integrations.shadcn.enabled: prefer shadcn UI; write css_vars into the listed CSS file; tokens win on conflict.
- If integrations.figma is present: this file is repo-canonical unless sync.direction says otherwise; ask on conflicts.
- Craft defaults when this file is silent: one primary CTA; nested radius = outer - padding; transform/opacity only (<300ms); 44x44 targets; focus visible; prefers-reduced-motion; no transition:all.

UPDATE
- Edit this file in place when design changes. Git is history.
- Ask before changing any path in locked. Bump version (SemVer).

VERIFY
- Compare tokens <-> CSS/Tailwind and components <-> imports; report drift per token group
  as added/removed/modified plus a regression flag before fixing.

PRECEDENCE
1) User prompt  2) This file  3) design skill  4) Generic taste skills  5) Model defaults

NEVER
- Invent a parallel design system beside this file
- Embed binaries or full page HTML trees here
- Claim affiliation with third-party brands used only as visual references"""

# Appended only to brand-analysis examples (not to generic templates/stubs).
BRAND_DISCLAIMER = """
DISCLAIMER
Independent visual analysis - not affiliated with the named brand. Adapt before production use."""

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
        return json.dumps(s, ensure_ascii=False)
    if s and s[0] in "\"'-":
        return json.dumps(s, ensure_ascii=False)
    if s == "" or s.lower() in ("true", "false", "null", "yes", "no", "on", "off", "y", "n", "~") or re.match(r"^-?\d", s):
        return json.dumps(s, ensure_ascii=False)
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
    """Emit a YAML literal block scalar (prose refs rewritten to tokens.*)."""
    pad = " " * indent
    lines = [f"{pad}{key}: |"]
    if not text.strip():
        lines.append(f"{pad}  ")
        return lines
    for ln in rewrite_refs(text).splitlines():
        lines.append(f"{pad}  {ln}")
    return lines


def _hex_rgb(value: str):
    m = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", str(value).strip())
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def _contrast(fg: str, bg: str):
    a, b = _hex_rgb(fg), _hex_rgb(bg)
    if a is None or b is None:
        return None

    def lum(rgb):
        chan = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
        return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2]

    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


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
    # contrast-correct our own derived pairs: muted-foreground must read on muted
    ratio = _contrast(light["muted-foreground"], light["muted"])
    if ratio is not None and ratio < 4.5:
        for candidate in (pick("body", "text-secondary", "ink-soft"), light["foreground"]):
            if candidate and (_contrast(candidate, light["muted"]) or 0) >= 4.5:
                light["muted-foreground"] = candidate
                break

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
        "direction": "stark monochrome engineering",
        "signature": "The multi-stop mesh gradient at hero scale — the only color in an otherwise black-and-white system",
        "voice_register": "Terse, technical, engineer-to-engineer; imperative mood; zero hype",
    },
    "stripe": {
        "file": ".tmp-stripe-DESIGN.md",
        "slug": "stripe",
        "getdesign": "https://getdesign.md/stripe/design-md",
        "site": "https://stripe.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/stripe/DESIGN.md",
        "intent_ref": "Stripe marketing — signature purple gradients, weight-300 elegance, fintech clarity",
        "direction": "polished fintech clarity",
        "signature": "The animated multi-color gradient ribbon over otherwise disciplined neutrals",
        "voice_register": "Precise, confident, benefit-led; explains money movement plainly",
    },
    "notion": {
        "file": ".tmp-notion-DESIGN.md",
        "slug": "notion",
        "getdesign": "https://getdesign.md/notion/design-md",
        "site": "https://notion.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/notion/DESIGN.md",
        "intent_ref": "Notion — warm minimalism, serif headings, soft surfaces, workspace calm",
        "direction": "warm editorial minimalism",
        "signature": "Hand-drawn spot illustrations on calm ivory surfaces",
        "voice_register": "Friendly, plain-spoken, lowercase-calm; tool talk without jargon",
    },
    "apple": {
        "file": ".tmp-apple-DESIGN.md",
        "slug": "apple",
        "getdesign": "https://getdesign.md/apple/design-md",
        "site": "https://apple.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/apple/DESIGN.md",
        "intent_ref": "Apple marketing — premium whitespace, SF Pro, cinematic product photography",
        "direction": "cinematic product minimalism",
        "signature": "Full-bleed product photography carrying entire sections; type stays out of its way",
        "voice_register": "Declarative, rhythmic short lines; superlatives spent sparingly",
    },
    "linear": {
        "file": ".tmp-linear.app-DESIGN.md",
        "slug": "linear",
        "getdesign": "https://getdesign.md/linear.app/design-md",
        "site": "https://linear.app",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md",
        "intent_ref": "Linear.app — ultra-minimal dark SaaS, lavender accent, product screenshots as hero",
        "direction": "dark precision software",
        "signature": "Glass-and-glow product panels floating on near-black",
        "voice_register": "Crisp, opinionated, low-noise; states positions without hedging",
    },
    "supabase": {
        "file": ".tmp-supabase-DESIGN.md",
        "slug": "supabase",
        "getdesign": "https://getdesign.md/supabase/design-md",
        "site": "https://supabase.com",
        "upstream": "https://github.com/voltagent/awesome-design-md/blob/main/design-md/supabase/DESIGN.md",
        "intent_ref": "Supabase — dark emerald developer platform, code-first documentation aesthetic",
        "direction": "dark developer utility",
        "signature": "A single emerald accent on near-black, code-first surfaces",
        "voice_register": "Direct, docs-like, developer-native; commands over descriptions",
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
    # one-line description: refs rewritten, uniform independent-analysis framing,
    # truncated at a word boundary
    desc = rewrite_refs(meta.get("description") or overview)
    brand_title = slug.capitalize()
    if "inspired interpretation" not in desc.lower():
        desc = f"An inspired interpretation of {brand_title}'s design language — " + desc[0].lower() + desc[1:]
    if len(desc) > 220:
        desc = desc[:217].rsplit(" ", 1)[0].rstrip(",;:") + " …"

    dos, donts = [], []
    if "dos_donts" in sections:
        dos, donts = extract_dos_donts(sections["dos_donts"])
        dos = [rewrite_refs(d) for d in dos]
        donts = [rewrite_refs(d) for d in donts]

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
    for line in (SELF_CONTAINED_INSTRUCTIONS + BRAND_DISCLAIMER).splitlines():
        lines.append(f"    {line}" if line else "    ")
    lines.append("")
    lines.extend(emit_literal_block("overview", overview, indent=0))
    lines.append("")
    lines.append("intent:")
    lines.append(f"  reference: {yaml_quote(cfg['intent_ref'])}")
    if cfg.get("direction"):
        lines.append(f"  direction: {yaml_quote(cfg['direction'])}")
    if cfg.get("signature"):
        lines.append(f"  signature: {yaml_quote(cfg['signature'])}")
    lines.append("  density: comfortable")
    lines.append("  trust: high")
    lines.append("  energy: medium")
    lines.append("  playfulness: low")
    lines.append("")
    if cfg.get("voice_register"):
        lines.append("voice:")
        lines.append(f"  register: {yaml_quote(cfg['voice_register'])}")
        lines.append("  casing: sentence")
        lines.append('  action_naming: "Button labels name the exact action; the same verb carries through the flow"')
        lines.append('  errors: "State what happened, why, and the next step; never blame the user"')
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
    lines.append("  - type: url")
    lines.append(f"    ref: {cfg['upstream']}")
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

    lines.append("omitted:")
    for o in data.get("omitted") or []:
        lines.append(f"  - {yaml_quote(o)}")
    lines.append("  - section: tokens.elevation")
    lines.append('    reason: "Depth model lives in rationale.elevation; add shadow tokens as they stabilize"')
    lines.append("")

    # shadcn
    lines.append("integrations:")
    lines.append("  shadcn:")
    lines.append("    enabled: true")
    lines.append("    style: new-york            # legacy style; current styles: see SPEC §7.1")
    lines.append("    icon_library: lucide")
    lines.append("    css_variables: true")
    lines.append("    base_color: neutral")
    lines.append("    css: app/globals.css")
    lines.append("    components_json: ./components.json")
    lines.append("    aliases:")
    lines.append('      components: "@/components"')
    lines.append('      utils: "@/lib/utils"')
    lines.append('      ui: "@/components/ui"')
    lines.append('      lib: "@/lib"')
    lines.append('      hooks: "@/hooks"')
    radius_base = rounded.get("md") or rounded.get("lg") or "0.5rem"
    lines.append(f"    radius: {yaml_quote(radius_base)}")
    lines.append("    css_vars:")
    lines.append("      theme:")
    lines.append(f"        radius: {yaml_quote(radius_base)}")
    mode = "dark" if sh["is_dark_marketing"] else "light"
    lines.append(f"      {mode}:")
    vars_full = dict(sh["light"])
    # sidebar defaults mirror background / primary / accent / border / ring
    vars_full.update(
        {
            "sidebar": vars_full["background"],
            "sidebar-foreground": vars_full["foreground"],
            "sidebar-primary": vars_full["primary"],
            "sidebar-primary-foreground": vars_full["primary-foreground"],
            "sidebar-accent": vars_full["accent"],
            "sidebar-accent-foreground": vars_full["accent-foreground"],
            "sidebar-border": vars_full["border"],
            "sidebar-ring": vars_full["ring"],
        }
    )
    # chart-1..5 from distinct brand accents when the palette provides them
    chart_candidates = []
    for key in ("link", "violet", "cyan", "success", "warning", "highlight-pink",
                "error", "accent", "primary"):
        val = colors.get(key)
        if val and val not in chart_candidates:
            chart_candidates.append(val)
    if len(chart_candidates) >= 5:
        for i, val in enumerate(chart_candidates[:5], start=1):
            vars_full[f"chart-{i}"] = val
    for k, v in vars_full.items():
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
    lines.append('  last_reviewed: "2026-08-06"')
    lines.append("  source_material:")
    lines.append(f"    - {cfg['getdesign']}")
    lines.append(f"    - {cfg['upstream']}")
    lines.append(f"    - {cfg['site']}")
    lines.append("    - https://github.com/google-labs-code/design.md/blob/main/docs/spec.md")
    lines.append("")
    return "\n".join(lines)


# Upstream analyses occasionally reference pipeline tooling that does not exist
# in this repo; scrub those lines so shipped files carry no dangling instructions.
SCRUB_LINE_PATTERNS = [
    re.compile(r"^.*derive-examples-block\.mjs.*$", re.M),
    re.compile(r"^.*resolve any TO_FILL markers.*$", re.M),
]
SCRUB_REPLACEMENT = "> Demonstration surfaces derived from the component tokens above; each `ex-*` entry reuses brand-native primitives so the same surfaces re-skin consistently."


def main():
    out_dir = ROOT / "examples"
    out_dir.mkdir(exist_ok=True)

    missing = [cfg["file"] for cfg in BRANDS.values() if not (ROOT / cfg["file"]).exists()]
    if missing:
        print("ABORT: missing converter inputs (gitignored DESIGN.md downloads):")
        for name in missing:
            print(f"  {name}")
        print("Download each brand's DESIGN.md into the repo root first (see BRANDS for URLs).")
        print("No files were deleted.")
        return 1

    for old in out_dir.glob("*.design"):
        old.unlink()
        print("removed", old.name)

    for slug, cfg in BRANDS.items():
        src = ROOT / cfg["file"]
        text = src.read_text(encoding="utf-8")
        for obfuscated, real in BRAND_NAME_FIXES.items():
            text = text.replace(obfuscated, real)
        for pattern in SCRUB_LINE_PATTERNS:
            text = pattern.sub(lambda m: SCRUB_REPLACEMENT if m.group(0).lstrip().startswith(">") else "", text)
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
    raise SystemExit(main() or 0)
