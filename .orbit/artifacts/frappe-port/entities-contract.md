# Entities contract — tasks · notes · assignment (frappe-port)

Source: `crm/fcrm/doctype/crm_task/crm_task.json`, `crm/fcrm/doctype/fcrm_note/fcrm_note.json`,
`crm/api/activities.py:479` (`get_linked_tasks` filters on `reference_docname` only).
Target: `massar-engine/src/db.ts` MIGRATION block — append at the END, `CREATE TABLE IF NOT EXISTS`,
later columns via `ALTER TABLE … ADD COLUMN IF NOT EXISTS` placed immediately after their CREATE
(the whole schema is ONE simple query; a misplaced ALTER aborts every statement after it).

## 1. DDL

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id          BIGSERIAL PRIMARY KEY,
  title       TEXT   NOT NULL,                       -- Frappe: reqd
  description TEXT,                                  -- NULL → «—»
  status      TEXT   NOT NULL DEFAULT 'todo'
              CHECK (status IN ('backlog','todo','in_progress','done','cancelled')),
  priority    TEXT   CHECK (priority IN ('low','medium','high')),  -- NULL is legal → «—»
  due_at      BIGINT,                                -- epoch ms, like every table here
  ref_kind    TEXT   NOT NULL CHECK (ref_kind IN ('contact','campaign')),
  ref_id      TEXT   NOT NULL,                       -- phone (contact) | campaigns.id::text
  created_at  BIGINT NOT NULL,
  updated_at  BIGINT NOT NULL,
  created_by  TEXT   NOT NULL DEFAULT 'اللوحة',      -- label, not identity (§4)
  done_at     BIGINT                                 -- set ONLY when status→done; never inferred
);
CREATE INDEX IF NOT EXISTS idx_tasks_ref ON tasks(ref_kind, ref_id);
CREATE INDEX IF NOT EXISTS idx_tasks_open ON tasks(status, due_at);

