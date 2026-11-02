# Current source catalogue — read-back-verifiable JSON shards

Dated **2 November 2026, 16:14 UTC**. The monolithic `../source-catalogue.json` crossed the GitHub Contents API's approximately 1 MiB inline-content threshold when the live source count reached 260. It remains preserved, but subsequent `fetch_file` calls may return no inline content even when the blob exists. **Do not interpret this as an empty catalogue or overwrite it.**

The 260 current canonical Supabase `cpa_library.resources` records were exported in sorted-ID order into two GitHub JSON shards:

- [Part 1](2026-11-02-1614Z-part-1.json): 130 records; first `AUDIT-CONESTOGA-INTERNAL`, last `STD-ICPAK-IFRSS1S2-READINESS-2026`.
- [Part 2](2026-11-02-1614Z-part-2.json): 130 records; first `STD-ICPAK-SUSTAINABILITY`, last `YT-YnkN9lV9kWQ`.

Both shards were **fetched again and parsed** after creation. Combined 260 distinct IDs exactly matched the live 260 sorted database IDs. These are catalogue metadata, not acquired media or a media archive. The standing CSV export also has 260 records. Future maintenance should work from live DB + the latest dated shards and create a new versioned shard set when records change, rather than repeatedly rewriting a >1 MiB monolith. Rights and academic acceptance remain independently gated.

## Incremental canonical addition — 2 November 2026, 17:18 UTC

[Two-record 2026-11-02-1718Z shard](2026-11-02-1718Z-incremental.json) extends the 260-record 16:14 UTC base shards to **262 canonical source decisions**. The two new IDs are `VIDEO-WB-KENYA-SME-TAX-2024` and `VIDEO-WB-REVENUE-RIGHT-2026`. The three shard files were independently read back and all **262 distinct IDs** matched live Supabase `cpa_library.resources` exactly; both source and rights CSV exports have 262 distinct rows. The preserved monolithic JSON predates this increment and must not be treated as the current canonical 262-record file. Neither these shards nor the metadata ZIP contains audiovisual bytes.

## Incremental canonical addition — 2 November 2026, 18:14 UTC

[One-record 2026-11-02-1814Z shard](2026-11-02-1814Z-incremental.json) extends the two 130-record 16:14 UTC base shards plus the two-record 17:18 UTC shard to **263 canonical source decisions**. New ID `VIDEO-ICPAK-IS-AUDIT-INDEX` groups overlapping ICPAK (11 lessons, 2 advertised free) and Bafunde (7 lessons, free with signup) IS-audit course indexes; no recordings acquired, dates or overlap verified. Current standing source/rights CSVs have 263 distinct IDs each. The original >1 MiB monolithic source JSON remains historical and untouched.

### Field-level overlay — 2 November 2026, 18:18 UTC

Apply [2026-11-02-1818Z-access-correction.json](2026-11-02-1818Z-access-correction.json) **by ID** after reading the historical base and incremental shards. It updates `VIDEO-IFRS18-WEBINARS2024` from partly gated to all three 2024 webinar watch links requiring sign-in. This overlay is **not** a new source ID; the canonical count remains 263. Preserve historical shard bytes and dated provenance. The current video-catalogue JSON already reflects the correction.

## Two 2026 Kenyan tax video metadata decisions — 2 November 2026, 19:17 UTC

The [two-record incremental shard](2026-11-02-1917Z-incremental.json) adds `VIDEO-CDH-FINANCEACT2026-POLICY` and `VIDEO-PKF-FINANCEACT2026-WEBINAR` to the previous 263 canonical IDs, yielding **265**. Apply the earlier IFRS 18 access overlay by ID; it remains a field correction, not a new source. Both entries are external-only metadata, with no recording downloads or new media hashes. Standing source and rights CSVs have 265 distinct rows each; the preserved monolithic source JSON remains historical.

## 2026-11-02T20:20:00Z increment

[Two-record external-only metadata shard](2026-11-02-2020Z-incremental.json) adds `VIDEO-CDH-KENYA-CORPORATE-GUIDE-2026`, `VIDEO-SGB-CA12-CLASS-2026` to the prior 265 canonical decisions, yielding **267**. Existing base shards, earlier incrementals and IFRS 18 access overlay are preserved. Standing source, rights and usage CSVs each reconcile to 267 distinct rows. Two blank action sets in the 19:17 usage export (CDH/PKF Finance Act videos) were restored from canonical Supabase records; no rights approval changed. No new acquired media.

## 2026-11-02T21:13Z incremental review

Two source decisions in `2026-11-02-2113Z-incremental.json`: one CPDbox IFRS3/10 ACCEPT_LINK with selected written-example arithmetic checked, and one CPDbox IFRS18 HOLD_ACCURACY over newly defined subtotals. Previous 267 IDs plus two distinct IDs = 269; the IFRS18 access overlay remains in force. No recordings downloaded; historical shards and >1 MiB monolith untouched. 2027 revised KASNEB syllabus PDF and transition circular not obtained.

## 2026-11-02T22:17:00Z increment

Two new external-only MIT Fall 2024 course records are in [2026-11-02-2217Z-incremental.json](2026-11-02-2217Z-incremental.json). Historical shards remain immutable. Canonical live count after verified sync: 271 distinct IDs; 154 accepted links, 94 video metadata, zero acquired recordings. The historical >1MiB monolithic JSON is not a current source of truth; current source CSV, rights exports and dated shards are reconciled with Supabase.
