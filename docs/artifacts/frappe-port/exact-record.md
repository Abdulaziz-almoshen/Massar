# Frappe CRM — Record Page, exact spec (source-read, Lead.vue reference)

Type tokens (frappe-ui `tailwind/generated/typography.json`, Inter Variable, line-height 1.15):
`2xs`11 `xs`12 `sm`13 `base`14 `md`15 `lg`16 `xl`17 `2xl`18 `3xl`20 `4xl`24 px.
Weights: regular 420 · medium 500 · semibold 600 · bold 700. So `text-lg-medium`=16/500,
`text-2xl-semibold`=18/600, `text-3xl-medium`=20/500, `text-base`=14/420, `text-sm`=13/420.
Spacing = 0.25rem step incl. fractional: `7.5`=30px, `10.5`=42px, `15.5`=62px, `size-11`=44px.

## 1. Three regions
| Region | Box |
|---|---|
| App header (`LayoutHeader`, teleported to `#app-header`) | `h-10.5` **42px**, `py-[7px]`, `pl-5` (sm) / `pl-2`, `justify-between`; left group `flex items-center gap-2`, right group same |
| Body | `div.flex.h-full.overflow-hidden` → `Tabs` (`flex-1`, column) + `Resizer` |
| Side panel (`Resizer side="right"`, `border-l`, `flex flex-col justify-between`) | width **352px** default, min **256**, max **480**, persisted `localStorage.sidebarWidth`, snaps to 352 within ±10px. Drag handle: `absolute w-1` (4px) full-height `bg-surface-gray-4`, `opacity-0 → 100` on hover, `cursor-col-resize`, on `left-0` |
| Tab list | `min-h-[45px]`, `px-5`, `gap-7.5` (**30px** between tabs), tabs `px-0 shrink-0`, scrollbar height 0; panel `flex grow` |

Contact.vue inverts it: Resizer **left** (`border-r`), tabs right.

## 2. Header, left → right
**Left:** `Breadcrumbs` — `[Leads] › [saved view (icon `mr-2 h-4`)] › [record title]`; view crumb only when `?view`/`?viewType`.
**Right (exact order):** `CustomActions(document._actions)` → `CustomActions(document.actions)` → `EnrichFromWebsite` → `AssignTo` → **status Dropdown** → *(Lead only)* solid `Convert to Deal`.
- CustomActions: plain Buttons for ungrouped actions (`FeatherIcon h-4 w-4` prefix); grouped ones collapse into a `lucide-more-horizontal` Dropdown; labelled groups render `label + chevron`.
- AssignTo: `Popover placement="bottom-end"`. 0 assignees → Button "Assign To"; 1 → Button wrapping avatar **+ name** (`text-base`); >1 → stacked `MultipleAvatar` size `md`, `flex-row-reverse`, `-mr-1.5` overlap, `ring-2 ring-outline-base`, `hover:scale-110`.
- Status: Button with `IndicatorIcon` prefix tinted by the status colour, label = status name, `iconRight` chevron-down/up. Options = **all** `CRM Lead Status` / `CRM Deal Status` rows ordered `position asc` (server data, not hardcoded), each `{label, icon: IndicatorIcon(color)}`; `placement="right"`.
- **Copy-id row** (top of side panel, not the header): `h-[45px] border-b px-5 py-2.5 cursor-copy text-lg-medium text-ink-gray-9`, click copies the docname.

Below it: identity block `flex items-center gap-5 border-b p-5` — Avatar `size-12` (48px, `size="3xl"`) with hover camera overlay (`h-9`, `bg-black/40`, `rounded-b-full`, `clip-path inset(12px 0 0 0)`); right column `gap-2.5`: title `text-3xl-medium` truncate, then icon-button row `gap-1.5`: Call (if telephony) · Email · Website · Attach · Delete (`subtle`/red, if permitted). Deal = same box but the avatar is the org logo, read-only. Then `SLASection` if `sla_status`.

