# API contract — «المنتجات» V5 (backend ↔ frontend). Implements spec.md incl. Addenda v2 + v3.

Product names travel in QUERY or BODY (never as a path segment): names contain «/» («تكامل الأنظمة (HIS/ERP)»).
All endpoints: `x-admin-token`. New endpoints answer errors as `application/problem+json`
`{ type:"about:blank", title, status, detail, error:<code>, field?:<name> }` — the client reads `error`.
Every READ below first calls `db.canRead()` and answers 503 `{error:"db_unavailable"}` when unreachable.

## Reads
### GET /admin/products  (CHANGED — same path, richer shape; `products` keeps every old field)
```json
{
  "products": [{
    "product": "الإجازات المرضية",
    "sector": "قطاع المستشفيات", "sectorId": 1, "sectorAssumed": false,
    "owner": null, "pricingNote": "…",
    "packages": [{ "id": 1, "name": "الباقة القياسية", "listPrice": 18000, "years": 1, "scope": "فرع واحد" }],
    "retiredPackageCount": 0,
    "archived": false, "archivedAt": null,
    "embedded": true,
    "eligible": true,
    "inAssistantKnowledge": false,
    "kb": { "state": "approved" , "source": "x.pdf", "approvedBy": "admin", "approvedAt": 1788000000000, "updatedAt": 1788000000000 },
    "draft": null,
    "asset": { "filename": "a.pdf", "publicId": "abc", "size": 123456, "updatedAt": 1788000000000 },
    "createdAt": 1788000000000
  }],
  "unmatched": [{ "name": "…", "kind": "kb", "filename": "x.pdf" }],
  "skill": { "publicId": "…", "filename": "lean-proposal-deck-v2.3.1-upload.zip" },
  "sectors": [{ "id": 1, "name": "قطاع المستشفيات" }]
}
```
- `kb.state`: `"approved"` (approved_at set, md non-empty) | `"legacy"` (md non-empty, approved_at NULL — NOT used by the assistant) | `"none"`.
- `draft`: `null` | `{ "source", "by", "at", "hash" }`.
- `embedded` = name ∈ SERVICE_CATALOGUE. `eligible` = isRuntimeEligible. `inAssistantKnowledge` = name ∈ agent's live hubKb products.
- `archived` products ARE included (client filters); `__*` names never appear anywhere.

### GET /admin/products/performance?year=2026  (NEW)
```json
{ "year": 2026, "byProduct": [{
  "product": "…",
  "achieved": 0, "wonLines": 0, "lostLines": 0,
  "openValue": 4200, "openLines": 1, "unpricedOpenLines": 0,
  "annualTarget": 34000, "targetQuarters": 1,
  "quarters": [{ "quarter": 1, "target": null, "achieved": 0 }, { "quarter": 2, "target": null, "achieved": 0 },
               { "quarter": 3, "target": 34000, "achieved": 0 }, { "quarter": 4, "target": null, "achieved": 0 }]
}]}
```
Definitions (spec G, G′): open = UNWEIGHTED priced open lines, all periods; achieved/quarter achieved = current stage won AND latest transition into won in the period; won/lost lines = current stage won/lost AND latest transition into that stage in the year; `annualTarget` = sum of entered quarter targets (null when none); `target` null = no target row.

### GET /admin/products/knowledge?product=X  (NEW)
`{ "product", "md", "mdHash", "state": "approved"|"legacy"|"none", "draftMd": null|"…", "draftHash": null|"…", "draftSource", "draftBy", "draftAt", "changeSummary": { "added": 12, "removed": 3 } | null }`
Hashes = hex SHA-256 of the exact UTF-8 text.

### GET /admin/products/impact?product=X  (NEW)
`{ "product", "embedded": true, "openLines": 2, "campaigns": 3, "targetedEntities": 12, "interestReadings": 23, "kb": true, "asset": true, "packages": 2, "targets": 1 }`
`interestReadings` = distinct phones in `interest_tags` for the product (excluding test contacts).

