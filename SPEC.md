# `.design` Format Specification

**Status:** design.v1  
**Organization:** [AgentsORG](https://www.agents.org.in/)  
**License:** MIT  

This document is the normative specification for the `.design` file format: a living visual contract that agents **read**, **follow**, and **update** as design progresses.

Companion documents: [PHILOSOPHY.md](PHILOSOPHY.md), [docs/research.md](docs/research.md), [schema/design.v1.schema.json](schema/design.v1.schema.json), [skills/design/](skills/design/).

---

## 1. Overview

A `.design` file is a single text document that represents a JSON object, authored preferably as YAML 1.2 (JSON serialization is equally valid). It defines the visual identity and decision rules of a product so that humans and AI agents can reconstruct and evolve the UI language consistently.

The file is the source of truth. Agents **follow** it when generating UI and **edit it in place** when the design system changes. Version history belongs in git — not inside the file.

Tokens and structured rules are **normative**. Prose fields (`overview`, component `when`/`when_not`, constraint strings) provide context and judgment.

---

## 2. Media type and filenames

| Form | Usage |
| --- | --- |
| `.design` | Preferred at repository or package root |
| `<name>.design` | Named systems (e.g. `agents.design`, `linear.design`) |
| JSON serialization | Same object shape; useful for tooling pipelines |

Recommended media type: `application/design+yaml` (informational; not yet IANA-registered).

---

## 3. Schema declaration

Every file MUST include:

```yaml
schema: design.v1
```

Consumers that do not recognize the schema version SHOULD warn when following and MUST NOT perform write operations they cannot safely preserve (see §23).

Optional JSON Schema reference:

```yaml
$schema: https://raw.githubusercontent.com/AgentsORG/DESIGN/main/schema/design.v1.schema.json
```

---

## 4. Discovery

Agents MUST discover the active design file as follows:

1. Starting from the path being edited (or the working directory), walk upward toward the repository root.
2. At each directory, if exactly one of `.design` or a single `*.design` exists, select it. If both `.design` and other `*.design` files exist, prefer `.design`. If multiple `*.design` files exist and no `.design`, the agent MUST ask which to use (or follow an explicit user path).
3. If none is found at the repository root, the agent SHOULD offer to bootstrap a new file rather than inventing an untracked system.
4. Nested package files win over parent files (**nearest wins**), matching AGENTS.md conventions.

### 4.1 Extends resolution

```yaml
extends:
  - ./base.design
  - material3.design
```

- Resolve left to right (bases first), then apply the current file as the final overlay.
- Child values override parent values for the same key path.
- Circular `extends` graphs MUST be rejected as an error.
- Remote or registry extends MAY be supported by tooling; v1 requires local path or same-directory name resolution at minimum.

---

## 5. Precedence

### 5.1 When generating or reviewing UI

1. Explicit user chat instructions for the current task  
2. Fields of the nearest `.design` file  
3. Installed `design` Agent Skill procedure  
4. Other design-related skills (generic taste / frontend-design)  
5. Model defaults  

### 5.2 When updating the `.design` file

1. Explicit user instruction to update, remix, lock, or unlock  
2. `status` and `locked` rules in this specification  
3. Agents MUST ask before changing paths listed in `locked`  
4. Meaningful edits SHOULD bump `version` (SemVer)  

---

## 6. Lifecycle states

```text
bootstrap → refine → lock → evolve
```

| `status` | Meaning | Agent update behavior |
| --- | --- | --- |
| `bootstrap` | Extracted or scaffolded draft; not yet trusted | May fill draft fields freely; SHOULD populate `sources`; SHOULD NOT set `locked` yet |
| `refine` | Actively shaped by humans and agents | MAY edit unlocked fields; MUST ask before changing `locked` paths |
| `lock` | Released contract; brand stability required | MUST ask before any edit to `locked` paths; additive unlocked fields OK with care |
| `evolve` | Post-release iteration | Edit unlocked freely; MAJOR (breaking) changes require user confirmation |

Entry-level substates MAY appear on components or patterns: `experimental`, `deprecated`.

---

## 7. Top-level object

Required:

| Field | Type | Description |
| --- | --- | --- |
| `schema` | string | MUST be `design.v1` |
| `name` | string | Short system identifier |
| `version` | string | SemVer of the contract (e.g. `1.4.0`) |
| `agent` | object | MUST contain `instructions` (§8) so the file is self-contained |

Recommended:

| Field | Type | Description |
| --- | --- | --- |
| `status` | enum | `bootstrap` \| `refine` \| `lock` \| `evolve` (default: `refine`) |
| `updated_at` | string | ISO-8601 timestamp |
| `description` | string | One-line summary |
| `overview` | string | Specific cultural/product reference narrative |
| `intent` | object | Typed intent + required `reference` when present |
| `targets` | (string \| object)[] | e.g. `web`, `mobile`, `presentation`; object form declares environment constraints (§7.6) |
| `voice` | object | UI copy contract (§13C) |
| `extends` | string[] | Parent design files |
| `sources` | object[] | Extraction provenance |
| `tokens` | object | Normative design tokens |
| `locked` | string[] | Dot-paths that require an ask before edit |
| `components` | object | Component contracts |
| `patterns` | object | Page/composition recipes |
| `policy` | object | Decision policy |
| `decisions` | object | If→then trees |
| `constraints` | object | `always` / `never` lists |
| `examples` | object | Good/bad references |
| `provenance` | object | Owner and review metadata |
| `integrations` | object | Tool bridges (`shadcn`, `figma`, …) |
| `rationale` | object | DESIGN.md-style prose sections (colors, layout, elevation, …) |
| `omitted` | array | Intentionally absent sections (suppress “missing” warnings) |
| `themes` | object | Named modes (light/dark/brand) overlaying tokens |
| `exports` | object | Declared export targets (DTCG, CSS, Tailwind, …) |
| `assets` | object | Non-embedded brand asset references (logo, wordmark, favicon) |

Unknown top-level keys: consumers MUST preserve them and SHOULD warn; they MUST NOT fail solely due to unknown keys (extension growth).

### DESIGN.md interop

`.design` imports [Google DESIGN.md](https://github.com/google-labs-code/design.md) frontmatter + body **losslessly**. Nothing required for designing from a DESIGN.md analysis SHOULD be dropped:

| DESIGN.md | `.design` |
| --- | --- |
| Frontmatter `colors` / `typography` / `spacing` / `rounded` / `components` | `tokens.color` / `typography` / `spacing` / `radius` / `components` |
| Body § Overview | `overview` (+ optional `rationale.overview`) |
| Body § Colors / Typography / Layout / Elevation / Shapes / Components | `rationale.*` |
| Body § Do’s and Don’ts | `constraints.always` / `constraints.never` **and** `rationale.dos` / `rationale.donts` |
| `omitted` | `omitted` |
| Token refs `{colors.x}` | `{tokens.color.x}` (see §11.3) |

Full mapping: [docs/design-md-mapping.md](docs/design-md-mapping.md).

---

### 7.1 Integrations — shadcn/ui

[shadcn/ui](https://ui.shadcn.com/) is the most common agent codegen target for React/Tailwind. `.design` does **not** replace `components.json`; it **orchestrates** it.

When `integrations.shadcn.enabled` is true, agents MUST:

1. Prefer installing/using shadcn components listed in the project (via CLI / registry / MCP) instead of inventing primitives.
2. Write theme tokens into the CSS file referenced by `integrations.shadcn.css` using the [shadcn CSS variable convention](https://ui.shadcn.com/docs/theming) (`background`/`foreground`, `primary`/`primary-foreground`, …) — the **full** current variable set, including `chart-1`…`chart-5` and the `sidebar-*` group, so Chart and Sidebar components theme correctly.
3. Keep `components.json` fields in sync when initializing a project (`style`, `base`, `iconLibrary`, aliases, `registries`, `tailwind.cssVariables`). `tailwind.baseColor` and `tailwind.cssVariables` cannot be changed after init — restyle through `css_vars`, never by re-initializing.
4. On Tailwind v4 projects, register any **custom** variable (beyond the standard set) under `@theme inline` in addition to `:root` / `.dark`, or no utility class can use it.
5. Install brand components only from declared `registries` — never guess a registry namespace.
6. Match the project's primitive `base` (`base` \| `radix` \| `react-aria`); never mix primitive libraries in one project.

```yaml
integrations:
  shadcn:
    enabled: true
    style: nova              # current styles: vega, nova, maia, lyra, mira, luma, rhea, sera (legacy: new-york)
    base: base               # primitive library: base | radix | react-aria
    icon_library: lucide
    preset: base-nova        # optional init preset (base + style combo)
    css_variables: true      # MUST be true for token-driven theming
    base_color: neutral      # init-only; options: neutral, stone, zinc, mauve, olive, mist, taupe
    css: app/globals.css
    components_json: ./components.json
    rsc: true
    tsx: true
    aliases:
      components: "@/components"
      utils: "@/lib/utils"
      ui: "@/components/ui"
      lib: "@/lib"
      hooks: "@/hooks"
    registries:
      "@acme": "https://registry.acme.com/{name}.json"   # ${ENV_VAR} for auth headers; never inline secrets
    components: [button, card, input]    # canonical installs (names, @ns/name, or URLs)
    mcp: true                # shadcn MCP server available for search/view/add
    radius: "0.5rem"         # maps to --radius (base of derived radius-sm…radius-4xl scale)
    css_vars:
      theme:                 # mode-independent vars (radius, fonts, tracking)
        radius: "0.5rem"
      light:
        background: "#ffffff"
        foreground: "#0a0a0a"
        primary: "#0a0a0a"
        primary-foreground: "#fafafa"
        secondary: "#f4f4f5"
        secondary-foreground: "#0a0a0a"
        muted: "#f4f4f5"
        muted-foreground: "#71717a"
        accent: "#f4f4f5"
        accent-foreground: "#0a0a0a"
        destructive: "#dc2626"
        border: "#e4e4e7"
        input: "#e4e4e7"
        ring: "#0a0a0a"
        card: "#ffffff"
        card-foreground: "#0a0a0a"
        popover: "#ffffff"
        popover-foreground: "#0a0a0a"
        chart-1: "#2a9d90"
        chart-2: "#e76e50"
        chart-3: "#274754"
        chart-4: "#e8c468"
        chart-5: "#f4a462"
        sidebar: "#fafafa"
        sidebar-foreground: "#0a0a0a"
        sidebar-primary: "#0a0a0a"
        sidebar-primary-foreground: "#fafafa"
        sidebar-accent: "#f4f4f5"
        sidebar-accent-foreground: "#0a0a0a"
        sidebar-border: "#e4e4e7"
        sidebar-ring: "#0a0a0a"
      dark:
        background: "#0a0a0a"
        foreground: "#fafafa"
        # …same keys
    map_from_tokens:
      background: tokens.color.canvas
      foreground: tokens.color.ink
      primary: tokens.color.primary
      primary-foreground: tokens.color.on-primary
      border: tokens.color.hairline
      ring: tokens.color.primary-focus
```

Value notes:

- `css_vars` values are any valid CSS color written **verbatim** into `:root` / `.dark` — never wrap in `hsl()`. Upstream shadcn ships `oklch()` values since Tailwind v4; hex is equally valid. Keep the format consistent with `tokens.*`.
- `map_from_tokens` values are dot-paths into this file. The fallback form `a|b|c` means *first path that resolves wins* (useful for generated files mapping across brands).

### Relationship

| Artifact | Role |
| --- | --- |
| `.design` | Visual contract + shadcn theme mapping + component when/when_not |
| `components.json` | CLI install paths, style, aliases, registries |
| `globals.css` | Concrete `--background`, `--primary`, `--radius`, … values |
| DTCG `tokens.json` | Optional export of `tokens.*` for other tools |

`tokens.*` remain normative. `integrations.shadcn.css_vars` SHOULD be derived from tokens (via literals or `map_from_tokens`). If both disagree, **tokens win** and CSS vars MUST be updated to match.

### Agent workflow with shadcn

```text
Need UI?
├── integrations.shadcn.enabled?
│   ├── Yes → use shadcn components (button, card, …)
│   │         ensure css_vars applied to globals.css
│   │         respect components.json aliases / style
│   └── No → implement with project stack + tokens
└── Always obey constraints / decisions / when / when_not
```

---

### 7.2 Integrations — Figma

`.design` is the **repo-canonical** contract. Figma is an authoring surface. Sync direction is explicit.

```yaml
integrations:
  figma:
    enabled: true
    file_key: "ABC123xyz"
    file_url: "https://www.figma.com/design/ABC123xyz/Product"
    variable_collections: ["Color", "Spacing"]
    modes: ["Light", "Dark"]
    sync:
      direction: figma_to_design   # or design_to_figma | bidirectional
      tokens_path: "./tokens/figma.dtcg.json"
    code_connect: true
    notes: "Variables are source for primitives; semantic roles live in .design"
```

| Field | Meaning |
| --- | --- |
| `file_key` / `file_url` | Design file identity for MCP / REST |
| `variable_collections` | Which Figma collections map into `tokens.*` |
| `modes` | Figma modes ↔ `themes.*` |
| `sync.direction` | Who wins on conflict; agents MUST ask if unclear |
| `tokens_path` | Optional DTCG dump path used as interchange |

Agents using Figma MCP MUST still **write normative decisions into `.design`** (components when/when_not, constraints, rationale). Variables alone are not a complete visual contract.

---

### 7.3 Themes (modes)

Multi-mode products (light/dark, brand skins) use `themes` as overlays on base `tokens`:

```yaml
themes:
  default: light
  modes:
    light:
      tokens:
        color:
          canvas: "#ffffff"
          ink: "#0a0a0a"
    dark:
      tokens:
        color:
          canvas: "#0a0a0a"
          ink: "#fafafa"
    high-contrast:
      tokens:
        color:
          primary: "#0000EE"
```

Rules:

- Base `tokens` are the shared defaults; mode objects **override** by path.
- `integrations.shadcn.css_vars.light` / `.dark` SHOULD match `themes.modes.light` / `dark` when both exist; **tokens + themes win**.
- Agents MUST generate UI for the active mode (user/OS preference or `themes.default`) and not invent a third palette.
- Mode palettes MUST be **designed, not inverted**: dark mode preserves surface layering (the top canvas stays the lightest dark surface) and re-tunes accents; it is never a mechanical negative of light.
- Deliberately single-theme systems SHOULD declare `themes: { single: true, reason: "…" }` so consumers do not warn about (or invent) a missing mode.
- Recommended CSS emission: components consume variables only; modes redefine variables under `@media (prefers-color-scheme: dark)` **and** `:root[data-theme="dark"]` / `:root[data-theme="light"]` so an explicit toggle beats the OS preference in both directions (see `exports.css.mode_strategy`).

---

### 7.4 Exports (toolchain bridges)

Declare where tooling SHOULD emit derived artifacts. `.design` remains normative; exports are generated.

```yaml
exports:
  dtcg:
    path: "./tokens/tokens.json"
    format: dtcg@2025.10
  css:
    path: "./src/styles/tokens.css"
    selector: ":root"
    prefix: ""                      # optional var prefix
    mode_strategy: both             # media-query | data-attribute | both
    attribute: data-theme
  tailwind:
    path: "./tailwind.theme.css"    # v4 @theme CSS; version: 3 emits a theme.extend JSON fragment
    version: 4
  shadcn_registry:
    path: "./registry/brand-theme.json"
    type: registry:theme            # registry:theme | registry:style | registry:base
  style_dictionary:
    config: "./sd.config.js"
  ios: { path: "./Sources/Tokens/Colors.swift" }
  android: { path: "./tokens/colors.xml" }
```

Notes:

- `shadcn_registry` maps `css_vars.light`/`dark` → registry-item `cssVars.light`/`dark` and mode-independent vars → `cssVars.theme`, producing a [registry item](https://ui.shadcn.com/docs/registry/registry-item-json) installable in any project via the shadcn CLI.
- `css.mode_strategy: both` emits variables under the media query **and** the `data-theme` attribute selectors so explicit toggles override OS preference.

Recommended pipeline:

```text
.design (normative)
  → export DTCG JSON
  → Style Dictionary / custom transforms
  → CSS variables, Tailwind @theme, iOS/Android
  → app consumes generated files
```

Reference implementations ship in this repository: `scripts/export_design.py` (CSS with mode strategies, Tailwind v4 `@theme`, DTCG, shadcn registry item) and `scripts/diff_design.py` (§18 diff + regression flag). Agents MAY use them, reimplement them, or hand-write CSS / shadcn vars from `tokens` + `themes`.

---

### 7.5 Assets (references only)

```yaml
assets:
  logo:
    light: "./brand/logo-light.svg"
    dark: "./brand/logo-dark.svg"
  wordmark: "./brand/wordmark.svg"
  favicon: "./public/favicon.ico"
  og_image: "./brand/og.png"
  font_files:
    - "./public/fonts/GeistVF.woff2"
```

Paths only — never embed binaries. Clear-space / misuse rules belong in `rationale` or `constraints`.

---

### 7.6 Targets (environment constraints)

`targets` entries MAY be objects that declare the constraints of the rendering environment, so agents adapt emission instead of shipping silently broken output:

```yaml
targets:
  - web
  - name: web-artifact
    external_assets: false     # CSP blocks CDN fonts/scripts — inline everything, data-URI assets
    single_file: true          # bundle to one self-contained HTML file
    notes: "System font stack or embedded @font-face only"
  - name: email
    external_assets: true
    notes: "Table layout; no custom properties"
```

When `external_assets: false`, agents MUST NOT emit external font/script/stylesheet URLs for that target — inline styles and assets, or fall back to system stacks.

---

## 8. Agent bootstrap

A `.design` file MUST be **self-contained**. When an agent is pointed at the file, or the file is dragged into a chat, `agent.instructions` alone MUST be enough to use it correctly — even if the portable `design` skill is not installed.

```yaml
agent:
  skill: design
  instructions: |
    You are holding a .design living visual contract (schema design.v1).
    If the AgentsORG `design` skill is installed, activate it — then still obey THIS file as source of truth.
    If the skill is absent, follow these instructions exactly.

    READ
    - Load this file before any UI generation or restyle. Large file? Normative core first
      (intent, constraints, policy/decisions, tokens, components, themes, voice, locked); rationale on demand.
    - Order: overview/intent → constraints → policy/decisions → tokens → voice → rationale → components/patterns → integrations → locked.
    - Tokens and structured rules are normative. Rationale is judgment when tokens under-specify.

    FOLLOW (generate or edit UI)
    - Calibrate treatment per surface: patterns.<name>.treatment > intent.treatment
      (utilitarian = restrained product craft; editorial = distinctive identity).
    - Prefer catalog components; obey when / when_not and decisions.* (first match wins).
    - Bind every listed component property (backgroundColor, textColor, typography, rounded, padding, size, height, width).
    - Never invent raw hex/spacing/radius when a token exists.
    - Apply patterns.*; enforce constraints.always / never; apply voice.* to all UI copy.
    - Concentrate boldness in intent.signature; keep everything around it quiet.
    - Themes: generate for the active mode (themes.default); modes are designed, never inverted.
    - Match the project's existing styling stack — do not switch stacks.
    - If integrations.shadcn.enabled: prefer shadcn UI; write css_vars into the listed CSS file; tokens win on conflict.
    - If integrations.figma is present: this file is repo-canonical unless sync.direction says otherwise; ask on conflicts.
    - Craft defaults when this file is silent: one primary CTA; nested radius = outer − padding; transform/opacity only (<300ms); 44×44 targets; focus visible; prefers-reduced-motion; no transition:all.

    UPDATE
    - Edit this file in place when design changes. Git is history.
    - Ask before changing any path in locked. Bump version (SemVer).

    VERIFY
    - Compare tokens ↔ CSS/Tailwind and components ↔ imports; report drift per token group
      as added/removed/modified plus a regression flag before fixing.

    PRECEDENCE
    1) User prompt  2) This file  3) design skill  4) Generic taste skills  5) Model defaults

    NEVER
    - Invent a parallel design system beside this file
    - Embed binaries or full page HTML trees here
    - Claim affiliation with third-party brands used only as visual references
```

| Field | Required | Description |
| --- | --- | --- |
| `skill` | no | Agent Skills name to activate if installed (`design`) |
| `instructions` | **MUST** | Full procedure for drop-in / drag-drop use without the skill |

Authors MAY shorten `instructions` only if every READ / FOLLOW / UPDATE / VERIFY / PRECEDENCE duty above remains covered. Full template: [docs/self-contained.md](docs/self-contained.md).

Consumers that encounter a file **without** `agent.instructions` SHOULD warn and apply the portable skill (if present) or the template in docs/self-contained.md.

### 8.1 Reading tiers (large files)

Authors SHOULD keep a `.design` file readable in one pass. When a file grows large (long `rationale`, many components), consumers MAY read in tiers instead of loading everything up front:

| Tier | Sections | Loading |
| --- | --- | --- |
| Normative core | `schema`, `agent`, `intent`, `constraints`, `policy`, `decisions`, `tokens`, `components`, `locked`, `themes`, `voice` | MUST load before generating UI |
| Judgment | `overview`, `rationale.*`, `patterns`, `examples` | SHOULD load; MAY defer sections irrelevant to the task |
| Tooling | `integrations`, `exports`, `assets`, `sources`, `provenance` | Load when performing that operation |

Oversized narrative belongs in linked docs (via `examples.ref`-style paths), not inline.

---

## 9. Intent

```yaml
intent:
  reference: "Linear density with marketplace clarity"
  direction: editorial-minimal
  signature: "The mesh-gradient hero band — everything else stays monochrome"
  treatment: utilitarian
  density: comfortable
  trust: high
  energy: medium
  playfulness: low
  emotion: calm
```

If `intent` is present, `intent.reference` MUST be present and SHOULD be a specific cultural or product reference (not a list of generic adjectives).

| Field | Purpose |
| --- | --- |
| `direction` | The **committed** aesthetic direction, named (e.g. `minimal`, `editorial`, `brutalist`, `industrial`, `retro-futuristic`, `playful-geometric`). One named direction beats three adjectives. |
| `signature` | The single distinctive element that carries the design. Boldness concentrates in the signature; everything around it stays quiet. |
| `treatment` | Default register: `utilitarian` (polished, restrained product craft) or `editorial` (distinctive identity — landing pages, marketing). `patterns.<name>.treatment` overrides per surface. |

Optional scale fields (`trust`, `energy`, `playfulness`, etc.) SHOULD use `low` \| `medium` \| `high` or documented scales such as `density`: `compact` \| `comfortable` \| `spacious`.

---

## 10. Sources

```yaml
sources:
  - type: repo
    path: "packages/ui"
  - type: figma
    file_key: "ABC123"
  - type: url
    ref: "https://www.example.com"
  - type: components_json
    path: "./components.json"
  - type: file
    path: "./brand/brandbook.pdf"
```

Common `type` values: `repo`, `figma`, `url`, `file`, `components_json`, `other`. Unknown kinds are accepted (consumers treat them as `other`).

Bootstrap/extract operations MUST populate `sources` when evidence exists.

---

## 11. Tokens

Tokens are normative. Agents MUST use token values instead of inventing raw colors, fonts, or spacing when a token exists. This section aligns with DESIGN.md frontmatter token groups (colors, typography, spacing, rounded) plus elevation/motion extensions.

### 11.1 Recommended groups

| Group | DESIGN.md equivalent | Purpose |
| --- | --- | --- |
| `tokens.color` | `colors` | Semantic colors (`primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`, …) |
| `tokens.typography` | `typography` | Role objects (typically 9–15 levels: display, headline, body, label, caption, …) |
| `tokens.spacing` | `spacing` | Scale levels; optional `unit` (e.g. `4` or `8`); MAY include `gutter`, `margin`, `section` |
| `tokens.radius` | `rounded` | Corner radius scale (`none`, `sm`, `md`, `lg`, `xl`, `full`, …) |
| `tokens.elevation` | Elevation & Depth (prose → tokens) | Shadow / blur / border treatments that encode depth |
| `tokens.motion` | — | Durations (ms) and easing |
| `tokens.breakpoint` | Responsive Behavior | Named viewport thresholds (`sm`, `md`, `lg`, …) |
| `tokens.opacity` | — | Opacity scale (prefer 0–1 for CSS) |
| `tokens.zIndex` | — | Stacking scale |
| `tokens.border` | — | Optional border widths / styles |
| `tokens.iconography` | Iconography prose | Default set, sizes, stroke rules |
| `tokens.background` | — | Atmosphere treatments: gradients, mesh, noise/grain, patterns — the one aesthetic dimension flat color maps cannot express |

Additional groups are allowed. Scale level names MAY be any descriptive string (`xs`, `sm`, `md`, `lg`, `xl`, `full`, `section`, …).

Token groups MAY **nest** to arbitrary depth (RECOMMENDED ≤ 20 levels, matching DESIGN.md interop limits). Nested tokens are addressed by their full dot path:

```yaml
tokens:
  color:
    background:
      light: "#ffffff"
      dark: "#0a0a0a"
  spacing:
    inset:
      sm: 8
      md: 16
# refs: {tokens.color.background.light}, {tokens.spacing.inset.md}
```

```yaml
tokens:
  breakpoint:
    sm: 640px
    md: 768px
    lg: 1024px
    xl: 1280px
    content-max: 1440px
  opacity:
    muted: 0.64
    disabled: 0.4
  zIndex:
    nav: 50
    modal: 100
    toast: 110
  iconography:
    set: lucide
    stroke: 1.5
    sizes: { sm: 16, md: 20, lg: 24 }
  motion:
    duration: { fast: 150ms, base: 250ms, slow: 400ms }
    easing:
      enter: cubic-bezier(0.32, 0.72, 0, 1)
      exit: cubic-bezier(0.4, 0, 1, 1)
      move: ease-in-out
    spring: { duration: 0.5s, bounce: 0 }
  background:
    hero-mesh: "radial-gradient(at 30% 20%, #007cf0, transparent 60%), radial-gradient(at 70% 60%, #ff0080, transparent 55%)"
    grain: "url(#noise) opacity 0.04"
    section-wash: "linear-gradient(180deg, {tokens.color.canvas} 0%, {tokens.color.canvas-soft} 100%)"
```

Easing curves, durations, and spring configs SHOULD live here as shared tokens — new motion extends these, never introduces a parallel hand-typed set.

### 11.2 Value types

| Type | Format | Example |
| --- | --- | --- |
| Color | Any CSS color string (hex, named, `rgb()`, `oklch()`, `color-mix()`, …) | `"#0B57D0"`, `oklch(62% 0.18 250)` |
| Dimension | number + unit (`px`, `em`, `rem`), or bare number in spacing/radius scales and typography sizes (interpreted as px) | `16px`, `1.5rem`, `4` |
| Typography | object | see below |
| Elevation | CSS shadow / filter string or structured object | `"0 4px 24px rgba(0,0,0,0.12)"` |
| Token reference | `{dot.path}` | `"{tokens.color.primary}"` |

Color semantics:

- Hex `#RRGGBB` is the RECOMMENDED default authoring format; `oklch()` is RECOMMENDED when deriving scales programmatically.
- Contrast checks compute in sRGB, but consumers MUST preserve the **authored** string for display and export.
- Non-color strings found in color positions on import (gradients, `color-mix()` chains) are accepted as opaque strings with a warning — never dropped, never a crash.
- When exporting to DESIGN.md, unitless `radius` numbers MUST gain a `px` suffix (DESIGN.md `rounded` accepts Dimensions only, units limited to `px`/`em`/`rem`); `spacing` numbers pass through.

**Typography object** fields (DESIGN.md-compatible):

| Field | Type | Notes |
| --- | --- | --- |
| `fontFamily` | string \| string[] | Required for a useful style. MAY be a CSS-style comma list or an array — the first entry is the brand face, the rest are the fallback stack (match x-height) |
| `fallbacks` | string[] | Alternative to an inline stack: ordered fallback faces applied when the primary is unavailable (offline targets, blocked font CDNs) |
| `fontSize` | Dimension | e.g. `16px`, `1rem` |
| `fontWeight` | number \| string | e.g. `400`, `600` |
| `lineHeight` | Dimension \| number | Unitless multiplier recommended |
| `letterSpacing` | Dimension | e.g. `-0.02em` |
| `fontFeature` | string | → `font-feature-settings` |
| `fontVariation` | string | → `font-variation-settings` |

### 11.3 References

- Canonical paths use the `tokens.*` prefix: `{tokens.color.primary}`, `{tokens.radius.md}`, `{tokens.typography.body-md}`, `{tokens.spacing.lg}`.
- **DESIGN.md interop:** consumers SHOULD rewrite legacy refs when importing:
  - `{colors.X}` → `{tokens.color.X}`
  - `{typography.X}` → `{tokens.typography.X}`
  - `{spacing.X}` → `{tokens.spacing.X}`
  - `{rounded.X}` → `{tokens.radius.X}`
- Inside `components`, references MAY point at composite typography objects (e.g. `{tokens.typography.label-md}`), matching DESIGN.md.
- Elsewhere, references SHOULD resolve to primitive values.
- A token value MAY reference another token; consumers MUST resolve chains up to depth **10** (matching DESIGN.md interop limits).
- Broken or circular references MUST fail validation; exceeding reference depth (10) or nesting depth (20) is an error. Linters SHOULD suggest the nearest known token name on broken refs.

### 11.4 Elevation

```yaml
tokens:
  elevation:
    flat: "none"
    soft-hairline: "0 0 0 1px rgba(0,0,0,0.08)"
    card: "0 4px 24px rgba(0,0,0,0.08)"
    product-shadow: "rgba(0,0,0,0.22) 3px 5px 30px 0"
    blur-nav: "backdrop-filter: blur(12px)"
```

If the brand is intentionally flat, document that in `rationale.elevation` and MAY set `omitted` to exclude unused elevation levels — do not invent heavy shadows.

### 11.5 Relationship to DTCG

v1 uses simple maps for agent readability. Tooling SHOULD be able to export to the [W3C Design Tokens Format Module](https://www.designtokens.org/tr/2025.10/format/). v1 does not require `$value` / `$type` graphs inside the file.

---

## 12. Locked paths

```yaml
locked:
  - tokens.color.primary
  - tokens.typography.heading.fontFamily
```

Paths use dot notation from the document root. Agents MUST ask the user before editing locked paths. Unlocked paths may be edited when the user requests an update or when refining an unlocked system.

---

## 13. Components

Components are normative style contracts for UI atoms. This section represents the [DESIGN.md Components](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) model **completely**: every DESIGN.md component property is representable, and `.design` adds catalog metadata (`when` / `when_not`, `import`, `decisions`) so agents do not lose usage rules during designing.

### 13.1 Two valid encodings

**A. Catalog form (recommended)** — family key + nested variant token bags + usage rules:

```yaml
components:
  button:
    description: "Primary call-to-action control"
    import: "@/components/ui/button"
    when: ["page primary action", "form submit"]
    when_not: ["navigation links", "more than one filled primary per view"]
    variants: [primary, secondary, danger]
    states: [default, hover, pressed, disabled, loading]
    anatomy: [icon-left, label, icon-right]
    status: stable
    tokens:
      primary:
        backgroundColor: "{tokens.color.primary}"
        textColor: "{tokens.color.on-primary}"
        typography: "{tokens.typography.body}"
        rounded: "{tokens.radius.pill}"
        padding: "11px 22px"
      primary-hover:
        backgroundColor: "{tokens.color.primary-focus}"
        textColor: "{tokens.color.on-primary}"
      danger:
        backgroundColor: "{tokens.color.error}"
        textColor: "{tokens.color.on-primary}"
```

**B. DESIGN.md flat form (interop)** — sibling keys per variant/state (exact DESIGN.md shape):

```yaml
components:
  button-primary:
    backgroundColor: "{tokens.color.primary}"
    textColor: "{tokens.color.on-primary}"
    typography: "{tokens.typography.body}"
    rounded: "{tokens.radius.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{tokens.color.primary-70}"
  button-primary-active:
    backgroundColor: "{tokens.color.primary-80}"
```

Rules for flat form:

- A component entry whose value is a **property bag** (has `backgroundColor` / `textColor` / … and no nested `tokens` object) is a DESIGN.md-style entry.
- Variants/states are **sibling keys** (`button-primary-hover`), not nested `button-primary.hover`.
- Importers SHOULD group `button-*` into catalog form when adding `when` / `when_not`, without dropping any sibling variant.

Both forms MAY coexist in one file. Agents MUST treat all entries as part of the catalog.

### 13.2 Component metadata (catalog form)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `description` | string | no | Human summary |
| `import` | string | no | Module path when implemented in code |
| `when` | string[] | conditional | When to use |
| `when_not` | string[] | conditional | When not to use |
| `variants` | string[] | no | Declared variant ids (keys under `tokens` or flat siblings) |
| `states` | string[] | no | Interaction states (`default`, `hover`, `pressed`, `disabled`, `loading`, `focus`, …) |
| `anatomy` | string[] | no | Structural slots |
| `status` | enum | no | `stable` \| `experimental` \| `deprecated` |
| `tokens` | object | no | Map of variant-or-state id → property bag |
| `notes` | string | no | Extra crafting guidance |

Rules:

- If `variants` is non-empty, the component MUST include `when` and/or `when_not` (at least one non-empty list).
- `import` SHOULD point at the real module path when the component exists in code.
- Agents MUST prefer catalog components over inventing new ones when `policy.reuse.prefer_existing_components` is true (default).

### 13.3 Property tokens (DESIGN.md whitelist + aliases)

Each property bag (flat entry or `tokens.<variant>`) MAY include:

| Property | Type | DESIGN.md | Notes |
| --- | --- | --- | --- |
| `backgroundColor` | Color \| ref | yes | Alias: `background` |
| `textColor` | Color \| ref | yes | Alias: `foreground` |
| `typography` | Typography ref \| object | yes | Composite refs allowed |
| `rounded` | Dimension \| ref | yes | Alias: `radius` |
| `padding` | Dimension \| string | yes | e.g. `12px` or `11px 22px` |
| `size` | Dimension | yes | Square control size |
| `height` | Dimension | yes | |
| `width` | Dimension | yes | |
| `borderColor` | Color \| ref | extension | Accepted; warn if unknown to strict linters |
| `borderWidth` | Dimension | extension | |
| `shadow` | Elevation string \| ref | extension | Prefer `{tokens.elevation.*}` |
| `gap` | Dimension \| ref | extension | |
| `opacity` | number \| string | extension | |

Canonical writers SHOULD prefer DESIGN.md names (`backgroundColor`, `textColor`, `rounded`) for interop. Readers MUST accept aliases (`background`, `foreground`, `radius`).

Unknown property names: **accept with warning** (same consumer behavior as DESIGN.md) — do not strip during import. Boolean scalar values in property bags MUST be accepted, not rejected. The same property reachable via two names (`background` **and** `backgroundColor`) with **different** values is a collision error.

### 13.4 Recommended component types

DESIGN.md encourages (non-exhaustive). Domain-specific names are encouraged:

| Type | Typical keys / variants |
| --- | --- |
| Buttons | `button-primary`, `button-secondary`, hover/active/disabled siblings |
| Chips | selection / filter / action |
| Lists | item, divider, leading/trailing |
| Tooltips | surface, timing via `tokens.motion` |
| Checkboxes | checked / unchecked / indeterminate |
| Radio buttons | selected / unselected |
| Input fields | default, focus, error; labels & helper text in `rationale.components` |
| Links | `text-link`, on-dark variants |
| Navigation | global nav, sub-nav, sticky bars |
| Cards / tiles | product tiles, utility cards |

### 13.5 Designing with components (agent duties)

When generating UI, agents MUST:

1. Resolve the matching catalog or flat entry before inventing styles.
2. Bind every listed property (color, type, radius, padding, size) — do not “approximately” restyle.
3. Apply hover/active/focus sibling entries when present.
4. Read `rationale.components` for qualitative guidance that tokens alone omit.
5. Record new approved variants back into `components` (UPDATE step) so later sessions do not lose them.

---

### 13A. Rationale (DESIGN.md body)

Machine tokens are incomplete without the **why**. `rationale` holds the DESIGN.md markdown-body sections as structured prose so conversion from getdesign.md / DESIGN.md loses nothing.

```yaml
rationale:
  overview: |
    Holistic brand & style narrative (may duplicate/extend top-level overview).
  colors: |
    Palette roles, when to use each token, gradients policy…
  typography: |
    Hierarchy principles, substitutes, OpenType notes…
  layout: |
    Grid, max width, whitespace philosophy, spacing rhythm…
  elevation: |
    How depth is conveyed (shadows vs tonal layers vs hairlines)…
  shapes: |
    Corner language, pill vs sharp, icon geometry…
  components: |
    Cross-cutting component craft (button grammars, input anatomy)…
  dos:
    - Use primary only for the single most important action per screen
    - Maintain WCAG AA contrast for body text
  donts:
    - Mix rounded and sharp corners in the same view
    - Use more than two font weights on a single screen
```

| Key | DESIGN.md section |
| --- | --- |
| `overview` | Overview / Brand & Style |
| `colors` | Colors |
| `typography` | Typography |
| `layout` | Layout / Layout & Spacing |
| `elevation` | Elevation & Depth |
| `shapes` | Shapes |
| `components` | Components (prose) |
| `dos` / `donts` | Do’s and Don’ts |
| `responsive` | Responsive Behavior (common extension) |
| `iteration` | Iteration Guide (common extension) |
| `known_gaps` | Known Gaps (common extension) |

Unknown rationale keys: preserve (e.g. `iconography`, `motion`). Agents MUST NOT drop unfamiliar `##` sections when importing DESIGN.md.

Rules:

- Present sections SHOULD follow this order when authored for humans.
- `constraints.always` / `constraints.never` SHOULD mirror the strongest dos/donts as short enforceable laws; `rationale.dos` / `rationale.donts` MAY keep the fuller list.
- Agents MUST read relevant `rationale.*` when tokens under-specify taste (whitespace, photography-first, flat vs shadowed, …).

---

### 13B. Omitted sections

Matches DESIGN.md `omitted`: intentionally absent groups so linters/agents do not invent filler.

```yaml
omitted:
  - tokens.motion
  - section: patterns
    reason: "Marketing-only system; no app shell patterns yet"
```

Each entry is either a string path/name or `{ section, reason? }`.

Both namespaces are valid: DESIGN.md section/category names imported verbatim (`spacing`, `Do's and Don'ts`) and `.design`-native dot paths (`tokens.motion`). Do not rewrite imported names to dot paths — round-tripping breaks. Entries suppress the matching §19 warnings.

---

### 13C. Voice (UI copy contract)

Words are design material. `voice` gives agents an enforceable home for copy rules that brand systems always carry and token files never do:

```yaml
voice:
  register: "Plain, direct, technical-friendly. Confident, never cute."
  casing: sentence            # UI casing default (labels, buttons, headings)
  terminology:
    webhook_endpoint: "notification URL"     # system term → user term
    org: "workspace"
  action_naming: "Button label names the exact action; the same verb carries through the flow (Publish → Published)."
  errors: "State what happened, why, and the next step. Never blame the user."
```

| Field | Meaning |
| --- | --- |
| `register` | The product's voice in one or two sentences |
| `casing` | `sentence` \| `title` \| custom note |
| `terminology` | Map of internal/system terms → end-user vocabulary |
| `action_naming` | Continuity rule for action labels across a flow |
| `errors` | Error copy style rule |

Agents writing UI copy MUST apply `voice` with the same force as `tokens`: end-user vocabulary, active voice, labels naming the exact action, error copy that states cause and fix.

---

## 14. Patterns

```yaml
patterns:
  landing_hero:
    treatment: editorial
    allowed: [headline, subhead, primary_cta, supporting_visual]
    forbidden: [stat_strip, floating_promo_chips]
    prioritize: []
  settings_page:
    treatment: utilitarian
    allowed: [section_nav, field_groups, save_bar]
    forbidden: [decorative_illustration]
```

Patterns describe composition recipes, not full page trees. `treatment` overrides `intent.treatment` per surface: `utilitarian` surfaces get restrained product craft; `editorial` surfaces run the distinctive-identity register. A well-composed page is never the wrong answer; an over-designed identity sometimes is.

---

## 15. Policy and decisions

### 15.1 Policy

```yaml
policy:
  hierarchy: [typography, spacing, contrast, color]
  reuse:
    prefer_existing_components: true
    invent_threshold: "only if no component covers the interaction"
  fallback_order: [semantic_token, nearest_approved_token, ask]
  if_missing: ask
  accessibility:
    contrast: AA
    focus_visible: required
    reduced_motion: honor
  color:
    accent_cycle: [accent-orange, accent-blue, accent-green]
  responsive:
    if_mobile: reduce_padding_before_font_size
    if_dense_data: prioritize_table_over_cards
```

`policy.color.accent_cycle` is an ordered list of `tokens.color` names that **decorative, non-text elements rotate through** (multi-accent brand systems). Text color on each accent is chosen by contrast against that background, not fixed. Without this field, agents MUST NOT rotate accents.

| Field | Default | Meaning |
| --- | --- | --- |
| `if_missing` | `ask` | `ask` \| `nearest` \| `invent_with_note` |

### 15.1.1 Craft defaults (informative)

When the file is silent on a craft detail (nested radius, motion duration, tap target size, line measure, …), agents following the portable `design` skill are expected to apply the skill’s [CRAFT.md](skills/design/references/CRAFT.md) defaults. Those defaults are **non-normative soft rules**: any explicit `tokens`, `constraints`, `rationale`, `components`, or `decisions` entry in this file **overrides** them.

Recommended `constraints` starters that encode common craft laws:

```yaml
constraints:
  always:
    - one filled primary action per view
    - use semantic tokens; never hardcode hex when a token exists
    - honor focus-visible and prefers-reduced-motion
  never:
    - "transition: all"
    - hover-only access to core actions
    - animating layout properties when transform/opacity suffice
```

### 15.2 Decisions

```yaml
decisions:
  button:
    - if: destructive
      then: { variant: danger }
    - if: page_primary
      then: { variant: filled }
  typography:
    - if: "text >= 24px"
      then: { role: heading }
    - if: "numeric data column"
      then: { role: mono-data }
```

Agents SHOULD walk `decisions.<key>` in order and apply the first matching rule. Keys are not limited to components: token roles (`typography`, `color`, `elevation`) MAY carry deterministic application rules, which is what lets an agent apply the brand across arbitrary surfaces without per-case judgment.

---

## 16. Constraints and examples

```yaml
constraints:
  always:
    - use semantic tokens; never hardcode hex when a token exists
    - one filled primary button per view
  never:
    - gradients as brand chrome
    - glassmorphism
    - off-system fonts

examples:
  good:
    - ref: "./docs/examples/home-good.png"
      note: "Homepage hero"
  bad:
    - ref: "./docs/examples/home-bad.png"
      note: "Card soup"
```

`ref` MAY be a relative path or URL. Binary assets are not embedded.

### 16.1 Authoring constraints that work

- Write constraints as **absolute or numeric laws** (`never`, `always`, `≤ 300ms`), not hedged prose (`try to`, `where appropriate`, `tasteful`). Hedged rules do not change agent behavior.
- Pair non-obvious rules with their why (in `rationale.*`) so they generalize to cases the author never wrote down.
- Encode judgment as decision procedures (`decisions.*` if→then, first match wins) rather than outcome descriptions.
- A good file constrains **dimensions** (type, color, motion, backgrounds), names the **defaults to avoid**, and gives one **specific reference** — it does not dictate every pixel. Constrained direction plus execution freedom outperforms both extremes.

---

## 17. Provenance

```yaml
provenance:
  owner: design-system
  last_reviewed: "2026-08-05"
  source_material:
    - "./brand/brandbook.pdf"
```

---

## 18. Updating the file

Agents update `.design` by **editing the file directly**.

| Operation | Behavior |
| --- | --- |
| `bootstrap` / `extract` | Create or fill draft from `sources`; set `status: bootstrap` |
| `update` | Edit unlocked fields; bump `version` and `updated_at` |
| `lock` / `unlock` | Adjust `status` and/or `locked[]` with user intent |
| `verify` | Compare contract to code (CSS vars, Tailwind, components); report findings per token group as **added / removed / modified**, plus a **regression** flag when anything consumers may rely on was removed or changed; fix only when asked |

### SemVer

- **MAJOR** — breaking visual or component API change (user confirmation required)
- **MINOR** — additive tokens, variants, patterns
- **PATCH** — fixes and clarifications

Git commits and PRs are the audit trail. Do not maintain an in-file proposal queue or changelog.

---

## 19. Validation

Consumers and linters SHOULD check:

| Rule | Severity |
| --- | --- |
| Missing `schema` / `name` / `version` | error |
| Broken `{token}` references (SHOULD suggest nearest known token) | error |
| Circular `extends` or token refs | error |
| Token reference chain deeper than 10 / nesting deeper than 20 | error |
| Alias or path collision — same property/token reachable via two names with different values | error |
| Component with `variants` but no `when`/`when_not` | error |
| `intent` without `reference` | error |
| Edit to `locked` path without user ask | error |
| Missing `agent.instructions` | error |
| Missing `tokens.color.primary` (unless in `omitted`) | warning |
| Empty or missing `tokens.typography` (unless in `omitted`) | warning |
| Unknown top-level key | warning |
| Unknown top-level key whose value parses as a token-like map (silently ignored tokens) | warning |
| Unknown typography sub-property | warning |
| `rationale` sections out of canonical order (§13A) | warning |
| Orphan color tokens never referenced | warning |
| Contrast failures on component fg/bg pairs | warning |

---

## 20. Consumer behavior for unknown content

| Scenario | Behavior |
| --- | --- |
| Unknown top-level key | Preserve; warn |
| Unknown token group | Accept if values parse |
| Unknown component property | Accept; warn |
| Duplicate component key | Error |
| Missing optional sections | Allowed |

---

## 21. Out of scope (non-goals)

The following MUST NOT be required in a `.design` file:

- Full page or screen layout trees / generated HTML  
- Embedded binary assets or font files (use `assets` paths)  
- Entire Figma or Storybook dumps  
- Secrets or private registry credentials  
- A parallel DTCG `$value`/`$type` graph **inside** the file (use `exports.dtcg`)  
- In-file `proposed_changes` or `history` queues (use git)  
- Replacement of CSS, Tailwind, or component frameworks as rendering engines  

### Ecosystem position (informative)

`.design` sits **above** interchange formats and **beside** agent procedure files:

| Layer | Role |
| --- | --- |
| Figma Variables / Tokens Studio | Design-time authoring |
| `.design` | Repo-canonical living contract + agent decisions |
| DTCG JSON (`exports.dtcg`) | Interchange for Style Dictionary |
| CSS / Tailwind / iOS / Android | Runtime consumption |
| shadcn `components.json` + CSS vars | Common React codegen path |
| `AGENTS.md` + `skills/design` | Discovery + enriched CRAFT procedure (optional; file must still self-teach) |
| DESIGN.md / getdesign.md | Bootstrap / analysis sources |

---

## 22. Minimal valid example

```yaml
schema: design.v1
name: starter
version: 1.0.0
status: refine

agent:
  skill: design
  instructions: |
    You are holding a .design living visual contract (schema design.v1).
    If the design skill is installed, activate it - still obey THIS file.
    If absent, follow these instructions exactly.
    READ this file before UI. FOLLOW tokens, components, constraints.
    Bind component properties; never invent hex when a token exists.
    UPDATE in place; ask before locked paths. VERIFY tokens vs CSS when asked.
    Precedence: user prompt > this file > design skill > generic taste.

overview: |
  A minimal product UI: calm ops surface, one accent, no decoration theater.

intent:
  reference: "A precise internal tool — Stripe Dashboard density without coldness"
  direction: calm-utilitarian
  signature: "One saturated blue reserved for the single primary action"
  treatment: utilitarian
  density: comfortable
  trust: high

voice:
  register: "Plain and direct; confident, never cute."
  casing: sentence
  errors: "Say what happened and the next step."

tokens:
  color:
    primary: "#0B57D0"
    on-primary: "#FFFFFF"
    surface: "#F8FAFC"
    text: "#0F172A"
  spacing:
    unit: 4
    sm: 8
    md: 16
    lg: 24
  radius:
    sm: 6
    md: 10
  typography:
    body:
      fontFamily: IBM Plex Sans
      fontSize: 16
      fontWeight: 400
    heading:
      fontFamily: IBM Plex Sans
      fontSize: 24
      fontWeight: 600

components:
  button:
    when: ["primary actions"]
    when_not: ["more than one filled primary per view"]
    variants: [filled, ghost, danger]
    states: [default, hover, disabled]

policy:
  if_missing: ask
  hierarchy: [typography, spacing, contrast, color]

constraints:
  always:
    - use semantic tokens
    - one filled primary per view
  never:
    - gradients
    - glassmorphism
    - off-system fonts
```

---

## 23. Versioning of this specification

This document defines **design.v1**. Future major schema versions (`design.v2`, …) MAY introduce breaking field changes. Tools SHOULD accept older schemas for read/follow and MUST NOT perform write operations they cannot safely preserve (§3).

---

## 24. Conformance

A file is **design.v1 conformant** when:

1. It parses as a single YAML or JSON object.  
2. It includes valid `schema`, `name`, `version`, and `agent.instructions`.  
3. It satisfies the MUST rules in this document for the fields it uses.  
4. Token references and `extends` graphs resolve without cycles (chain depth ≤ 10, nesting depth ≤ 20).  

A consumer is **conformant** when it implements discovery (§4), precedence (§5), and the update rules (§18) for the operations it claims to support.
