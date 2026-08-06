# Changelog

All notable changes to the `.design` format and this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project uses SemVer for the **contract schema** (`design.v1`, future `design.v2`).

## [Unreleased]

## [1.1.0] — 2026-08-06

### Added

- `voice` — UI copy contract (register, casing, terminology map, action naming, error style) (SPEC §13C)
- `intent.direction`, `intent.signature`, `intent.treatment` — committed aesthetic direction, boldness budget, utilitarian/editorial register; `patterns.<name>.treatment` per-surface override
- Nested token groups (depth ≤ 20) with full dot-path references; token→token reference chains (depth ≤ 10)
- `targets` object form with environment constraints (`external_assets`, `single_file`)
- Reading tiers for large files (SPEC §8.1)
- `themes.single` declaration; designed-not-inverted mode rule; CSS mode-emission strategy (`exports.css.mode_strategy`)
- shadcn: `base` / `icon_library` / `preset`, `registries` (+ never-guess rule), `components` install list, `mcp` hint, full current variable set (`chart-1…5`, `sidebar-*`), `css_vars.theme` mode-independent key, Tailwind v4 `@theme inline` rule
- `exports.shadcn_registry` (registry:theme item), `exports.tailwind` v3, `exports.css.prefix`
- Constraint-authoring guidance (SPEC §16.1); expanded validation table (collisions, token-like unknown keys, missing primary/typography, section order)
- Skill: treatment calibration, plan → critique → confirm → write bootstrap, adjacent-signal scanning, post-generation self-check, tiered reading
- CRAFT bar: major expansion — typography/color-scale/surface numbers, iconography & illustration, gestures & direct manipulation, performance, information architecture, default-looks-to-avoid catalogue
- Typography `fontFamily` stacks / `fallbacks`; `tokens.background` atmosphere group (gradients, mesh, noise)
- `policy.color.accent_cycle` (ordered decorative accent rotation); `decisions.*` generalized beyond components (token-role rules such as `decisions.typography`)
- Verify reports added/removed/modified per token group plus a regression flag
- Canonical `agent.instructions` template covers voice, treatment, signature, and tiered reading (SPEC §8, docs, converter, examples)
- Examples now carry `intent.direction`/`signature`, `voice`, sidebar/chart CSS variables, and `css_vars.theme`
- `templates/starter.design` — annotated kitchen-sink template exercising every major section (linted in CI)
- Linter: WCAG contrast checks (component bags + shadcn fg/bg pairs), alias-collision detection, orphan-token summary, instruction-duty coverage
- CI: schema validation of all examples + format lint rules + banned-reference leak guard; `.gitattributes` line-ending normalization

### Fixed

- Schema: flat DESIGN.md component property bags now validate (`anyOf`); inline typography objects and boolean scalars accepted; `variants` ⇒ `when`/`when_not` enforced
- Schema: typed `tokens.breakpoint` / `opacity` / `zIndex` / `iconography`; nested `spacing`/`radius`/`color`
- `agent` documented as required consistently (SPEC §7 / §24, schema, summary)
- Broken relative links in the skill's SPEC-SUMMARY
- Example hygiene: real brand names throughout, `sources` URL types, no placeholder elevation tokens

## [1.0.0] — 2026-08-05

### Added

- Normative **design.v1** specification ([SPEC.md](SPEC.md))
- JSON Schema ([schema/design.v1.schema.json](schema/design.v1.schema.json)) — requires `agent.instructions`
- **Self-contained files** — every `.design` teaches READ → FOLLOW → UPDATE → VERIFY on drag-drop ([docs/self-contained.md](docs/self-contained.md))
- Portable Agent Skill (`skills/design/`) with CRAFT bar + REVIEW critique checklist
- Google DESIGN.md parity: tokens, component property bags, full `rationale.*`, `omitted`
- Integrations: `shadcn`, `figma`; `themes`, `exports`, `assets`
- Token groups: color, typography, spacing, radius, elevation, motion, breakpoint, opacity, zIndex, iconography
- Examples from [getdesign.md](https://getdesign.md/) (independent — not affiliated; [NOTICE.md](NOTICE.md))
- Documentation hub with Mermaid diagrams ([docs/INDEX.md](docs/INDEX.md))
