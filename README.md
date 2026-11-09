<p align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/agents-dark-bg.svg">
    <img src="docs/brand/agents-light-bg.svg" alt="agents.org.in" height="56">
  </picture>
</p>

# `.DESIGN` — a living visual contract for AI agents

[![skills.sh](https://skills.sh/b/AgentsORG/DESIGN)](https://skills.sh/AgentsORG/DESIGN)
[![Release](https://img.shields.io/github/v/release/AgentsORG/DESIGN)](https://github.com/AgentsORG/DESIGN/releases)
[![Schema](https://img.shields.io/badge/schema-design.v1-0B57D0.svg)](SPEC.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

```bash
npx skills add AgentsORG/DESIGN --skill design
npx skills add AgentsORG/design-engineering
```

One file holds your product's design: tokens, components and when to use them, the voice of every label, what is locked, and the instructions an agent needs to follow it. Name it after the system it describes (`campusbinge.DESIGN`, `relay.DESIGN`), commit it, and every agent that touches your UI builds from the same contract. It is YAML, readable in a pull request, and it carries its own `agent.instructions`, so it works even when no skill is installed: drop it in the repo or drag it into a chat.

![Claude Code is asked to build the pricing page from relay.DESIGN. It reads the file (design.v1, relay 1.3.0, 3 locked paths), says it is following the file's agent.instructions, and writes app/pricing/page.tsx with 0 raw hex, 0 invented spacing, and Button and Card from the catalog. A card beside it lists what the build bound to: color.primary #0B57D0 (locked), radius.md 10, spacing.unit 4, voice.casing sentence](docs/readme/img/ds-drop.png)

## Best with design-engineering

`.DESIGN` says **what** your design is. [design-engineering](https://github.com/AgentsORG/design-engineering) knows **how** good UI is built: easing and timing, states, focus, contrast, type, the review checklist, the tells that make a screen look generated. Install both. design-engineering reads the project's `.DESIGN` before anything else and ranks it above its own defaults, so a review separates the two kinds of finding: drift from your contract, and craft the contract is silent on.

![Claude Code running /design-engineering review on app/pricing/page.tsx. It names its contract, relay.DESIGN, which outranks its defaults, then three findings as Before (−), After (+) and Why: a raw #2563eb replaced by var(--color-primary) because tokens.color.primary is locked in relay.DESIGN; "Start Free Trial" changed to "Start free trial" for voice.casing sentence; and transition all .3s ease-in replaced by a named transform transition on the enter easing, citing design-engineering's easing-curves node. Verdict: ship after these three](docs/readme/img/ds-pair.png)

| Job | Owner |
| --- | --- |
| Colours, type, spacing, radii, motion values, components and when to use them, voice, what is locked | your `.DESIGN` file |
| Discover, read, follow, update and verify the file | the `design` skill in this repo |
| Everything the file is silent on, and the review | design-engineering |

## The file

A `.DESIGN` file is the contract, not a mood board. Tokens are normative and referenced by path; components say when to use them and when not to; `locked` lists what an agent must ask about before changing; `voice` governs every label and error. The required `agent.instructions` teach an agent four verbs: read the normative core first, follow it, update the file in place, verify the code against it.

![relay.DESIGN open in an editor: schema design.v1, color tokens with primary #0B57D0, radius sm 6 md 10 pill 9999, tokens.color.primary under locked, a button component with when and when_not, and voice casing sentence. A card names the required agent.instructions and its four verbs: Read the normative core first; Follow tokens, components and voice; Update in place and ask on a locked path; Verify drift by token group](docs/readme/img/ds-contract.png)

| Layer | Contents |
| --- | --- |
| **Agent** | `agent.instructions` (required): the file teaches itself on drop-in |
| **Identity** | `name`, `version`, `status`, `overview`, `intent` (direction, signature, treatment), `themes` |
| **System** | `tokens` (nestable groups: color, type, space, radius, elevation, motion, background, sound), `components`, `patterns`, `locked`, `assets` |
| **Voice** | The UI copy contract: register, casing, terminology, error style |
| **Rationale** | DESIGN.md body prose (`rationale.*`) |
| **Rules** | `policy`, `decisions`, `constraints`, `examples` |
| **Integrations** | `shadcn` (styles, bases, registries, MCP), `figma` |
| **Exports** | DTCG, CSS, Tailwind v4, shadcn registry item, HyperFrames `frame.md`, Style Dictionary, native |
| **Targets** | `web`, single-file artifacts, `video` (aspect, fps, delivery loudness) |

Lifecycle: `bootstrap` → `refine` → `lock` → `evolve`. History lives in git.

### Naming

| Form | Use |
| --- | --- |
| `<name>.DESIGN` | The usual form: one file named after its system, e.g. `campusbinge.DESIGN`. Capitals make it stand out beside `README.md` and `AGENTS.md` |
| `.design` | A bare, unnamed file at a repository or package root |

The extension is matched case-insensitively, so `campusbinge.design` also works. Agents look for the nearest file walking up from the code they are editing; with several named files in one folder they ask which one to use ([SPEC §2, §4](SPEC.md#2-media-type-and-filenames)).

## One file, every format

The file stays normative; everything else is generated from it. The reference exporter writes the CSS variables, a Tailwind v4 `@theme`, DTCG tokens, a shadcn registry theme and a HyperFrames `frame.md` for video, each to the path its `exports` section names.

![A terminal running python scripts/export_design.py relay.DESIGN, which wrote css to src/styles/tokens.css, tailwind to tailwind.theme.css, dtcg to tokens/tokens.json, shadcn_registry to registry/brand-theme.json and frame_md to frame.md. A card shows the start of tokens.css, generated and never edited: --color-primary #0B57D0, --color-on-primary #FFFFFF, --color-surface-base #F8FAFC, --radius-md 10px, --spacing-md 16px](docs/readme/img/ds-exports.png)

It imports [Google's DESIGN.md](https://github.com/google-labs-code/design.md) without loss ([mapping](docs/design-md-mapping.md)), orchestrates [shadcn/ui](https://ui.shadcn.com/) rather than replacing `components.json` ([shadcn](docs/shadcn.md)), and bootstraps from a [getdesign.md](https://getdesign.md/) brand analysis ([pipeline](docs/getdesign.md)).

## Quick start

**1. Add a file.** Start from the annotated template, where every section is explained, or from a brand analysis:

```bash
cp templates/starter.DESIGN ./campusbinge.DESIGN
# or: cp examples/vercel.DESIGN ./campusbinge.DESIGN
```

**2. Point your agents at it**, in `AGENTS.md` (or just drag the file into a chat):

```markdown
## Design
Before UI work, read `./campusbinge.DESIGN` (or activate the `design` skill).
Obey `agent.instructions` in that file. Ask before changing `locked` paths.
```

**3. Install the skills** for the full procedure and the craft review:

```bash
npx skills add AgentsORG/DESIGN --skill design
npx skills add AgentsORG/design-engineering
```

**4. Check and export** with the reference tooling (Python 3 with PyYAML and jsonschema):

```bash
python scripts/lint_design.py                                   # schema + SPEC §19 lint over the repo's files
python scripts/export_design.py campusbinge.DESIGN              # every artifact under `exports`
python scripts/diff_design.py old.DESIGN new.DESIGN --fail-on-regression
```

## Examples

Independent analyses of public sites, converted from getdesign.md: **not affiliated** with those brands ([NOTICE.md](NOTICE.md)).

| File | Reference |
| --- | --- |
| [vercel.DESIGN](examples/vercel.DESIGN) | getdesign.md/vercel |
| [stripe.DESIGN](examples/stripe.DESIGN) | getdesign.md/stripe |
| [notion.DESIGN](examples/notion.DESIGN) | getdesign.md/notion |
| [apple.DESIGN](examples/apple.DESIGN) | getdesign.md/apple |
| [linear.DESIGN](examples/linear.DESIGN) | getdesign.md/linear.app |
| [supabase.DESIGN](examples/supabase.DESIGN) | getdesign.md/supabase |

## Documentation

| Doc | Topic |
| --- | --- |
| [SPEC.md](SPEC.md) | The normative design.v1 specification |
| [docs/INDEX.md](docs/INDEX.md) | The docs hub |
| [docs/self-contained.md](docs/self-contained.md) | In-file agent instructions |
| [docs/overview.md](docs/overview.md) | System map and diagrams |
| [docs/ecosystem.md](docs/ecosystem.md) | Figma → DTCG → CSS → agents |
| [docs/design-md-mapping.md](docs/design-md-mapping.md) | DESIGN.md field parity |
| [docs/shadcn.md](docs/shadcn.md) | shadcn/ui integration |
| [docs/getdesign.md](docs/getdesign.md) | The getdesign.md pipeline |
| [docs/motion-media.md](docs/motion-media.md) | Sound tokens, video targets, HyperFrames `frame.md` |

## Status

**design.v1**, contract **1.3** ([CHANGELOG](CHANGELOG.md)): voice, committed intent, nested tokens, sound tokens and video targets, the current shadcn model and registry export, the HyperFrames `frame.md` export, companion-skill routing (design-engineering, impeccable, HyperFrames, ElevenLabs), the annotated starter, and reference tooling for [lint](scripts/lint_design.py), [export](scripts/export_design.py) and [diff](scripts/diff_design.py), all run in CI. A packaged CLI is planned.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Security: [SECURITY.md](SECURITY.md).

The stills on this page are faux product UI built with [Stageshow](https://benji.org/stageshow) (MIT, Benji Taylor). The scenes and how to re-film them are in [docs/readme/stage/](docs/readme/stage/README.md).

## License

[MIT](LICENSE) © AgentsORG
