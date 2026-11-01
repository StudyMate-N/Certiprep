# Research capabilities and connection usage

Verified 1 November 2026 UTC. Use the minimum relevant capabilities and preserve working connections. No global permission settings were changed.

| Service / API | Verified state | Project use | Limits |
|---|---|---|---|
| GitHub | Connected; repository read/write/admin permission confirmed | Public StudyMate-N/Certiprep catalogue, provenance, policy, scripts, coverage and audit history | No credentials or uncleared media; no force push |
| Supabase | Connected; private cpa_library schema created and 144 resources / 162 asset metadata rows synchronized and read back | Queryable private catalogue, rights decisions, inventory, audit events and settings | Existing active project; CPA schema only; RLS/default deny; media bytes are not in the database |
| Public web research | Working search and primary-page retrieval | Academic authority, editions, syllabus, current Kenyan law/tax, licences and effective dates | Respect source access restrictions; retrieval is evidence, not redistribution permission |
| World Bank API | Actual native CSV ZIP, observations and series metadata acquired and cross-checked | Licensed Kenyan economic practice datasets with nulls, dates and provenance | Series-specific rights; do not assume all reports/data are CC BY |
| DOI/publisher and official repositories | Actual Springer, university, OPLA and author-hosted downloads verified | Exact editions, in-file permissions, source dates and actual teaching files | Check component credits; no universal publisher licence assumption |
| Library | Durable deliverable saving through supported file upload workflow | Verified master ZIP and portable catalogue snapshot | Save receipt required; links alone are not acquired media |
| Hourly automation | Existing CPA Library Continuous Review enabled | Bounded gap research, rights/currency checks, acquisition, catalogue/database maintenance and verified exports | Up to 40 minutes / 12 candidates / five approvals / 150 MiB; 50-minute non-overlap lease |
| Dropbox | Available, offered; account installation/authorization not confirmed | Optional archive mirror after a verified connection | Do not claim connected or upload until authorization completes |

## Skills and agent workflow

The personal skill **Maintain KASNEB CPA Library** codifies discovery, academic/rights checks, question-use boundaries, downloads/adaptations, grouped counts, database and archive verification. Its mechanical checker is tested against the live collection and a negative LFS fixture. A separate read-only forward check found stale manifest/report and counter weaknesses; release generation and verification now address them. Independent subject-expert review remains a separate completion gate.

Use the PDF skill for adaptations and visual checks, Supabase guidance for database changes, Library guidance for durable file delivery, and plugin management only for relevant missing integrations. Update project guidance and the personal skill when real work reveals repeatable gaps; validate changes before saving them.

The paused StudyMate-N Supabase project could not resume because of the active-free-project limit. No project was paused/deleted or upgraded. The active database hosts an isolated metadata catalogue; the approved file bytes are delivered in the verified archive. See session-2026-11-01/catalog/hosting.json for exact hosting verification and limitations.
