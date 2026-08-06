# SPEC-SUMMARY — design.v1 field map

Normative detail: [SPEC.md](../../../SPEC.md). Schema: [schema/design.v1.schema.json](../../../schema/design.v1.schema.json).

## Required

| Field | Purpose |
| --- | --- |
| `schema` | MUST be `design.v1` |
| `name` | System id |
| `version` | SemVer of the contract |
| `agent.instructions` | Self-contained drop-in procedure |

## Canonical (follow + update in place)

| Field | Purpose |
| --- | --- |
| `status` | `bootstrap` \| `refine` \| `lock` \| `evolve` |
| `overview` | Specific reference narrative |
| `intent.reference` | Required if `intent` present |
| `intent.direction` / `signature` / `treatment` | Committed aesthetic, boldness budget, register |
| `voice` | UI copy contract: register, casing, terminology, errors |
| `tokens` | Normative color/type/spacing/radius/motion (groups may nest; full dot-path refs) |
| `locked` | Dot-paths that require ask before edit |
| `components` | Catalog + when/when_not + variants |
| `patterns` | Composition recipes |
| `policy` | hierarchy, reuse, if_missing, a11y |
| `decisions` | if → then trees |
| `constraints` | always / never |
| `examples` | good/bad refs |
| `sources` | Extraction provenance |
| `extends` | Parent `.design` files |
| `integrations.shadcn` | Optional shadcn bridge: style, aliases, css_vars, map_from_tokens |
| `integrations.figma` | Optional Figma file/modes/sync direction |
| `themes` | Named modes overlaying tokens (light/dark/…) |
| `exports` | DTCG / CSS / Tailwind / Style Dictionary / native paths |
| `assets` | Logo / font path references (no binaries) |
| `rationale` | DESIGN.md body prose: colors, typography, layout, elevation, shapes, components, dos/donts |
| `omitted` | Intentionally missing sections |

## Components (DESIGN.md parity)

Property bags MUST support: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width` (aliases: `background`, `foreground`, `radius`). Variants MAY be nested under `tokens` or flat sibling keys (`button-primary-hover`). Bind every listed property when implementing.

Craft defaults when silent: [CRAFT.md](CRAFT.md). See [docs/design-md-mapping.md](../../../docs/design-md-mapping.md).

## Not in the format

Do **not** add `ops`, `proposed_changes`, or `history`. Use git for change history.

## Discovery

Nearest `.design` / `*.design` walking up from edited path; root fallback; nearest wins.

## Precedence

User prompt > nearest `.design` > `design` skill > generic taste skills > model defaults.
