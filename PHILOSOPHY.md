# Philosophy

`.design` is the OpenAPI of product UI: a single, portable file that lets humans and AI agents share one visual contract — and keep it true as the product evolves.

## The problem

AI coding agents generate UI that looks plausible and is off-system underneath. They invent token names, drift on spacing within a session, forget decisions between sessions, and rebuild components that already exist. A static style guide does not fix this. A file that is never updated is worse than no file: stale guidance actively misleads the agent.

The durable fix is a **living contract in git** plus a **loop**: read → follow → update → verify.

## What `.design` is for

1. **Read** — Agents discover and load the file before generating or changing UI.
2. **Follow** — Tokens, components, constraints, and decisions are normative. Prose and intent explain *why*.
3. **Update** — As design progresses, agents edit the `.design` file in place (bump `version`, respect `locked` paths by asking first).
4. **Verify** — Drift against real CSS variables, Tailwind themes, and component inventories is detectable and repairable.

## Two audiences, one file

| Audience | Needs | Without it |
| --- | --- | --- |
| Agents | Exact allowed values, closed component inventories, when/when-not rules, forbidden behaviors, fallbacks | Invents colors, rebuilds Button, “almost right” spacing |
| Humans | Specific cultural reference, rationale, anti-examples, taste narrative | Token soup; adjective lists → generic UI |

Tokens are normative. `overview` and `intent.reference` carry judgment. Adjective lists (“modern, clean, premium”) describe a region; a specific reference (“Linear density with marketplace clarity”) describes a point.

Two more things belong in the contract because agents lose them between sessions: **words** (`voice` — register, casing, terminology, error style, applied with the same force as tokens) and **the committed aesthetic** (`intent.direction` names the direction, `intent.signature` names the one element where boldness concentrates). A recorded choice reads as intent; an unrecorded one decays into the model's default look.

## Process plus data

A `.design` file alone is data. Agents also need a **procedure**. This repository ships an Agent Skill (`skills/design/`) that encodes how to discover, load, apply, update, and verify the file. Every valid file may also include a short `agent.instructions` stub so a bare drop-in still works when the skill is not installed.

## Updating the contract

Keep the format simple: the file *is* the source of truth. When brand or components change, edit the YAML. Use `locked` for paths that require an explicit human ask before mutation. Use git for review and history — not an in-file proposal queue.

## Relationship to adjacent standards

- **[DESIGN.md](https://github.com/google-labs-code/design.md)** — Complementary identity document (markdown + YAML tokens). `.design` is a YAML file format with policy, lifecycle, and agent decision rules.
- **[W3C Design Tokens (DTCG)](https://www.designtokens.org/tr/2025.10/format/)** — Token *exchange*. `.design` sits above DTCG and can export to it; it does not replace it.
- **[AGENTS.md](https://agents.md/)** — How to work in the repo. Point it at `.design` for UI work.
- **[Agent Skills](https://agentskills.io/specification)** — How agents load procedural knowledge. The `design` skill is the procedure for this format.
- **[shadcn/ui](https://ui.shadcn.com/)** — Common agent codegen stack. `.design` orchestrates it via `integrations.shadcn` (CSS variables + `components.json`); it does not replace the library.
- **[getdesign.md](https://getdesign.md/)** — Public brand DESIGN.md analyses useful for bootstrap. Converted examples are independent analyses, not official kits.
- **Claude Design / Stitch / v0 / Lovable / Figma MCP** — Extraction, remix, and handoff products. `.design` is the repo-canonical twin they can sync to or from.

## What we refuse

- Binary or opaque formats agents cannot diff in PRs
- Folder packages as the primary unit (optional companions are fine; the contract is one file)
- Replacing decades of CSS / design-token work with a new rendering language
- Soft taste essays without measurable rules
- In-file proposal queues or changelogs that duplicate git

## Design progress is the point

Brands evolve. Components gain variants. Accents appear in marketing screens. Edit the contract, bump SemVer, open a PR. A static file is the floor. Keeping it current is the fix.
