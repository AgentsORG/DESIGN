# `.design` — Living Visual Contract for AI Design

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Schema](https://img.shields.io/badge/schema-design.v1-0B57D0.svg)](SPEC.md)
[![skills.sh](https://skills.sh/b/AgentsORG/DESIGN)](https://skills.sh/AgentsORG/DESIGN)
[![Release](https://img.shields.io/github/v/release/AgentsORG/DESIGN)](https://github.com/AgentsORG/DESIGN/releases)

**A self-contained visual contract you can drop into any repo — or drag into any agent.**  
YAML file + portable skill. Agents read it, follow it, and update it as design progresses. No skill install required for basic use: every file carries its own `agent.instructions`.

Maintained by [AgentsORG](https://www.agents.org.in/) · Spec: [SPEC.md](SPEC.md) · Docs: [docs/INDEX.md](docs/INDEX.md)

```bash
npx skills add AgentsORG/DESIGN --skill design
cp examples/vercel.design ./.design
# or: drag any *.design into your agent — it teaches itself via agent.instructions
```

## About

`.design` is the **OpenAPI of product UI**: one machine-readable file that is also human-auditable in git. It unifies what agents otherwise invent session-to-session — tokens, components, taste rationale, and decision rules — into a living contract.

| Problem | What `.design` does |
| --- | --- |
| Agents invent off-brand hex and rebuild Button | Normative `tokens` + `components` with when/when_not |
| Style guides go stale | Edit the file in place; git is history |
| DESIGN.md prose lost on import | Full `rationale.*` + property bags |
| Skill not installed | Required `agent.instructions` — drag-drop still works |
| shadcn / Figma / DTCG drift | `integrations` + `exports` + `themes` |

Superset of [Google DESIGN.md](https://github.com/google-labs-code/design.md). Orchestrates [shadcn/ui](https://ui.shadcn.com/). Bootstraps from [getdesign.md](https://getdesign.md/). Works with every [skills.sh](https://www.skills.sh/agent/) agent.

## Ecosystem

```mermaid
flowchart LR
  FIG[Figma] --> DES[".design"]
  GMD[DESIGN.md] --> DES
  GET[getdesign.md] --> DES
  DES --> DTCG[DTCG export]
  DES --> SH[shadcn theme]
  DES --> APP[Product UI]
  SK[design skill] --> DES
  SK --> APP
  DTCG --> CSS[CSS / Tailwind / native]
  CSS --> APP
```

Full map: [docs/ecosystem.md](docs/ecosystem.md) · Self-contained drop-in: [docs/self-contained.md](docs/self-contained.md).

## Architecture

```mermaid
flowchart TB
  subgraph contract [".design — design.v1"]
    AG[agent.instructions — self-teach]
    ID[identity / intent / status / themes]
    TOK[tokens + elevation + breakpoints]
    COMP[components / patterns]
    RAT[rationale — DESIGN.md prose]
    RULES[policy / decisions / constraints]
    INT[integrations: shadcn · figma]
    EXP[exports · assets]
  end

  subgraph agents ["Agents"]
    SKILL[design skill + CRAFT]
    DROP[drag-drop / @file only]
  end

  subgraph runtime ["Runtime"]
    CSS[globals.css]
    UI[UI components]
  end

  DROP -->|agent.instructions| contract
  SKILL -->|discover + read| contract
  SKILL -->|follow| UI
  DROP -->|follow| UI
  INT --> CSS
  TOK --> CSS
  CSS --> UI
  SKILL -->|update in place| contract
```

## Quick start

### 1. Drop a file in your repo

```bash
cp examples/vercel.design ./.design
```

Examples are independent visual analyses — **not affiliated** with those brands ([NOTICE.md](NOTICE.md)). Adapt to your product. Every example includes full `agent.instructions`.

### 2. Point agents at it (or drag the file)

Add to `AGENTS.md`:

```markdown
## Design
Before UI work, read `./.design` (or activate the `design` skill).
Obey `agent.instructions` in that file. Ask before changing `locked` paths.
```

### 3. Optional — install the skill (enriched CRAFT + review)

```bash
npx skills add AgentsORG/DESIGN --skill design
```

### 4. Optional — shadcn / Figma / exports

See [docs/shadcn.md](docs/shadcn.md), [docs/ecosystem.md](docs/ecosystem.md), and SPEC §7.2–§7.5.

## What’s in a `.design` file

| Layer | Contents |
| --- | --- |
| **Agent** | `agent.instructions` (required) — self-teach on drop-in |
| **Identity** | `name`, `version`, `status`, `overview`, `intent`, `themes` |
| **System** | `tokens`, `components`, `patterns`, `locked`, `assets` |
| **Rationale** | DESIGN.md body prose (`rationale.*`) |
| **Rules** | `policy`, `decisions`, `constraints`, `examples` |
| **Integrations** | `shadcn`, `figma` |
| **Exports** | DTCG, CSS, Tailwind, Style Dictionary, native |

Lifecycle: `bootstrap` → `refine` → `lock` → `evolve`. History lives in **git**.

## Documentation

| Doc | Topic |
| --- | --- |
| [docs/INDEX.md](docs/INDEX.md) | Full docs hub |
| [docs/self-contained.md](docs/self-contained.md) | In-file agent instructions |
| [docs/overview.md](docs/overview.md) | System map + diagrams |
| [docs/ecosystem.md](docs/ecosystem.md) | Figma → DTCG → CSS / agents |
| [docs/design-md-mapping.md](docs/design-md-mapping.md) | DESIGN.md field parity |
| [docs/shadcn.md](docs/shadcn.md) | shadcn/ui integration |
| [docs/getdesign.md](docs/getdesign.md) | getdesign.md pipeline |
| [SPEC.md](SPEC.md) | Normative design.v1 |

## Examples

| File | Reference |
| --- | --- |
| [vercel.design](examples/vercel.design) | getdesign.md/vercel |
| [stripe.design](examples/stripe.design) | getdesign.md/stripe |
| [notion.design](examples/notion.design) | getdesign.md/notion |
| [apple.design](examples/apple.design) | getdesign.md/apple |
| [linear.design](examples/linear.design) | getdesign.md/linear.app |
| [supabase.design](examples/supabase.design) | getdesign.md/supabase |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Security: [SECURITY.md](SECURITY.md).

## Status

**design.v1** — released. Format, schema, self-contained files, skill + CRAFT, integrations, examples, docs. CLI (`lint`, `diff`, `verify`, `export`) planned.

## License

[MIT](LICENSE) © AgentsORG
