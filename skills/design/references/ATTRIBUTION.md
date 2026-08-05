# Attribution — craft sources

The `design` skill’s procedure (discover → read → follow → update → verify) is original to AgentsORG DESIGN.

The **craft bar** in [CRAFT.md](CRAFT.md) and the **review triage** in [REVIEW.md](REVIEW.md) were distilled from private design-engineering Agent Skills developed for AI UI work (commonly kept under a project’s `.agents/skills/`), including patterns aligned with:

| Theme | Source skill (local aiforui pack) |
| --- | --- |
| Hierarchy, spacing, type, color, IA, copy | `design-foundations` |
| Review method, escalation triggers, verdict shape | `ui-review` |
| Motion timing / GPU props / reduced motion | `animations` |
| Nested radii, borders, shadows, dark surfaces | `surfaces` |
| Tap targets, hover gating, focus | `touch-and-accessibility` |
| Composition-first component APIs | `component-design` |

Those packs draw heavily on **Emil Kowalski’s design-engineering practice** (see [animations.dev](https://animations.dev/)). This repository does **not** vendor-copy those skill trees; it absorbs durable defaults so a single portable `design` skill remains self-contained for [skills.sh](https://skills.sh/).

Project `.design` contracts always override CRAFT defaults.
