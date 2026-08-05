# Ecosystem map

How `.design` fits the full design-to-code stack used by agents and humans in 2026.

## One contract, many surfaces

```mermaid
flowchart TB
  subgraph authoring ["Authoring"]
    FIG[Figma Variables / Tokens Studio]
    GMD[Google DESIGN.md]
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
  end

  subgraph runtime ["Runtime / codegen"]
    CSS[CSS custom properties]
    TW[Tailwind @theme / config]
    SH[shadcn/ui + components.json]
    IOS[iOS / Android resources]
    APP[Product UI]
  end

  FIG -->|integrations.figma sync| DES
  GMD -->|import| DES
  GET -->|convert| DES
  HUM -->|author| DES
  AG -->|points at| DES
  SK -->|READ FOLLOW UPDATE VERIFY| DES
  DES -->|exports.dtcg| DTCG
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
```

## What each layer owns

| Layer | Owns | Does not own |
| --- | --- | --- |
| Figma | Visual exploration, variable primitives | Agent when/when_not, git history |
| `.design` | Normative tokens, components, policy, rationale, themes | Binary fonts, full page trees |
| DTCG | Typed interchange (`$type` / `$value`) | Product taste / CTA rules |
| Style Dictionary | Multi-platform transforms | Brand judgment |
| shadcn | React primitives + CSS var theming | Brand system of record |
| AGENTS.md + skill | Procedure | Token values |

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
  A->>P: Follow tokens + components + shadcn
  A->>R: Update catalog when new pattern approved
  P->>R: Verify drift (CSS ↔ tokens ↔ themes)
```

## Field coverage checklist

A production-ready `.design` for the “entire ecosystem” typically includes:

- [ ] `tokens.color` / `typography` / `spacing` / `radius`
- [ ] `tokens.elevation` / `motion` / `breakpoint` / `iconography` (as needed)
- [ ] `themes.modes` for light/dark (or `omitted` with reason)
- [ ] `components` with DESIGN.md property bags + `when` / `when_not`
- [ ] `rationale.*` for prose agents need beyond hex
- [ ] `constraints` + `policy` + `decisions`
- [ ] `integrations.shadcn` **or** documented non-shadcn stack
- [ ] `integrations.figma` when Figma is source
- [ ] `exports` paths for DTCG/CSS/Tailwind CI
- [ ] `assets` path refs for logo/fonts
- [ ] `locked` on brand-critical paths
- [ ] `AGENTS.md` pointer + installed `design` skill

Normative detail: [SPEC.md](../SPEC.md) §7–§13B · [design-md-mapping.md](design-md-mapping.md) · [shadcn.md](shadcn.md).
