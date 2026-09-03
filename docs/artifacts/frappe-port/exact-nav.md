# Frappe CRM — exact shell & navigation spec

Read from clone `frappe-crm/frontend/src/`. `*` = inference, not in repo.

## 0. Skeleton
`DesktopLayout` = `flex h-screen w-screen` → `AppSidebar` + `flex-1 overflow-auto`(`AppHeader` + slot) + `GlobalModals`.
`MobileLayout` = `MobileSidebar` (headlessui drawer, `AppSidebar mobile`, 260px, overlay gray-8/50, closes on `route.fullPath` change) + `MobileAppHeader` (hamburger → `mobileSidebarOpened`, `#app-header`, `CallUI`).
`AppHeader` = `flex border-b pr-5` → `<div id="app-header" flex-1>` + `CallUI`. Pages teleport into it via `LayoutHeader` (`header h-10.5 py-[7px] pl-5`; slots `left-header` / `right-header`, each `flex items-center gap-2`).

## 1. Sidebar (`Layouts/AppSidebar.vue`)
frappe-ui `<Sidebar v-model:collapsed>` in `relative flex h-full bg-surface-gray-1`, inner `flex h-full flex-col p-2`. Collapse persisted in `localStorage.isSidebarCollapsed`; mobile disables collapse, forces 260px. Expanded/collapsed px = frappe-ui defaults (*~240px / ~50px rail*).

Order:
1. **Workspace switcher** (`UserDropdown`) — `h-12`, `BrandLogo` h-8, line1 `brand.name||'CRM'`, line2 `user.full_name`, `chevron-down`; collapsed → text/chevron `w-0 opacity-0`.
2. **Notifications** (`id=notifications-btn`, `NotificationsIcon`) — desktop toggles panel, mobile routes to `Notifications`. Suffix `Badge variant=subtle` = `unreadNotificationsCount`; collapsed → 1.5px dot top-right of icon.
3. Section **All Views** (`hideLabel:true` → no header): Dashboard `lucide-layout-dashboard` (desktop) · Leads · Deals · Contacts · Organizations · Notes · Tasks · Calendar (desktop) · Call Logs — icons `Leads/Deals/Contacts/Organizations/Note/Task/Calendar/PhoneIcon`.
4. Section **Public Views** — only if `getPublicViews().length`.
5. Section **Pinned Views** — only if `getPinnedViews().length`.

Headers: `CollapsibleSection` + `SidebarLabel divider mb-1 mt-4` = `lucide-chevron-right` (rotate-90 when open) + truncated label; row toggles; all `opened:true`. Rows: right tooltip hoverDelay 1.5. Active = `activeItem`, set on click (skipped for meta/ctrl/shift/alt/middle), key = `route.query.view || route.name`.

Bottom (`mt-auto`, desktop): `SignupBanner` (`is_demo_site`) · `TrialBanner` (`is_fc_site`) · `GettingStartedBanner` (onboarding incomplete) · **Clear Demo Data** (`BrushCleaningIcon`, red; manager+demo data) · **Help** (`HelpIcon` → HelpModal) · **Collapse/Expand** (`CollapseSidebar`, mirrored when collapsed).

**Switcher dropdown** — from `settings.dropdown_items`; `type='Separator'` starts a group. Standard `name1`: `app_selector` (submenu = `frappe.apps.get_apps` + synthetic **Desk** → `/desk`), `settings` (opens Settings modal, desktop), `login_to_fc` (FC sites), `about`, `logout`. Custom items → `window.open(route, open_in_new_window?'_blank':'')`.

## 2. Views (`stores/views.js`, `ViewControls.vue`, `ViewModal.vue`)
- Store `crm-views` ← `crm.api.views.get_views`; buckets `pinnedViews`, `publicViews`, `standardViews[dt+' '+type]`, `defaultView`.
- Doctype **CRM View Settings** stores: `label, icon, type(list|group_by|kanban), dt, route_name, filters, order_by, columns, rows, group_by_field, column_field, kanban_columns, kanban_fields, title_field, load_default_columns, pinned, public, is_standard, is_default, user`.
- Created from breadcrumb dropdown → **Create View** (`+`). `ViewModal` asks **View Name** + **Icon** (lucide IconPicker; legacy emoji preserved). Modes: Create / Edit View / Duplicate View.
- Sidebar link `{name: route_name, params:{viewType:type}, query:{view:name}}`; icon = stored → per-route default → `PinIcon`.
- Row `⋯` actions: **Set As Default** (standard, non-default) · **Duplicate** · **Edit** · **Pin/Unpin View** (non-public) · **Make Public/Private** (manager) · group "Delete View" → **Delete** (red confirm). Standard views: only Set As Default + Duplicate.
- Dirty view → **Cancel** + **Save Changes** bar in ViewControls.

