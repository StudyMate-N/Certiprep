# Scripts

`verify_library.py` is the portable standard-library verifier for the extracted ZIP. It checks all manifest hashes, acquired catalogue paths, PDF signatures, ZIP CRCs, Git LFS pointer signatures and missing/remote HTML media. Run it from any directory with Python 3.

The `prepare_*.py` and `qa_examples.py` files preserve the actual session transformation/check recipes. They assume the original scratch `research-work/` layout, downloaded source names, and (for PDF/HTML preparation) PyMuPDF/lxml. They are audit evidence, not one-command acquisition tools for this extracted archive. Original restricted PDFs and omitted artwork are deliberately not bundled. The catalogue/request register records how sources were acquired; do not re-download/re-distribute a changed edition without a fresh rights check.

The numerical spot checks are intentionally limited; they are not a full test suite certifying every exercise or exam outcome. No automatic download of paid holdings, videos or KASNEB past papers is provided.