## 3. Tabs — Lead and Deal are identical (10)
Order: **Activity** (default) · Emails · Comments · Data · Events · Calls · Tasks · Notes · Attachments · WhatsApp *(only if `whatsappEnabled`)*. Icons: Activity/Email/Comment/Details/Event/Phone/Task/Note/Attachment/WhatsApp. **No counts or badges on Lead/Deal.** Contact has one tab: *Deals* (`DealsIcon`) **with** a solid gray `size="sm"` count Badge; its `#tab-item` is `flex items-center gap-2 border-b border-transparent py-2.5 text-base text-ink-gray-5 → text-ink-gray-9` when selected, icon `h-5`.
Default tab (`useActiveTabManager`): URL hash `#activity` wins → else `localStorage.lastLeadTab`/`lastDealTab` (seeded `'activity'`) → else index 0. Selecting a tab pushes the hash and persists (300ms debounce).

## 4. Activity timeline
`ActivityHeader` renders above the list on every tab **except Data**: `sm:mx-10 sm:mt-8 sm:mb-4`, left title `h-8 text-2xl-semibold text-ink-gray-8`, right primary action — Emails `New Email`+ · Comments `New Comment`+ · Calls MultiActionButton [Log a Call / Make a Call] · Events `Schedule an Event` · Notes `New Note` · Tasks `New Task` · Attachments `Upload Attachment` · WhatsApp `Send Template` + solid `New Message` · Activity `New ▾` (Email, Comment, Schedule an Event, Log a Call, Make a Call, Note, Task, Upload Attachment, WhatsApp Message).
List body: `FadedScrollableDiv flex flex-col h-full overflow-y-auto`. Loading = centered `LoadingIndicator h-6 w-6` + "Loading…" `text-2xl-medium ink-gray-4`.

**Rail** (Activity, Emails, Comments, Calls, Events only): `grid grid-cols-[30px_minmax(auto,_1fr)] gap-2 sm:gap-4 px-3 sm:px-10`. A 1px vertical line via `before:` at `left-[50%]`, `before:h-full` for every entry, `before:h-4` on the last. Icon puck `h-7 w-7` (`h-8` for comment/communication/call) with `bg-surface-base` masking the line. **No day grouping anywhere.**

