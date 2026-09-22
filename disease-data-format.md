# How MediGuide already stores diseases and conditions

Reference for the seed work. Every rule below is taken from the code, with the
file it comes from, so the seed data can be validated before it is written.

## Tables

`backend/migrations/00048_disease_taxonomy.sql`

### `diseases` — the canonical clinical subject

| Column | Type | Rule |
|---|---|---|
| `id` | uuid | PK, `uuid_generate_v4()`; seeds supply deterministic UUIDs instead |
| `parent_id` | uuid | self-reference, `ON DELETE SET NULL`. **This is where a condition hangs off its disease** |
| `name` | text | 2–240 chars after trim |
| `normalized_name` | text | lookup key; trimmed, non-empty |
| `slug` | text | must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`, ≤ 240 |
| `short_name` | text | optional, ≤ 80 |
| `description` | text | optional, ≤ 10 000 |
| `icon` | text | optional, ≤ 120 — lucide names in existing data (`shield-alert`, `heart-pulse`) |
| `color` | text | optional, ≤ 80 — hex in existing data (`#C62828`) |
| `status` | text | `active` \| `inactive` \| `archived`, default `active` |
| `sort_order` | integer | ≥ 0; existing rows step by 10 |
| `created_by` / `updated_by` | uuid | → `users(id)` |
| `created_at` / `updated_at` / `deleted_at` | timestamptz | soft delete |

Indexes that constrain seed data:

- `idx_diseases_slug` — unique on `lower(slug)` where not deleted. **Slugs are globally unique**, not per-parent.
- `idx_diseases_active_normalized_name` — unique on `normalized_name` where not deleted and `status = 'active'`. **Two active diseases cannot share a normalized name.**

Trigger `trg_reject_disease_hierarchy_cycle` rejects a cycle, a missing parent,
and a new parent that is not `active`. So parents must be inserted before
children, and an inactive parent cannot take new children.

### `disease_aliases`

`disease_id`, `alias` (1–240), `normalized_alias`. Unique per
`(disease_id, normalized_alias)`.

### `disease_codes`

`disease_id`, `code_system` (1–80), `code` (1–120), optional `display_name` (≤ 240).
Unique on `(lower(code_system), lower(code))` **across all diseases** — one code
maps to at most one disease.

### `content_disease_assignments`

`backend/migrations/00049_...sql`. Links a disease to content:
`content_type` ∈ `guideline`, `outbreak`, `outbreak_document`, `situation_report`,
`algorithm`, `clinical_tool`, `form`, `drug_reference`; `is_primary` is unique per
`(content_type, content_id)`.

## Normalization (must be reproduced exactly)

`backend/internal/services/disease_service.go:512` — `normalizeDiseaseTerm`:
lowercase, keep Unicode letters and digits, collapse every other run to one
space, trim. `Ebola virus disease` → `ebola virus disease`; `COVID-19` → `covid 19`.

The extraction script mirrors this function, and derives the slug from the same
normalized string with spaces replaced by `-`.

## Service-level validation

`backend/internal/services/disease_service.go`

- `validateDiseaseFields` — the length/slug/status/sort-order rules above.
- `validateDiseaseIdentity` — rejects a name or alias that is ambiguous against
  another **active** disease's name or aliases.
- `normalizeDiseaseAliases` / `normalizeDiseaseCodes` — at most 100 of each per
  disease, no duplicates within the payload.
- `Archive` refuses a disease that still has non-archived children.

## Public exposure

`backend/internal/services/disease_public_service.go:239` — a disease appears in
the public/mobile directory **only if it, or a descendant, has published content**
(an active published hub, or a resource whose own service says it is public).
Seeding taxonomy alone adds classification targets; it does not add anything a
mobile user can browse until content is assigned.

## Where it is written today

| Path | What it writes |
|---|---|
| `backend/migrations/00048_disease_taxonomy.sql` | 7 active diseases + 8 aliases, fixed UUIDs `90000000-0000-4000-8000-0000000000NN` / `91000000-…` |
| `backend/cmd/seed/demo_disease_hubs.go` | re-upserts 6 of those, adds descriptions, icons, colours, 3 aliases, 6 ICD-10 codes, hubs, pillars, assignments |
| `backend/cmd/seed/ucg_disease_taxonomy.go` (`SEED_SCOPE=disease-taxonomy`) | the reviewed UCG taxonomy: 387 new diseases, 44 aliases, 281 ICD-10 codes, reusing the 5 curated rows it overlaps. Data lives in `backend/cmd/seed/fixtures/ucg-disease-taxonomy.csv`, whose `seed_action` column holds the review decision per row |

Seed conventions worth matching (`backend/cmd/seed/main.go`, `demo_disease_hubs.go`):

- rows are `map[string]any` passed to `upsertByID(database, "<table>", row)`, so a
  rerun updates rather than duplicates;
- IDs come from `demoID("<kind>", "<key>")` for derived rows, or fixed constants;
- `SEED_SCOPE` selects the scope in `cmd/seed/main.go:100`. `admin` and
  `facilities` are the only production-safe scopes today; `demo` is refused when
  `APP_ENV=production` unless `SEED_ALLOW_DEMO=true`.

## Already seeded — reconcile, do not duplicate

| Disease | UUID suffix | Slug | Codes present |
|---|---|---|---|
| Ebola virus disease | `…0001` | `ebola-virus-disease` | ICD-10 A98.4 |
| Malaria | `…0002` | `malaria` | ICD-10 B50-B54 |
| Cholera | `…0003` | `cholera` | ICD-10 A00 |
| Marburg virus disease | `…0004` | `marburg-virus-disease` | ICD-10 A98.3 |
| Measles | `…0005` | `measles` | ICD-10 B05 |
| Diabetes mellitus | `…0006` | `diabetes-mellitus` | — |
| Hypertension | `…0007` | `hypertension` | ICD-10 I10 |

The candidate set from the UCG hits four of these by name (`Malaria` 2.5.2,
`Measles` 2.3.3, `Hypertension` 4.1.6, `Cholera` 6.2.3) and one by a near miss
(`Diabetes Mellitus` 8.1.3 vs seeded `Diabetes mellitus` — same normalized name).
Those must reuse the existing UUIDs; inserting them again violates the unique
active normalized-name index. `Ebola and Marburg` (2.3.6.1) is a single UCG
section covering two existing diseases.

## The legacy `condition_name` field is a different thing

`medical_guidelines` (`backend/migrations/00003_consolidate_legacy_schema.sql:432`)
holds free-text clinical content keyed by `condition_name` plus an optional
`icd10_code`. `docs/disease-taxonomy-phase-1-2.md` calls it legacy and explicitly
not a reusable taxonomy, and `cmd/seed/main.go:1050` lists it among the tables the
seed skips. It is not the target for this work.
