# design skill

[![skills.sh](https://skills.sh/b/AgentsORG/DESIGN)](https://skills.sh/AgentsORG/DESIGN)

Agent Skill for the AgentsORG [`.design`](https://github.com/AgentsORG/DESIGN) living visual contract.

## Install

```bash
npx skills add AgentsORG/DESIGN --skill design
```

Or copy `skills/design/` into your repo at `.agents/skills/design/`.

Compatible with agents listed on [skills.sh/agent](https://www.skills.sh/agent/) via the [Agent Skills](https://agentskills.io/specification) standard.

## Pair with a file

Drop `.design` (or `product.design`) at your repo root. Start from a [getdesign.md](https://getdesign.md/)-sourced example:

```bash
cp examples/vercel.design ./.design
```

See [docs/drop-in.md](../../docs/drop-in.md) and [docs/shadcn.md](../../docs/shadcn.md).

## What it does

Teaches agents to **discover → read → follow → update → verify** the contract so UI stays on-brand and the file evolves with design progress.

When the contract is silent, agents apply the craft bar in [references/CRAFT.md](references/CRAFT.md) (hierarchy, surfaces, motion, a11y). When `integrations.shadcn` is enabled, agents apply CSS variables and prefer shadcn components.

| Reference | Role |
| --- | --- |
| [SKILL.md](SKILL.md) | Procedure |
| [references/CRAFT.md](references/CRAFT.md) | Design-engineering defaults |
| [references/REVIEW.md](references/REVIEW.md) | Critique / verify |
| [references/ATTRIBUTION.md](references/ATTRIBUTION.md) | Craft source credits |
