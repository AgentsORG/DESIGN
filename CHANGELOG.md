# Changelog

All notable changes to the `.design` format and this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project uses SemVer for the **contract schema** (`design.v1`, future `design.v2`).

## [Unreleased]

### Added

- **Self-contained files:** `agent.instructions` is required (schema + SPEC §8); drag-drop / @-mention works without the skill
- Canonical template: [docs/self-contained.md](docs/self-contained.md); examples patched via `scripts/patch_agent_instructions.py`
- Design-engineering **CRAFT** bar in `skills/design/references/CRAFT.md`
- Expanded `REVIEW.md` triage + Before/After/Why findings table
- Craft gates in `APPLY.md`; SPEC §15.1.1 craft-defaults note
- Official [skills.sh](https://skills.sh/AgentsORG/DESIGN) badge on README + skill README

## [1.0.0] — 2026-08-05

### Added

- Normative **design.v1** specification ([SPEC.md](SPEC.md))
- JSON Schema ([schema/design.v1.schema.json](schema/design.v1.schema.json))
- Portable Agent Skill (`skills/design/`) for discover → read → follow → update → verify
- Google DESIGN.md parity: component property bags, `rationale`, `omitted`
- Integrations: `shadcn`, `figma`
- `themes`, `exports` (DTCG/CSS/Tailwind/…), `assets`
- Token groups: color, typography, spacing, radius, elevation, motion, breakpoint, opacity, zIndex, iconography
- Examples converted from [getdesign.md](https://getdesign.md/) analyses (independent — not affiliated)
- Documentation hub with Mermaid diagrams ([docs/INDEX.md](docs/INDEX.md))
