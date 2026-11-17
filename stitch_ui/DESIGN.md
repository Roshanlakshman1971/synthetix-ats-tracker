---
name: Synthetix ATS Engine
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#ca8100'
  on-tertiary-container: '#3e2400'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  metric-num:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system delivers an authoritative, high-precision AI recruitment tooling experience. It targets career-driven professionals, executives, and talent specialists who require algorithmic confidence, rigorous parsing analytics, and instantaneous keyword synthesis. The visual environment balances enterprise SaaS credibility with cutting-edge artificial intelligence affordances.

The design movement combines **Modern SaaS with Precision Glassmorphism**:
- **Structured Precision:** Crisp delineation, calibrated data visualizers, and data-dense dashboards evoking executive control.
- **Architectural Depth:** Layered translucent surfaces, subtle spectral violet refractive borders, and controlled ambient backdrops.
- **Trust & Validation:** Analytical metric indicators, rigorous scorecards, and non-distracting semantic accents prioritizing immediate scanning and validation.

## Colors

The palette is engineered for prolonged analytical work within a dark-mode-first environment.

- **Primary (`#6366F1` - Electric Indigo):** Anchors primary calls-to-action, active navigational states, interactive drag-and-drop zones, and AI synthesis triggers.
- **Secondary (`#10B981` - Emerald Precision):** Dedicated semantic signal for high ATS compatibility scores (85%+), verified syntax matches, and optimized parsing metrics.
- **Tertiary (`#F59E0B` - Amber Alert):** Indicates keyword gaps, formatting friction points, and warning diagnostics requiring user intervention.
- **Neutral (`#0F172A` - Slate Abyss):** Base substrate for the system. Tonal variants range from deep slate surfaces (`#0B0F19`) to elevated containers (`#1E293B`) and ultra-subtle border strokes (`#334155`).

Apply color strictly to convey status and guide scanning; keep neutral background real estate dominant to ensure high ATS data density remains legible.

## Typography

Typography prioritizes tabular clarity, high-speed scannability, and structural refinement. 

- **Plus Jakarta Sans** governs headings, key metric counters, and display anchors. Its crisp geometric architecture lends modern executive presence without sacrificing optical balance.
- **Inter** handles all narrative parsing text, matched resume bullet points, configuration panels, and micro-labels. Its neutral grotesque skeleton maintains optimal legibility across varying font sizes and high-density tabular viewports.

Metric values (`metric-num`) utilize tabular figures when possible to prevent horizontal jitter during real-time scoring updates.

## Layout & Spacing

The layout model is built on an adaptable 12-column responsive fluid grid designed for side-by-side comparative views (e.g., Target Job Description vs. Candidate Resume vs. Live ATS Diagnostic Score).

- **Desktop (≥ 1280px):** 12-column layout with 24px (`1.5rem`) gutters and dynamic page margins centered within a max-width container of `1536px`. Supports tri-pane workflows: Navigation/Job Panel (3 cols), Live Resume Editor (6 cols), and ATS Insight Inspector (3 cols).
- **Tablet (768px - 1279px):** 8-column layout with 16px (`1rem`) gutters and 24px margins. Panels collapse into stacked, tabbed views.
- **Mobile (≤ 767px):** 4-column layout with 16px margins. Comparative editors collapse into linear, step-wise inspection cards with sticky metric progress docks.

Internal component spacing follows an 8px base grid rhythm (`0.5rem`), scaling down to 4px (`0.25rem`) for micro-badges and keyword chips.

## Elevation & Depth

Visual hierarchy is maintained through subtle glassmorphism and tonal surface layering against dark slate grounds.

