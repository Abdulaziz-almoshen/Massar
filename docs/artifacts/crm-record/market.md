# Market brief — CRM contact-record anatomy, inline editing, AI provenance (task #13)

Scope: the five questions asked, nothing else. Positioning line and sizing omitted deliberately —
this is a UX prior-art scan, not a category fork. All structural claims carry a URL; inferences are labeled.

## 1. Anatomy of the HubSpot contact record (2026 default layout)

Three regions, and HubSpot's own docs name them left sidebar / middle column / right sidebar
([work-with-records](https://knowledge.hubspot.com/records/work-with-records),
[updated default layout](https://knowledge.hubspot.com/records/understand-the-default-record-layout)):

- **Left sidebar** — (a) *Highlight section*: primary + secondary display properties (name, email) plus the
  action/log-activity icons; (b) *Key information / About* card: the properties that matter, grouped by
  property group, values editable in place. **Lifecycle stage and lead status live here**, not in a header banner.
- **Middle column** — tabs: *About* (journey overview, Breeze summary, key properties, signals), *Activities*
  (chronological timeline, upcoming at top), *Catch-up* (AI insights, health, **data quality**), *Revenue*,
  *Intelligence*.
- **Right sidebar** — *Associations* previews (Deals, Companies, Tickets…) and *Attachments*. Nothing editable of substance.

So: **status/stage = left rail. Properties = left rail. Activity = middle. Related records = right rail.**
Left/middle are customizable, up to 50 cards each ([customize records](https://knowledge.hubspot.com/object-settings/customize-records)).

## 2. Inline editing and the "missing data" affordance

- **HubSpot**: hover a property → edit icon → edit in place in the sidebar card; the long tail sits behind
  *Actions → View all properties* / *View property history* ([source](https://knowledge.hubspot.com/records/work-with-records)).
- **Salesforce**: pencil icon per field; clicking one puts **every** updateable field on the layout into edit mode
  with Cancel/Save — a form commit, not a per-field commit. Required styling only applies if the field is required
  on the *object* ([LWC record-form docs](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-record-form.html?type=Specifications)).
- **Attio**: attributes are edited directly in the cell, in table and on the record; sections are configurable
  ([configure record pages](https://attio.com/help/reference/managing-your-data/records/configure-record-pages)).
- **Completeness affordance — yes, and it has a name.** HubSpot's *Catch-up* tab has a **data quality** section that
  "displays key properties with missing values (e.g., Phone number) and any detected duplicates"
  ([source](https://knowledge.hubspot.com/records/understand-the-default-record-layout?region=france)). The *Intelligence*
  tab shows an **enrichment prompt at the top** when properties are missing or wrong
  ([source](https://knowledge.hubspot.com/records/use-the-intelligence-tab)). Note the pattern: gaps are surfaced in a
  **dedicated panel**, never as scattered red asterisks on the record. No blocking required-field gate on the record page.

## 3. AI-inferred vs human-entered — **there is no strong convention.** Say it plainly.

Nothing in HubSpot's or Salesforce's record docs marks an individual field as AI-guessed. The prior art instead
uses **review-before-write**, so provenance stops mattering after the write:

- **HubSpot Breeze**: enrichment happens in the Intelligence tab — *Enrich record* → right panel lists candidate
  properties, all pre-checked, **you de-select the ones you want to keep**, then it writes
  ([source](https://knowledge.hubspot.com/records/use-the-intelligence-tab)). After the write the value looks like any other.
- **Attio** is the only citable per-value provenance UI found: for the web-research autofill, "a small colored dot appears
  next to each result to indicate how confident the agent is" (green/amber/red), and hovering reveals "the agent's
  reasoning and the web sources it used" ([AI attributes](https://attio.com/help/reference/attio-ai/ai-attributes)).
  The research agent returns "confidence ratings, detailed reasoning, and full citations"
  ([changelog](https://attio.com/changelog/2026/web-research-agent)).
  *(A secondary review claimed lilac cells + a sparkle in column headers; I could not verify it on Attio's own pages — treat as unconfirmed.)*
- **Design-system level**, the emerging (not yet standard) suggestion pattern is: suggestion + confidence indicator +
  explanation toggle + accept/reject + feedback ([AI UX patterns for design systems](https://thedesignsystem.guide/blog/ai-ux-patterns-for-design-systems-(part-1)),
  [Supernova roundup](https://www.supernova.io/blog/top-6-examples-of-ai-guidelines-in-design-systems)).

**Verdict for Massar: the confidence-dot + hover-reasoning-and-source pattern is the only proven per-field
provenance affordance in a real CRM. Copy it. The sparkle icon is not an established CRM field-level convention.**

## 4. Messaging-first CRMs — closer to Massar than HubSpot is

| | stage shown as | where you edit it | field UI | graded fit for Massar |
|---|---|---|---|---|
| **Wati** | `Lead stage` attribute, 6 defaults (New lead → Contacted → Qualified → Proposal sent → Deal won/lost); New/Won/Lost undeletable ([src](https://support.wati.io/en/articles/12264879-understanding-contact-owner-and-lead-stage-attributes)) | one dropdown in contact view | flat attribute list | **full** — a 6-stage sorter, same shape as ours |
| **Kommo** | stage in the lead card's left "about" snapshot alongside contact info + tags; feed carries stage-change events ([src](https://www.kommo.com/support/crm/leads/)) | in the card; chat sits at its bottom | grouped fields | **high** — record *is* the conversation |
| **respond.io** | Lifecycle stage, toggled visible in Inbox and Contacts ([src](https://respond.io/help/workspace-settings/workspace-settings-lifecycle)) | contact-details panel; name edits inline | standard then custom fields, **tags at the bottom**, merge suggestions inline ([src](https://respond.io/help/contacts/contact-details)) | **high** |
| **Trengo** | custom fields in the profile/contact sidebar, can be marked *Required* ([src](https://help.trengo.com/article/custom-fields-explained)) | sidebar | flat | partial |
| **HubSpot** | lifecycle stage as one property in a left-rail card | left rail | 50 cards, tabs | partial — too much chrome |

**What they do that HubSpot does not:** stage is a *single dropdown you can reach without leaving the thread*; the
transcript is the record, not a tab; tags carry qualitative interest and sit at the bottom as a chip row; duplicate/merge
prompts appear in the panel itself. **What none of them do:** distinguish AI-written from human-written fields at all.

## 5. Reuse-or-build

- **Reuse wholesale (3 patterns):** (1) HubSpot's **region contract** — identity+stage+key properties in one rail,
  timeline in the middle, associations opposite; (2) HubSpot's **gaps-in-one-panel** rule instead of per-field error
  decoration — a "what's missing" card, which is exactly the CPO's "better indicators to enrich them";
  (3) **Attio's confidence dot + hover reasoning/sources** for every LLM-inferred field.
- **Build (no adequate prior art):** a **provenance token on the field itself** — tool-written fact vs LLM inference vs
  human-confirmed — because every platform above dodges this by committing AI values through a review panel and then
  forgetting. Massar's agent writes continuously, so review-before-write does not apply; we need after-the-fact marking.
  Also build: interest level derived from the transcript (Wati/Kommo leave it to manual tags).
- **Actively wrong for a 6-stage WhatsApp sorter:** HubSpot's 50-card, 5-tab, association-heavy record (we have no deals
  or companies — the right rail has nothing to hold); Salesforce's whole-form edit mode (a stage change must be one tap);
  and any required-field gate on stage transition — the agent must be able to advance a contact on partial data.
- **RTL flags:** HubSpot's own CRM still lacks full RTL/Arabic interface support
  ([HubSpot Ideas thread](https://community.hubspot.com/t5/HubSpot-Ideas/RTL-right-to-left-amp-amp-rich-text-functionality/idi-p/38023)) —
  **there is no Arabic reference implementation of any of this; we mirror it ourselves.** Direction-dependent bits to flip:
  the "left rail" becomes the **right** rail (start-side); the confidence dot sits on the *start* side of the value;
  stage progress chevrons/funnels must reverse; Latin phone numbers and URLs inside Arabic field values need bidi
  isolation or they will render scrambled. Timelines (newest/upcoming at top) are direction-neutral.

**Unverified / open question:** whether Attio's confidence dot persists after the value is written or only during the
autofill run — the help page does not say. Assume the former, design for both.
