#!/usr/bin/env python3
"""Render project-authored Markdown primers to downloadable PDFs."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "original" / "CA11-accounting-foundations.md"
output = ROOT / "assets" / "pdfs" / "CA11-accounting-foundations-original.pdf"
output.parent.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CPAHead", parent=styles["Heading1"], textColor=colors.HexColor("#702536"), spaceBefore=14))
styles.add(ParagraphStyle(name="CPABody", parent=styles["BodyText"], leading=15, spaceAfter=7))
document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=55, rightMargin=55, topMargin=55, bottomMargin=55, title="CA11 Accounting Foundations — Certiprep Original Primer")
story = []
for line in source.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        story.append(Spacer(1, 6))
    elif line.startswith("#"):
        story.append(Paragraph(escape(line.lstrip("# ")), styles["CPAHead"]))
    else:
        story.append(Paragraph(escape(line).replace("**",""), styles["CPABody"]))
document.build(story)
print(output)