| Type | Entry |
|---|---|
| change (`added/removed/changed/creation`) | no card, no avatar; puck = type icon `ink-gray-4`. `mb-4 flex-col gap-2 py-1.5`, one `text-base` line: **owner** (medium ink-gray-8) · verb · **field label** · old → new (User values get `UserAvatar xs` + full name). Timestamp right (`ml-auto`, `TimelineTimestamp` `text-sm ink-gray-5`, relative w/ exact in tooltip). Bursts collapse to "Show +N changes from <owner>" with a `!size-4` ghost toggle; expanded rows `py-1.5` with an `arrow-right` glyph |
| email | puck = **sender UserAvatar `md`** (`mt-2.5`). Card `rounded-md shadow-sm bg-surface-elevation-1 px-3 py-1.5`: sender name + `<addr>` (`text-sm ink-gray-5`, hidden <sm) + optional green "Notification" badge; right: status badge, timestamp, Reply / Reply-All ghost icons (`gap-0.5`). Then subject, then To/CC/BCC line; `border-t mt-3 mb-1`; body; attachments `flex-wrap gap-2`. Wrapper `pb-5` |
| comment | meta row `mb-1 py-1 text-base`: `UserAvatar md` + "**owner** added a **comment**"; right timestamp + owner-only `…` dropdown `!h-6 !w-6` (Edit/Delete). Body `rounded bg-surface-gray-1 px-3 py-[7.5px] text-base leading-6`. Wrapper `mb-4` |
| call | puck = Missed(red)/Declined/Inbound/Outbound icon. Meta row `Avatar md` + "has reached out / has made a call" + timestamp. Card `border rounded-md bg-surface-elevation-1 px-3 py-2.5 gap-2`: "Inbound/Outbound Call" `text-base-medium` + `MultipleAvatar sm`; badge row `flex-wrap gap-2` — date (`MMM D, dddd`), duration, Listen/Hide Recording, status (themed); AudioPlayer when expanded |
| task | **no rail.** `px-3 sm:px-10 pb-3 sm:pb-5`; row `flex gap-6 rounded p-2.5 hover:bg-surface-gray-1`; left `gap-1.5 text-base`: title `font-medium ink-gray-9`, sub-row `UserAvatar xs` + assignee · `DotIcon h-2.5` · Calendar + `D MMM, hh:mm a` · Dot · priority icon `!h-2 !w-2` + priority; right: status Dropdown (TaskStatusIcon) + `…` Delete. Divider `mx-2 h-px border-t` |
| note | **card grid**, no rail: `grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3 px-3 sm:px-10 pb-3 sm:pb-5`. Card `h-48` (192px) `rounded-md bg-surface-gray-1 px-4 py-3 hover:bg-surface-gray-2`: title `text-lg-medium ink-gray-8` + `…` dropdown `!h-6 !w-6`; body `prose-sm text-p-sm ink-gray-5 flex-1 overflow-hidden`; footer `UserAvatar xs` + name `text-sm ink-gray-8`, right modified timestamp `text-sm ink-gray-7` |
| attachment | **list, no rail**: row `p-2.5 rounded hover:bg-surface-sidebar`; `size-11` thumb (image `object-cover`, else bordered box + `size-4` file icon); name `text-base ink-gray-8` over size `text-sm ink-gray-5`; right column `items-end gap-2`: timestamp then two `!size-5` buttons (lock/unlock, trash) with `size-3` icons. Divider `mx-2 h-px`. *In the Activity tab* an `attachment_log` is one rail line: owner · action · filename (link) · lock glyph `size-3` · timestamp |
| event | own pane (`EventArea`, `h-full`), own rail `gap-4`, puck `CalendarIcon h-4 w-4`. Body `mb-5`: meta row (`Avatar md` + "has created an event" + timestamp); card `border rounded-lg px-2.5 py-2.5 flex gap-2` with a **2px** colour bar (`event.color`, default `#30A66D`), subject `font-medium ink-gray-7` + `MultipleAvatar sm` if >1 participant, second row time (left) / date (right) `ink-gray-6` |
| whatsapp | chat bubbles, **no rail, no avatars, no day separators**, `px-3 sm:px-10`. Row `flex gap-2 mb-3` (`mb-7` if reaction), `flex-row-reverse` for Outgoing. Bubble `max-w-[90%] rounded-md bg-surface-gray-1 p-1.5 pl-2 text-base shadow-sm`; failed → red badge `-top-2 right-0`; reply quote `border-l-4` (green incoming / blue outgoing) `bg-surface-gray-3 p-2`, sender `text-sm-bold`, `max-h-12`; hover chevron menu top-right; reaction chip `-bottom-5 rounded-full border p-1`; image `h-40 rounded-md`, document `size-10` icon |

**Empty states** — `EmptyState`, absolutely centred (`left-1/2 -translate-x-1/2`, `w-4/12`), `top: 32.3%` for Activity/Emails/Comments else `30%`; icon `size-7.5` (30px) `ink-gray-5`, `gap-3`; title `text-lg-medium ink-gray-8`; description `text-p-base ink-gray-6`, centred.

| Tab | Title / description |
|---|---|
| Activity | No Activities Found / There are no activities to display here. Go ahead and make some changes. |
| Emails | No Emails Found / No emails found in your inbox. New messages will appear here soon. |
| Comments | No Comments Found / Be the first to add one. |
| Data | No Data Fields Added Yet / No data fields have been added yet. |
| Calls | No Call History / No recent calls to display. Log a call or call someone now! |
| Notes | No Notes Found / Nothing here for now. Add a note to keep track of things. |
| Tasks | No Tasks Found / Nothing to do at the moment. Start organizing by adding one here. |
| Attachments | No Attachments Found / No files have been attached yet. Upload files to see them here. |
| WhatsApp | No WhatsApp Messages Found / Start a conversation now! |
| Events | No Events Scheduled / No events coming up. Create a new one to keep things on track. |

Docked composer below the scroll area: `CommunicationArea` on Emails/Comments/Activity; `WhatsAppBox` on WhatsApp.

