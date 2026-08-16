# DESIGN.md — token authority

Base system: `.orbit/skills/massar-design-language.md` (palette, type, chips, cards). That file wins
on anything it defines. This file records tokens introduced by approved cycles and **overrides any
token a future run tries to invent**.

## Cycle `journey-scope` — per-contact campaign journeys (`#customer/<phone>`)
Approved prototype: `.orbit/design/previews/customer-journey-scope/v3-ledger-scope.html`

### New tokens
| token | value | use |
|---|---|---|
| `--scope-grad` | `linear-gradient(135deg,#0F2E52,#1F4470)` | sticky scope banner, campaign scope |
| `--scope-life-bg` | `#fff` + `1px solid #e3e7ee` | sticky scope banner, lifetime scope |
| `--gold` | `#C9A227` | lifetime-block start border (3px) |
| `--gold-bg` | `#FEFBF0` | lifetime-block card fill |
| `--gold-ink` | `#8a6d10` on `rgba(201,162,39,.16)` | «مدى الحياة» ribbon |
| `--overlap-bg` | `#FFF9EC`, border `#F2E3BC`, ink `#7a5c0c` | dual-attribution note |

### Type scale (this component)
- ledger column head `9.5px/700 #98A2B3` · journey name `13px/700 #101828` · window sub `10.5px #98A2B3`
- cell label `9.5px/600 #98A2B3` · cell value `12px/700 #101828` `direction:ltr;text-align:right`
- absent value `11px/500 #98A2B3` · reason line `11.5px/1.85 #667085`
- scope banner: label `10.5px/700 opacity .72` · value `15px/700` · window line `11.5px opacity .85`

### Spacing / shape
Card radius `14px`, chip radius `999px`. Card padding `18px 20px`; ledger row `13px 20px`
(`14px` at ≤480). Card gap `16px`. Row hairline `1px #F2F4F7`. Journey rail `3px`, radius `999px`.

### Rules that outrank aesthetics
1. **Scope before number.** No scoped figure renders without the scope banner visible above it.
2. **Zero with reason.** An absent fact renders as `٠` / `لا ردّ` / `لم تُسجَّل` plus one Arabic line
   saying why. Never blank, never a plausible substitute.
3. **Lifetime is marked in place.** Any lifetime-only block carries `--gold` start border + the
   «مدى الحياة» ribbon, or it is omitted. It never sits unlabelled beside scoped numbers.
4. **No winner is forced on overlap.** Both campaigns are named; neither is dimmed.
5. Focus ring `2px #2E7D77`, offset `2px`, on every interactive element. Motion ≤ 140ms hover tint.