## 3. Settings modal (`Settings/Settings.vue`)
`Dialog size=5xl`, `h-[calc(100vh-8rem)]`, `w-56` left nav, sticky group labels. Opened by `showSettings`; deep-link `activeSettingsPage`.

| Group | Items |
|---|---|
| User Configuration | Profile, Preferences |
| System Configuration *(mgr)* | General, Dashboard, Defaults, Brand, Calendar |
| User Management *(mgr)* | Users, Invite User, Sales Hierarchy |
| Email | Accounts *(mgr)*, Templates |
| Automation & Rules *(mgr)* | Assignment Rules, SLA Policies, Forms |
| Customization *(mgr)* | Home Actions |
| Integrations | Telephony, WhatsApp *(installed+mgr)*, ERPNext *(mgr)*, Lead Syncing *(mgr)* |

## 4. Every modal

| Modal | Trigger | Does |
|---|---|---|
| GlobalModals | both layouts | hosts CreateDocument, QuickEntry, ChangePassword, About, FieldLayoutDialogContainer |
| Lead/Deal/Contact/OrganizationModal | list "Create" | create record via quick-entry layout |
| CreateDocumentModal | `showCreateDocumentModal` | generic create, any doctype |
| QuickEntryModal | `showQuickEntryModal` | renders configured quick-entry layout |
| DoctypeModal / DoctypeModals | `useDoctypeModal()` | generic create/edit any doctype |
| ConvertToDealModal | "Convert to Deal" | pick/create contact + org, convert |
| LostReasonModal | status → Lost | lost reason + notes (Other required) |
| AssignmentModal | AssignTo | manage assignees |
| EditValueModal | bulk actions | **Bulk Edit** one field over selection |
| DeleteLinkedDocModal / BulkDeleteLinkedDocModal | delete w/ links | confirm linked-doc deletion |
| EventModal | Calendar | Create/Edit/Duplicate an Event |
| CallLogDetailModal | call log row | call detail + linked task/note |
| EmailTemplateSelectorModal / WhatsappTemplateSelectorModal | composers | 4xl template pickers |
| ViewModal | views dropdown | Create/Edit/Duplicate view |
| FieldLayoutDialog(+Container) | "Edit Field Layout" | 3xl editor, "Not Saved" badge, Preview/Reset/Save |
| DataFieldsModal | side panel | 4xl "Edit Data Fields Layout" |
| SidePanelModal | side panel settings | edit record side-panel layout |
| ChangePasswordModal | onboarding/profile | password + strength checks |
| AddExistingUserModal | Settings→Users | add existing site user to CRM |
| AboutModal | dropdown → About | version info |
| Sla/EditResponseResolutionModal, Sla/WorkDayModal | SLA settings | priority response/resolution; working hours |
| HelpModal, IntermediateStepModal (frappe-ui) | Help / onboarding step | docs tree; video step |

## 5. Top bar
- **LIST** (`pages/Leads.vue`): left `ViewBreadcrumbs` = router-link "Leads" + `/` + views Dropdown (icon + current view label + chevron). Right = `CustomActions` (custom list actions) + solid **Create** (`plus`). Under it `ViewControls`: quick-filter row · divider · [Cancel|Save Changes] · Refresh · GroupBy · Filter · SortBy (non-kanban) · Kanban/ColumnSettings · `⋯` (Import, Export, Customize Quick Filters).
- **RECORD** (`pages/Lead.vue`): left `Breadcrumbs` = [Leads] → [view label+icon if `?view`] → [record title]. Right = `CustomActions`(`_actions`,`actions`) + `EnrichFromWebsite` + `AssignTo` + status Dropdown (indicator + chevron) + solid **Convert to Deal**. Body = `Tabs` + right `Resizer` panel with 45px click-to-copy record-ID head.

## 6. Rest of shell
- **Notifications panel**: absolute `left: calc(100% + 1px)`, fixed 400px, full height, outside-click closes (ignores `#notifications-btn`). Title + "Mark all as read"; `TabButtons` **All**/**Events** (Mentions commented out); rows = unread dot + avatar/WhatsApp icon + text + `timeAgo`, click marks read + routes to record hash. Sockets `crm_notification`/`event_notification`. Empty: "No New Notifications".
- **Shortcuts**: `composables/useKeyboardShortcuts.js` — global handler, skips typing targets + open dialogs; used per page. `KeyboardShortcut.vue`/`ShortcutTooltip.vue` render hints. **No command palette.**
- **Onboarding** (`useOnboarding('frappecrm')`), 9 steps: setup password · create first lead · invite team *(mgr)* · convert lead to deal · create first task · create first note · add first comment · send email · change deal status. Surfaces: GettingStartedBanner, HelpModal (docs tree: Introduction, Settings, Masters, Capturing Leads, Views, Other Features, Customization, Integration, Mobile), IntermediateStepModal (video + CTA).
- **CallUI** pinned in app header on both layouts.
