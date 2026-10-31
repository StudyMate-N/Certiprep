# Kenya CPA media acquisition status — 31 October 2026

## What is in the repository?
- Source metadata, references, video discovery links, an original CA11 primer and its PDF generation script.
- Git LFS pointer for `assets/pdfs/CA11-accounting-foundations-original.pdf` (the GitHub API response does not include the PDF file's binary bytes).
- No third-party videos or PDFs confirmed as hosted binaries.

## Verification rules
- Do not count a source URL as an acquired file.
- Do not count an LFS pointer as a verified PDF until successful LFS retrieval and `%PDF-` header checks.
- Use `python research-library/kenya-cpa/scripts/audit_library.py` after checkout with `git lfs pull`.
- Keep all third-party copyrighted sources link-only unless redistribution/hosting permission is established.
- Keep the specific exam-version date on all law and tax material.
- Before commercial distribution of MIT OCW materials, obtain permission separately; CC BY-NC-SA does not permit standard paid-course reuse.

## Immediate next gates
1. Verify original CA11 PDF is available via Git LFS download.
2. Obtain redistribution permission for official past papers or link users to KASNEB.
3. Record individual video titles, channels, durations, syllabus outcomes and rights, not just search result pages.
4. Acquire additional genuinely redistributable textbooks and original course materials.
