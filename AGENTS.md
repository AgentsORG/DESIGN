# AGENTS.md

Guidance for coding agents working on the AgentsORG DESIGN specification repository.

## Project

This repo defines the **`.design` file format** (design.v1): a living visual contract for AI design, plus a portable Agent Skill, shadcn/ui integration, and getdesign.md-sourced examples.

- Normative spec: [SPEC.md](SPEC.md)
- Philosophy: [PHILOSOPHY.md](PHILOSOPHY.md)
- Schema: [schema/design.v1.schema.json](schema/design.v1.schema.json)
- Skill: [skills/design/](skills/design/)
- Docs: [docs/INDEX.md](docs/INDEX.md)
- Examples: [examples/](examples/) (from [getdesign.md](https://getdesign.md/))

## Design (meta)

When editing format docs or examples, treat [SPEC.md](SPEC.md) as source of truth. Examples are independent brand analyses — not affiliated with those companies. Prefer [examples/vercel.design](examples/vercel.design) as the default teaching sample.

## How to change the format

1. Update `SPEC.md` first (normative).
2. Keep `schema/design.v1.schema.json` in sync.
3. Update `skills/design/` references if procedure changes.
4. Refresh examples (`python scripts/convert_getdesign.py` or hand-edit).
5. Keep `docs/` diagrams accurate (especially shadcn + discovery).
6. Note breaking changes clearly; bump documented schema only with a new `design.vN` when breaking.

## Do not

- Edit plan files under `.cursor/plans` as part of normal work
- Invent a parallel token graph that conflicts with SPEC.md
- Reintroduce `proposed_changes` / in-file history blocks
- Commit secrets
- Claim examples are official brand design systems

## Commits / PRs

Prefer clear, focused commits: spec, schema, skill, examples, or docs. Do not push to GitHub unless the user explicitly asks.
