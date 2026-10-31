# Kenya CPA Research Library

**Status:** acquisition staging — metadata and source pointers only; **zero external PDF/video assets uploaded**.

## Scope
KASNEB CPA Foundation, Intermediate and Advanced papers. Kenyan law, tax and exam syllabuses override international supplemental teaching sources.

## Structure
- `catalog/resources.csv` — verified source leads; URLs are source pages unless marked direct PDF
- `catalog/videos.csv` — video teaching discovery; URLs are external, not downloaded media
- `assets/pdfs/` — put actual authorised PDF files here after rights checks
- `assets/videos/` — use Git LFS only for files with explicit hosting rights; otherwise external streaming URLs
- `rights/` — permission and provenance records before distribution
- `scripts/` — ingestion and validation scripts (future)

## Acquisition policy
1. Check each PDF/video URL, edition, target paper and author.
2. Record source URL, publisher, effective date, license, use permission, SHA256, size and file path.
3. **No reproduction of KASNEB past papers, proprietary IFRS texts, paid textbooks, or YouTube videos without permission.**
4. MIT OCW is commonly CC BY-NC-SA; it is not cleared for a paid exam tool.
5. Content status values: `discovered`, `downloaded`, `verified`, `licensed_for_distribution`, `restricted_link_only`.
6. Keep local tax/legal materials current. External accounting lectures should be labelled supplemental rather than authoritative Kenyan exam teaching.

## GitHub storage
Ordinary Git warns for files above 50 MiB and blocks above 100 MiB; use Git LFS for authorised large binaries. Avoid treating GitHub as an unrestricted commercial video CDN.

Next step: ingest actual authorised binaries, validate hashes and map each to exact KASNEB syllabus objectives.
