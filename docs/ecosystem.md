# Ecosystem map

How `.design` fits the full design-to-code stack used by agents and humans in 2026.

## One contract, many surfaces

```mermaid
flowchart TB
  subgraph authoring ["Authoring"]
    FIG[Figma Variables / Tokens Studio]
    GMD["Google DESIGN.md — file + CLI"]
    GET[getdesign.md analyses]
    HUM[Human / design lead]
  end

  subgraph canonical ["Repo canonical"]
    DES[".design — design.v1"]
    SK[design Agent Skill]
    AG[AGENTS.md]
  end

  subgraph interchange ["Interchange"]
    DTCG[DTCG tokens.json]
    SD[Style Dictionary]
    REG["shadcn registry item — exports.shadcn_registry"]
  end

  subgraph craft ["Craft skills — procedure below the contract"]
    DE["design-engineering — skill graph, subagents, /design-engineering router"]
    IMP["impeccable — 23 named passes"]
  end

  subgraph runtime ["Runtime / codegen"]
    CSS[CSS custom properties]
    TW[Tailwind @theme / config]
    SH["shadcn/ui + components.json + MCP"]
    IOS[iOS / Android resources]
    APP[Product UI]
    HF["HyperFrames frame.md — video"]
    SFX["assets.sounds — generated audio"]
  end

  FIG -->|integrations.figma sync| DES
  GMD -->|"import — lossless (0.4.0)"| DES
  GET -->|convert| DES
  HUM -->|author| DES
  AG -->|points at| DES
  SK -->|READ FOLLOW UPDATE VERIFY| DES
  DES -->|exports.dtcg| DTCG
  DES -->|exports.shadcn_registry| REG
  REG -->|shadcn CLI install| SH
  DTCG --> SD
  SD --> CSS
  SD --> TW
  SD --> IOS
  DES -->|integrations.shadcn| SH
  DES -->|themes + tokens| CSS
  CSS --> APP
  TW --> APP
  SH --> APP
  IOS --> APP
  SK --> APP
  DES -->|exports.frame_md| HF
  DES -->|tokens.sound.material prompts| SFX
  SK -->|routes named jobs| DE
  SK -->|routes named jobs| IMP
  DE -->|craft where the file is silent| APP
  IMP -->|polish / critique passes| APP
```

## What each layer owns

| Layer | Owns | Does not own |
| --- | --- | --- |
| Figma | Visual exploration, variable primitives | Agent when/when_not, git history |
| Google DESIGN.md (file + CLI) | MD+YAML brand identity docs, incl. CLI-maintained analyses (0.4.0) | Policy, lifecycle, voice — gained on lossless import into `.design` |
| `.design` | Normative tokens, components, policy, voice, rationale, themes | Binary fonts, full page trees |
| `design` skill + CRAFT | Procedure + craft bar when contract is silent | Brand-specific tokens (those live in `.design`) |
| DTCG | Typed interchange (`$type` / `$value`) | Product taste / CTA rules |
| Style Dictionary | Multi-platform transforms | Brand judgment |
| shadcn | React primitives, CSS var theming, styles + `base` choice, namespaced registries, MCP server | Brand system of record |
| shadcn registry item (`exports.shadcn_registry`) | Distributable `registry:theme` payload derived from `css_vars` | Normative tokens (those stay in `.design`) |
| HyperFrames `frame.md` (`exports.frame_md`) | Video-frame companion: brand tokens plus `motion` and `sound` groups, read ahead of `design.md` / `DESIGN.md` inside a video project | Composition, beats, layout — the frame author's |
| AgentsORG `design-engineering` | Craft knowledge graph (motion, sound, typography, anti-tells) and the `/design-engineering` router that hands jobs to the right skill; applies only where `.design` is silent | Brand tokens, contract precedence |
| impeccable | Named polish / critique / audit passes (`/impeccable polish`, `critique`, `typeset`, …); may write a DESIGN.md that imports losslessly | Being the source of truth — `.design` outranks the DESIGN.md it produces |
| Audio generation (ElevenLabs sound-effects, open-weight, CC0) | The files `assets.sounds` points at, prompted by `tokens.sound.material` | Level, length, toggle default — those are `tokens.sound` |
| AGENTS.md | Repo pointer / install hint | Token values |

## Skill layers

```mermaid
flowchart TB
  DES[".design contract — normative"]
  SK[design skill procedure]
  CR[CRAFT.md defaults]
  GEN[Generic taste skills]
  DES --> SK
  SK --> CR
  CR --> GEN
```

Precedence: user prompt → nearest `.design` → design skill (procedure + CRAFT) → generic taste skills → model defaults.

## Recommended team pipeline

```mermaid
sequenceDiagram
  participant D as Designer
  participant F as Figma
  participant R as .design in git
  participant A as Coding agent
  participant P as Product UI

  D->>F: Adjust variables / modes
  D->>R: Sync primitives + update rationale
  Note over R: PR review — tokens + constraints
  A->>R: Discover nearest .design
  A->>P: Follow tokens + components + voice + shadcn
  A->>R: Update catalog when new pattern approved
  A->>R: Verify drift (CSS ↔ tokens ↔ themes) — added / removed / modified + regression flag
```

## Field coverage checklist

A production-ready `.design` for the “entire ecosystem” typically includes:

- [ ] `agent.instructions` (required — the file self-teaches on drop-in)
- [ ] `intent` with `reference`, `direction`, `signature`, `treatment`
- [ ] `voice` — register, casing, terminology, action naming, error style
- [ ] `tokens.color` / `typography` / `spacing` / `radius`
- [ ] `tokens.elevation` / `motion` / `breakpoint` / `iconography` / `background` (as needed)
- [ ] `tokens.sound` with `enabled: false` — or `omitted: [tokens.sound]` so silence is a decision
- [ ] `targets` entry for `video` (aspect, fps, loudness) and `exports.frame_md` when launch films or reveals are produced
- [ ] `themes.modes` for light/dark (or `themes.single` / `omitted` with reason)
- [ ] `components` with DESIGN.md property bags + `when` / `when_not`
- [ ] `rationale.*` for prose agents need beyond hex
- [ ] `constraints` + `policy` + `decisions`
- [ ] `integrations.shadcn` **or** documented non-shadcn stack
- [ ] `integrations.figma` when Figma is source
- [ ] `exports` paths for DTCG / CSS / Tailwind / shadcn registry CI
- [ ] `assets` path refs for logo/fonts
- [ ] `locked` on brand-critical paths
- [ ] `AGENTS.md` pointer + installed `design` skill

Normative detail: [SPEC.md](../SPEC.md) §7–§13B · [design-md-mapping.md](design-md-mapping.md) · [shadcn.md](shadcn.md).
