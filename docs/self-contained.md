# Canonical `agent.instructions` (self-contained)

Every `.design` file MUST embed enough procedure that an agent can use it after a drag-drop or `@`-mention **without** installing the portable skill. Normative copy lives in [SPEC.md §8](../SPEC.md).

Recommended block (adapt brand disclaimer as needed):

```yaml
agent:
  skill: design
  instructions: |
    You are holding a .design living visual contract (schema design.v1).
    If the AgentsORG `design` skill is installed, activate it — then still obey THIS file as source of truth.
    If the skill is absent, follow these instructions exactly.

    READ
    - Load this file before any UI generation or restyle. Large file? Normative core first
      (intent, constraints, policy/decisions, tokens, components, voice, locked); rationale on demand.
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
    - Match the project's existing styling stack (Tailwind/CSS/etc.) — do not switch stacks.
    - If integrations.shadcn.enabled: prefer shadcn UI, keep cssVariables true, write css_vars into the listed CSS file; tokens win over stale CSS vars.
    - If integrations.figma is present: treat .design as repo-canonical unless sync.direction says otherwise; ask on conflicts.
    - Themes: use themes.default / active mode overlays on tokens.
    - Craft defaults when this file is silent: one primary CTA per view; nested radius = outer − padding; animate transform/opacity only (<300ms); 44×44 tap targets; focus visible; prefers-reduced-motion; ~65ch body measure; no transition:all; no hover-only core actions.

    UPDATE
    - Edit this file in place when the design system changes. Git is history — no in-file proposal queues.
    - Ask the user before changing any path listed in locked.
    - Bump version (SemVer: MAJOR breaking, MINOR additive, PATCH fix).

    VERIFY
    - When asked to sync/verify: compare tokens ↔ CSS/Tailwind; components ↔ imports; flag hardcoded values; report before rewriting.

    PRECEDENCE
    1) Explicit user prompt (this task)  2) This file  3) design skill  4) Generic taste skills  5) Model defaults

    NEVER
    - Invent a parallel design system beside this file
    - Embed binaries or full page HTML trees here
    - Claim affiliation with third-party brands used only as visual references
```