CREATE TABLE IF NOT EXISTS notes (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT,                                   -- Frappe reqd; Massar NULL → «—» (§ no invented values)
  content    TEXT   NOT NULL,                        -- plain text/markdown, NOT html
  ref_kind   TEXT   NOT NULL CHECK (ref_kind IN ('contact','campaign')),
  ref_id     TEXT   NOT NULL,
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  created_by TEXT   NOT NULL DEFAULT 'اللوحة'
);
CREATE INDEX IF NOT EXISTS idx_notes_ref ON notes(ref_kind, ref_id);
```

**users — DO NOT CREATE.** See §4.

Dropped from Frappe, with reason:
| Dropped | Why |
|---|---|
| `assigned_to` (Link→User) | no user table, one operator (§4) |
| `start_date` | Massar has no scheduling/gantt view; a start date nobody reads is invented data |
| `reference_doctype` (Link→DocType) | Massar has 2 linkables, not N doctypes; replaced by `ref_kind` |
| `owner`, `modified_by`, `_assign`, `_liked_by`, `_comments`, `share`, permissions/roles | no auth beyond ADMIN_TOKEN |
| Text-Editor HTML for `description`/`content` | RTL plain text; no sanitizer in the engine today |

## 2. Enumerations (one table, both directions — the "emitted values must be readable" rule)

Export ONE map per enum from `src/taskEnums.ts`; `db.init()` asserts its keys equal the CHECK list at
boot. The UI never hardcodes an Arabic string.

| status (stored) | Arabic label | | priority | Arabic label |
|---|---|---|---|---|
| `backlog` | مؤجَّلة | | `low` | منخفضة |
| `todo` | للتنفيذ | | `medium` | متوسطة |
| `in_progress` | قيد التنفيذ | | `high` | عالية |
| `done` | منجزة | | `NULL` | — |
| `cancelled` | ملغاة | | | |

Spelling is fixed once: stored `cancelled` (Frappe writes `Canceled`); the port maps on read.
Dates/counts render in Arabic-Indic numerals — `npm run check:numerals` must stay green.

## 3. Reference / link model

Two columns, `(ref_kind, ref_id)`, `ref_id` always TEXT because contacts are phone-keyed (TEXT) and
campaigns are BIGSERIAL. **No foreign key** — matching `campaign_targets`, which has none, and
avoiding the real failure: a task on an imported `entities` phone that has no `contacts` row yet
would 500 on insert. Consequences that MUST be implemented:
- Write path validates the ref exists (`contacts.phone` OR `entities.phone` for contact;
  `campaigns.id` for campaign) and returns `400 {error:"unknown_ref"}` if not. Never auto-creates.
- Read path resolves the ref for display; an unresolvable ref renders «سجل محذوف», never a guess.
- `deleteEntity` / campaign delete must `DELETE FROM tasks/notes WHERE ref_kind=$1 AND ref_id=$2`
  in the same call — otherwise orphans accumulate silently.

## 4. Assignment with one operator — verdict: **do not build a users table.**

There is one operator and one ADMIN_TOKEN. A `users` table would hold exactly one row whose only
consumer is a dropdown with one option; every "assigned to" badge would be a decoration, and the
first multi-user story will change its shape anyway. `src/index.ts:96` already states this
(assumption A-3: the token is the authorization, the name is only a label).

Minimum honest version: `created_by TEXT NOT NULL DEFAULT 'اللوحة'`, taken from the existing
`byLabel(req)` helper (`req.body.by`, ≤60 chars). It records who typed it; it claims nothing else.
Replacement for assignment in the UI: the record tab shows **حالة** + **موعد الاستحقاق** (status +
due date) — the two fields that actually change behaviour — and no "المسؤول" field at all. An empty
assignee column is worse than an absent one.

MUST NOT be built now: `users` table, login/session, roles/permissions, `_assign` JSON arrays,
multi-assignee, notification-on-assign, task comments, mentions, attachments, reminders, recurrence,
activity/audit feed, HTML rich text.

## 5. API surface (all endpoints require `x-admin-token`; `adminOk()` → 401 otherwise)

| Method | Path | Body / Query | Response |
|---|---|---|---|
| GET | `/admin/tasks` | `?contact=<phone>` \| `?campaign=<id>` \| `?status=` (omit all → all) | `{tasks:[Task]}` newest-first, `done`/`cancelled` last |
| POST | `/admin/tasks` | `{title, ref_kind, ref_id, description?, status?, priority?, due_at?, by?}` | `201 {task}` · `400 {error:"title_required"\|"unknown_ref"\|"bad_status"}` |
| PATCH | `/admin/tasks/:id` | any subset of the above; `{}` → 400 | `{task}` · `404` |
| DELETE | `/admin/tasks/:id` | — | `{deleted:true}` · `404` |
| GET/POST/PATCH/DELETE | `/admin/notes[/:id]` | same shape, `{content, title?, ref_kind, ref_id, by?}`; content required | as above |

`Task = {id, title, description|null, status, statusLabel, priority|null, priorityLabel|null,
due_at|null, ref_kind, ref_id, refLabel|null, created_at, updated_at, created_by, done_at|null}`.
Writes go through a transactional path that **throws** on a dead pool (the `upsertProps` precedent) —
a typed human record must never be fire-and-forget; the panel returns 503 «أعد المحاولة» honestly.
`status:'done'` stamps `done_at`; moving off `done` clears it.

## 6. Acceptance criteria

1. `db.init()` on an EMPTY database creates `tasks` and `notes` and logs `connected + migrated`.
   *Evidence:* fresh Postgres, `\dt` shows both; `/health` `ok:true`.
2. Re-running `init()` on the existing production schema is a no-op with zero errors.
   *Evidence:* deploy log free of `init failed`; `counts()` unchanged.
3. Boot asserts every enum key against the CHECK list; a mismatch fails loudly at boot, not at render.
   *Evidence:* unit test flips one label key → boot throws.
4. `POST /admin/tasks` with an unknown `ref_id` returns 400 and inserts nothing.
   *Evidence:* curl + `SELECT COUNT(*)` unchanged.
5. Every endpoint without `x-admin-token` returns 401.
   *Evidence:* one curl per route, all 401.
6. A task with `priority` NULL and `due_at` NULL renders «—» in both cells — no default, no guess.
   *Evidence:* QA screenshot of the record tab at 3 viewports.
7. Deleting a contact/campaign leaves zero tasks or notes pointing at it.
   *Evidence:* `SELECT` after delete returns 0 rows.
8. All dates and counts on the tasks/notes tabs are Arabic-Indic. *Evidence:* `npm run check:numerals` exits 0.
9. `npm run build` exits 0 (strict TS) and `npm run smoke` exits 0 — the record page renders, not blank.

**Assumptions (labelled, unverified):** A-3 one operator (from `src/index.ts:96`); notes are plain
text because no sanitizer exists; `entities.phone` counts as a valid contact ref. Any of these
turning false changes §3 or §4 and should re-open this contract.