## 5. Side panel (`SidePanelLayout`)
- Container `.sections flex flex-col overflow-y-auto`; each section separated by a `h-px border-t` (skipped before the first visible one); section padding `p-1 sm:p-3`.
- Section header (`CollapsibleSection`): `h-8` (32px), label `px-2 font-semibold` `text-base` ink-gray-9, `chevron-right h-4` **left** of the label rotating 90° when open (300ms), optional count Badge, actions slot right. Collapse animates `max-h 0 ↔ 200px`.
- **"Add field" affordance** = a ghost pencil `EditIcon` Button (`w-7 mr-2`) in the actions slot, rendered **once**, only for managers, not on mobile, never on the contacts section → opens `SidePanelModal` (full layout editor).
- Field column: `flex flex-col gap-1.5 overflow-y-auto`, `max-height 300px` (last section unbounded).
- **Field row:** `flex gap-2 px-3 leading-5 first:mt-3`, `items-center` (`items-start` for Text/Small Text/Long Text/Code). **Label left**: `w-[35%] min-w-20` truncate `text-sm ink-gray-5` (+ red `*` when mandatory, tooltip after 1ms; `pt-[9px]` for textareas). **Value right**: `w-[65%]` (`w-full` for Button/HTML), `min-h-[28px]`, `text-base`. Edit affordance = the control **is** the value: ghost inputs with transparent border/background (`margin:2px`), so text starts at 9px; hover/focus tints selects `surface-gray-1`. Read-only renders as plain text `h-7 px-2 py-1 ink-gray-5`. Trailing `ml-1`: `ArrowUpRight h-4 w-4` (navigate link / external URL) and pencil `size-3.5` for editable links.
- Controls by fieldtype: Dropdown · Check · Textarea · Select · Link · **User** Link (`UserAvatar sm` prefix `mr-1.5`, options show full name) · Time/Date/Datetime pickers · Percent/Int/Float/Currency (`FormattedInput`, 500ms debounce) · Password · Duration · Rating (`step 0.5`, max `options||5`, stored 0–1) · Button · Attach/Attach Image · HTML · Geolocation · Text Editor (`min-h-[38px]`) · TextInput default. Change → `triggerOnChange` → `document.save` (or emits `beforeFieldChange` when the page listens).
- Hidden when: empty read-only field (`hide_empty_read_only_fields`), failed `depends_on`, or `hidden`.
- **Contacts section (Deal only, `contacts_section`):** actions slot = a `Link` popover on a ghost `lucide-plus` Button (`h-7 px-3`) to attach an existing Contact or create one (opens ContactModal). Each contact: `px-2 pb-2.5`, `pt-5` first / `pt-2.5` rest; collapsible header row `h-7 gap-2 text-base ink-gray-7` = `Avatar md` + full_name + outline-green **Primary** Badge; right `…` dropdown (set-primary/remove) + `ArrowUpRight` → contact page + chevron toggle. Expanded: email row (`Email2Icon h-4 w-4`, `gap-3 pl-1 pt-4 pb-1.5`), mobile row (`p-1 py-1.5`), else "No Details Added" `py-4 text-sm ink-gray-4`. Divider `mx-2 h-px` between contacts; empty → `h-20` centred "No Contacts Added" `text-base ink-gray-5`; loading → `min-h-20` + `LoadingIndicator h-4 w-4`.
- Organization is **not** a list section — it is a normal Link field with `link` (route to Organization) and `create` (OrganizationModal) handlers.

*Sources: `frontend/src/pages/{Lead,Deal,Contact}.vue`, `components/Activities/*.vue`, `components/{SidePanelLayout,CollapsibleSection,Resizer,LayoutHeader,AssignTo,MultipleAvatar,CustomActions}.vue`, `ListViews/EmptyState.vue`, `composables/useActiveTabManager.js`, `stores/statuses.js`, frappe-ui tailwind preset + generated/typography.json. Inference (labelled): Lead/Deal tab items use frappe-ui's default `#tab-item`, which matches Contact's override minus the count badge.*
