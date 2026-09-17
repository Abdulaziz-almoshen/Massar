# UI component & motion references

The founder's standing reference set for Massar design work (given Sep 16, 2026). Load this
before any design run. Massar rules always win on conflict: RTL Arabic (Cairo), `DESIGN.md`
tokens, the `#2563EB` accent, western numerals, white page ground.

| Site | What it is | What to mine it for |
| --- | --- | --- |
| [libraries.dev](https://libraries.dev) | Interactive UI effects & animations | Border beam, thinking orbs, gooey, **metal** (real-time liquid-metal shader for buttons/text/badges, `metal-fx` on Paper Shaders) |
| [transitions.dev](https://transitions.dev) | Smooth transitions and micro-interactions | Page and state transitions, the easing vocabulary |
| [astryx.atmeta.com](https://astryx.atmeta.com) | 170+ customizable React components | Breadth; component API shapes |
| [beui.dev](https://beui.dev) | Animated components, Motion + Tailwind 4 | **Charts** (heat calendar, returns calendar, price-target fan), Number Animation (count-up, rolling ticker, fixed-slot digit swap), Tabs (spring `layoutId` indicator), Dock, Dynamic Island, Command Palette, Metallic Button |
| [coss.com/ui](https://coss.com/ui) | Clean, accessible React components | Accessible primitives, focus behaviour |
| [originkit.dev](https://originkit.dev) | Interactive components, polished animations | Interaction polish |
| [kinetics.colorion.co](https://kinetics.colorion.co) | Fluid motion powered by physics | Spring configs, momentum, interruptible gestures |
| [21st.dev](https://21st.dev) | 1,000+ AI-ready UI components | Dashboard layouts; `line-charts-8` (monotone-cubic curve, dashed reference line, stroke-dasharray draw) is already ported |
| [beautifului.dev](https://www.beautifului.dev) | Stunning components for AI products | The card/edge grammar: ring-in-box-shadow instead of a border, 6-stop shadows at 1-3% ink, concentric radius ladder, tabular figures |

## Rules for using them

Read the reference with `getComputedStyle`, never from memory. The measured values are the
point; a screenshot only tells you it looked nice. Past passes that worked did this:
beautifului.dev's edge is `0 0 0 1px` inside `box-shadow`, never a `border`; 21st.dev's chart
curve is Fritsch-Carlson monotone cubic, verified against recharts to within 0.006% path length.

Use a reference's component when it fits. Build custom only when nothing in the set covers the
need, and say which reference you departed from and why.

Motion rules come from `emil-design-eng` and are mandatory: custom easing curves (the built-in
CSS ones are too weak), UI motion under 300ms, `scale(0.97)` press feedback, never enter from
`scale(0)`, exit faster than enter, `@media (hover: hover) and (pointer: fine)` on every hover
effect, `prefers-reduced-motion` honoured, and no animation at all on anything the user triggers
from the keyboard many times a day.
