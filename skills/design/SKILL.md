---
name: design
description: Discover, read, follow, update, and verify AgentsORG .design living visual contracts. Use when generating or reviewing UI; restyling; extracting or remixing a design system; fixing design drift; locking tokens; or when a .design / *.design file exists. Triggers on: .design, design system, brand, tokens, components, DESIGN.md, restyle, visual identity, UI generation, design drift, remix, bootstrap design, verify design, landing page, dashboard, shadcn theme, design progress, UI review, polish, craft, accessibility.
license: MIT
metadata:
  author: AgentsORG
  version: "1.0"
  spec: design.v1
---

# `.design` Skill

You are operating against a **living visual contract**. The `.design` file is data. This skill is the procedure: **READ → FOLLOW → UPDATE → VERIFY**.

Project `.design` always beats generic frontend/taste skills. User chat can override for the current task only.

## When to activate

- Any UI generation, restyle, design review, or brand-consistency task
- A `.design` or `*.design` file exists in the repo
- User asks to bootstrap, remix, sync, lock, unlock, or verify design

## 1. Discover

1. From the edited path (or cwd), walk upward.
2. Prefer `.design`; else a single `*.design`; if multiple named files and no `.design`, ask.
3. Nearest file wins (monorepo package overrides root).
4. Resolve `extends` depth-first; child overrides parent; cycles = error — stop and report.
5. If no file exists and UI work is requested, offer **bootstrap** (do not invent an invisible system).

Load order once found:

1. `agent.instructions`
2. `overview` / `intent` / `rationale.overview`
3. `constraints` (+ `rationale.dos` / `rationale.donts`)
4. `policy` / `decisions`
5. `tokens` (including `elevation` when present)
6. `rationale` (colors, typography, layout, elevation, shapes, components)
7. `components` / `patterns` (bind every property in each bag)
8. `integrations` (e.g. shadcn)
9. `examples`
10. `locked` when updating
11. `omitted` (do not invent filler for listed sections)

## 2. Read

Treat tokens and structured rules as **normative**. Use `intent.reference` and `overview` for taste. Adjective-only intent without a specific reference is weak — prefer the reference sentence.

If `agent.skill` is `design`, you are on the correct procedure.

## 3. Follow (generate / edit UI)

Walk this loop every time:

```
Need UI change?
├── Match an existing components.* entry?
│   ├── Yes → walk decisions.<component> (first match wins)
│   │         bind tokens (never hardcode if token exists)
│   │         obey when / when_not
│   └── No → policy.if_missing
│             ├── ask → ask the user
│             ├── nearest → closest approved component + note
│             └── invent_with_note → invent once, then update .design catalog
├── Apply patterns.* if the surface matches
├── Enforce constraints.always / constraints.never
├── If integrations.shadcn.enabled:
│     prefer shadcn components (aliases.ui)
│     write css_vars (from map_from_tokens / literals) into integrations.shadcn.css
│     keep components.json style, aliases, cssVariables aligned
│     tokens.* win if they disagree with css_vars
└── Else: match the project's styling system (Tailwind, CSS, CSS-in-JS) —
    apply .design VALUES into the existing stack; never impose a new stack
```

Preserve `policy.hierarchy` when trading off (default: typography → spacing → contrast → color).

Then apply craft defaults from [references/CRAFT.md](references/CRAFT.md) wherever `.design` is silent (hierarchy, surfaces, motion, a11y, copy). **`.design` wins** on conflict.

After generating, cite which tokens and components you used.

Detailed trees: [references/APPLY.md](references/APPLY.md). Craft: [references/CRAFT.md](references/CRAFT.md). shadcn: [docs/shadcn.md](../../docs/shadcn.md).

## 4. Update (design progress)

Edit the `.design` file **in place**. Git is the history — do not invent an in-file proposal queue.

| Situation | Action |
| --- | --- |
| Path in `locked` | Ask the user before changing |
| Unlocked path + user asked to update | Edit file; bump `version` + `updated_at` |
| Bootstrap / extract | Fill draft; set `status: bootstrap`; populate `sources` |
| Sync from Claude Design / Stitch / Figma | Merge into file; ask before overwriting locked keys |
| Breaking change | Confirm with user; MAJOR SemVer bump |

SemVer: MAJOR = breaking visual/API; MINOR = additive; PATCH = fix/clarify.

Full rules: [references/UPDATE.md](references/UPDATE.md) and [SPEC.md](../../SPEC.md) §18.

## 5. Verify (drift)

When asked to sync/verify, or after large UI refactors:

1. Compare `tokens` to CSS custom properties / Tailwind theme / token files
2. If `integrations.shadcn.enabled`, compare `css_vars` + `radius` to `globals.css` and `components.json`
3. Compare `components` to real imports and variants
4. Flag hardcoded hex/spacing that should be tokens
5. Report findings; update `.design` only when asked

Checklist: [references/REVIEW.md](references/REVIEW.md) (includes CRAFT escalation triggers and Before/After/Why table).

## 6. Precedence conflicts

1. Explicit user prompt (this task)  
2. Nearest `.design`  
3. This skill (procedure + [CRAFT.md](references/CRAFT.md))  
4. Generic design/taste skills  
5. Model defaults  

## 7. What not to do

- Do not invent a parallel design system when `.design` exists
- Do not hardcode colors/fonts/spacing when tokens exist
- Do not put full page HTML trees or binaries into `.design`
- Do not edit locked paths without asking
- Do not replace the project's styling toolchain
- Do not add `proposed_changes` or in-file changelog blocks

## Quick field map

See [references/SPEC-SUMMARY.md](references/SPEC-SUMMARY.md).

## References

| File | Role |
| --- | --- |
| [APPLY.md](references/APPLY.md) | Decision trees for follow |
| [CRAFT.md](references/CRAFT.md) | Design-engineering bar when contract is silent |
| [REVIEW.md](references/REVIEW.md) | Verify / critique |
| [UPDATE.md](references/UPDATE.md) | In-place edit rules |
| [ATTRIBUTION.md](references/ATTRIBUTION.md) | Craft source credits |