## Writes
- **POST /admin/products** `{ name, sectorId?, owner?, pricingNote?, firstPackage?: {name, listPrice, years, scope} }` → 201 + `Location: /admin/products?product=<enc>` + `{ ok:true, product:<row as in GET> }`. One transaction (tag + product_meta + package). Name via `normalizeProductName` → 400 `invalid_name` {field:"name", detail}; 409 `name_exists`. Then `agent.refreshKb()`.
- **PATCH /admin/products?product=X** `{ sectorId?: number|null, owner?: string|null, pricingNote?: string|null }` → `{ ok:true, product:<row> }`. Upsert product_meta; sending `sectorId` (even the same value) sets `sector_assumed=false`. owner ≤60, pricingNote ≤120 → 400 `invalid_field`. 404 `unknown_product`.
- **POST /admin/products/archive** `{ product, archived: boolean }` → `{ ok:true, archived, impact }`. 409 `embedded_product` for SERVICE_CATALOGUE names. Then `agent.refreshKb()`.
- **POST /admin/products/knowledge/approve** `{ product, draftHash }` → `{ ok:true }`; 409 `stale_draft` when the stored draft's hash ≠ draftHash; 404 `no_draft`. Atomic: md=draft_md, source=draft_source, approved_by=adminName, approved_at=now, clear draft. Then refreshKb.
- **POST /admin/products/knowledge/approve-current** `{ product, contentHash }` → `{ ok:true }`; 409 `stale_content`; 404 `no_knowledge`. Sets approved_by/at only. Then refreshKb.
- **POST /admin/products/knowledge/discard** `{ product }` → `{ ok:true }`; 404 `no_draft`.
- **POST /admin/products/reconcile** `{ from, to, kind: "kb"|"asset" }` → `{ ok:true }`; 404 `unknown_source`; 400 `invalid_target` (not an active non-reserved tag); 409 `target_has_kb|target_has_asset`. Atomic move preserving md/draft/provenance. Then refreshKb.
- **PATCH /admin/packages/:id** `{ name, listPrice, years, scope }` → `{ ok:true, package }`; integer listPrice ≥0; years int 1–10; name required ≤60; scope ≤120; 409 `name_exists` within product.
- **POST /admin/packages/:id/retire** (existing) `{ retire?: boolean }` — `retire:false` restores.
- **POST /admin/sales/targets** (CHANGED) `{ product, year, quarter, amount }` — `amount:null` deletes the row → `{ ok:true, deleted:true }`; amount integer 0…1e12.
- **POST /admin/kb/upload** (CHANGED) product REQUIRED (multipart field before file, or `?product=`); must be an active tag (400 `unknown_product` / `archived_product`); types .pdf .docx .pptx .xlsx .md .txt ≤15MB (400 `invalid_file`); writes DRAFT only; response `{ ok:true, product, draftHash, changeSummary }`. Extraction failure → 502 `extraction_failed`, existing draft/md untouched.
- **POST /admin/product-asset/upload** (CHANGED) for non-`__*` products: active tag, PDF magic bytes `%PDF`, ≤10MB (400 `invalid_file`); failed upload keeps the old asset; refreshKb after success. `__skill__` branch unchanged.
- **POST /admin/tags** (CHANGED) → `normalizeProductName` (400 `invalid_name`).
- **POST /admin/tags/rename** (CHANGED) `{from,to}`: normalize `to`; 409 `embedded_product` when `from` ∈ SERVICE_CATALOGUE; 409 existing; keeps the cascade; after commit rewrites in-memory tracker contacts `tags[].product` and runs refreshKb; response adds `{ counts: <impact of from> }`.
- **POST /admin/tags/delete** (CHANGED) → 409 `referenced` + `{ counts }` when referenced by any PRODUCT_NAME_TABLES table, entities.product_tags or interest_tags.
- **POST /admin/campaign/launch** (CHANGED) → when `product` supplied and not eligible: 400 `product_not_eligible` (before any send).
- **POST /admin/compose** (CHANGED) → 400 `not_eligible` for a non-eligible product.
- **POST /admin/opps** (CHANGED) → 400 `archived_product` for a new line on an archived product.

## Runtime (agent)
- `refreshKb()`: hub md only where `approved_at IS NOT NULL AND md <> ''` AND product is an active non-archived tag; assets only for eligible products; exclude `__*`.
- `composeOpener()` throws `not_eligible` for non-eligible products.
- `send_asset`: exact name, then `productlock.productOf`; the `includes` fallback is removed.
- export `runtimeKnowledgeProducts(): string[]` and `isEligibleNow(name): boolean`.
- Boot tag seeding: SERVICE_CATALOGUE only (kb names removed).

## Pure domain — src/product-domain.ts (unit-tested; serialised to the browser as PRODUCT_DOMAIN_JS like OPPS_DOMAIN_JS)
- `normalizeProductName(raw): { ok:true, name } | { ok:false, reason }` — collapse whitespace, trim, 1–60 chars, not `__*`, no `#` `?` `%`, last `/` segment ∉ {performance, pricing, targets, knowledge}.
- `RESERVED_SECTIONS`, `EMBEDDED_PRODUCTS` (= SERVICE_CATALOGUE values, injected as a constant).
- `isRuntimeEligible({ exists, archived, kbState, embedded })`.
- `readinessOf({ archived, kbState, hasDraft, embedded, hasAsset, hasPrice, eligible, loadFailed })` → `{ cells: [{key:"knowledge"|"asset"|"price"|"lock", state:"done"|"missing"|"pending"}], eligible, word, reason }` with the exact Arabic words of spec B/B′.
- `coveragePct(achieved, target)` → number|null (null when target is null or ≤0).
- `priceSummary(packages, pricingNote)` → `{ kind:"package"|"note"|"none", lowest?: {name, listPrice, years}, count }`.
