# Changelog

All notable changes to the `.design` format and this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project uses SemVer for the **contract schema** (`design.v1`, future `design.v2`).

## [Unreleased]

## [1.0.0] — 2026-08-05

### Added

- Normative **design.v1** specification ([SPEC.md](SPEC.md))
- JSON Schema ([schema/design.v1.schema.json](schema/design.v1.schema.json)) — requires `agent.instructions`
- **Self-contained files** — every `.design` teaches READ → FOLLOW → UPDATE → VERIFY on drag-drop ([docs/self-contained.md](docs/self-contained.md))
- Portable Agent Skill (`skills/design/`) with CRAFT bar + ui-review-style REVIEW
- Google DESIGN.md parity: tokens, component property bags, full `rationale.*`, `omitted`
- Integrations: `shadcn`, `figma`; `themes`, `exports`, `assets`
- Token groups: color, typography, spacing, radius, elevation, motion, breakpoint, opacity, zIndex, iconography
- Examples from [getdesign.md](https://getdesign.md/) (independent — not affiliated; [NOTICE.md](NOTICE.md))
- Documentation hub with Mermaid diagrams ([docs/INDEX.md](docs/INDEX.md))
