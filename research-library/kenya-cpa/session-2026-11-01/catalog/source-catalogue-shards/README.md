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