- **Base Ground (`#090D16`):** The canvas canvas bedrock.
- **Surface Level 1 (`#0F172A` with 80% opacity, `backdrop-filter: blur(12px)`):** Applied to persistent navigation, sidebar docks, and primary dashboard containers. Framed by a 1px border of `rgba(255, 255, 255, 0.07)`.
- **Surface Level 2 (`#1E293B` with 70% opacity, `backdrop-filter: blur(16px)`):** Applied to draggable resume section cards, ATS inspection widgets, and keyword lists. Bordered with `rgba(255, 255, 255, 0.12)`.
- **Surface Level 3 (Floating Overlays & Popovers):** Highest surface tier (`#1E293B` at 95% opacity), reinforced by an ambient violet-tinted shadow: `0 20px 32px -8px rgba(0, 0, 0, 0.5), 0 0 1px 1px rgba(99, 102, 241, 0.2)`.
- **Active Scanning Glow:** Active scoring elements use a localized, soft radial backlight: `box-shadow: 0 0 24px -4px rgba(99, 102, 241, 0.25)`.

## Shapes

The design system employs a **Rounded** (Token `2`) geometry profile:
- Primary interactive buttons, standard form fields, and keyword pill chips utilize `0.5rem` (8px).
- Structural content cards, preview viewports, and dashboard panels use `rounded-lg` at `1rem` (16px).
- Modals, large drop-zones, and summary score units use `rounded-xl` at `1.5rem` (24px).
- Metric indicator rings and status dot anchors remain full circular geometry (`rounded-full`).

This geometric cadence pairs software precision with approachable, modern consumer ergonomics.

## Components

### Buttons
- **Primary:** Solid Electric Indigo (`#6366F1`) with white text, crisp 8px radius, accompanied by an inner top highlight border (`rgba(255, 255, 255, 0.2)`). Hover initiates a subtle brightness increase and `0 4px 14px rgba(99, 102, 241, 0.4)` bloom.
- **Secondary:** Semi-transparent slate (`rgba(30, 41, 59, 0.6)`) with `1px` border of `rgba(255, 255, 255, 0.1)`. Hover state shifts border to `rgba(99, 102, 241, 0.4)` and brightens text.
- **Ghost/Tertiary:** Pure translucent container, high-contrast label, active state framed with soft indigo wash (`rgba(99, 102, 241, 0.1)`).

### Metric Badges & Keyword Chips
- **Keyword Match Chip (Verified):** Background `rgba(16, 185, 129, 0.12)`, text `#34D399`, border `1px solid rgba(16, 185, 129, 0.25)`, leading mini-check icon.
- **Keyword Missing Chip (Gap):** Background `rgba(245, 158, 11, 0.1)`, text `#FBBF24`, border `1px dashed rgba(245, 158, 11, 0.3)`, leading plus icon for one-click insertion.
- **Overall ATS Score Gauge:** High-contrast radial gauge utilizing `#10B981` (for scores ≥ 80), `#F59E0B` (50–79), and `#EF4444` (&lt; 50). Center features `metric-num` Plus Jakarta Sans typography.

### Input Fields & Textareas
- Form inputs feature deep slate fill (`rgba(15, 23, 42, 0.6)`), 8px border radius, and `1px solid rgba(255, 255, 255, 0.1)`.
- Focused states trigger an electric indigo border (`#6366F1`) accompanied by a subtle `0 0 0 3px rgba(99, 102, 241, 0.2)` outer ring. Monospaced metadata inputs (e.g., parsed raw text) inherit clean sans-serif alignment.

### Cards & Comparison Panels
- Translucent glass finish (`backdrop-blur-md`), 16px corner radius, hairline outline (`rgba(255, 255, 255, 0.08)`).
- Header areas feature a subtle divider line separating configuration toggles from parsed content blocks.

### Selection Controls (Checkboxes & Radios)
- Checkboxes maintain 4px rounding; checked states display solid `#6366F1` with an optical white check icon.
- Radios are circular with centered `#6366F1` solid pips and high-contrast outer rings.

### ATS Difference Diffs (Tailoring Engine)
- Inline bullet recommendations highlight additions with subtle green underlines (`rgba(16, 185, 129, 0.2)`) and flagged weak impact verbs in amber strikethroughs with instant AI replace tooltips.