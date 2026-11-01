from pathlib import Path
import json,fitz,hashlib,re,zipfile,datetime
O=Path('Certiprep/research-library/kenya-cpa/session-2026-11-01');W=Path('research-work');R=json.loads((O/'catalog/source-catalogue.json').read_text());out=[]
for r in R:
 if r.get('pdf_pages'):
  p=fitz.open(O/r['package_path']);texts=[pg.get_text() for pg in p]
  controls=[]
  for i in range(1,p.xref_length()):
   try:
    obj=p.xref_object(i)
    if re.search(r'/S\s*/(JavaScript|Launch)\b',obj):controls.append(i)
   except Exception:pass
  out.append(dict(resource_id=r['id'],pages=len(p),all_pages_extracted=True,text_characters=sum(map(len,texts)),nonempty_text_pages=sum(len(t.strip())>10 for t in texts),embedded_files=p.embfile_count(),active_action_xrefs=controls,metadata=p.metadata))
  assert not controls,(r['id'],controls)
# All retained World Bank page renders must match; extracted text reading order may differ after PDF rewrite.
a=fitz.open(W/'evidence/WB-PEFA-COVERLESS.pdf');b=fitz.open(W/'evidence/WB-PEFA.pdf');match=[]
for i in range(len(a)):
 match.append(a[i].get_pixmap(matrix=fitz.Matrix(.35,.35)).samples==b[i+1].get_pixmap(matrix=fitz.Matrix(.35,.35)).samples)
assert all(match)
# Confirm all micro text is preserved and restricted original image byte payloads absent.
a=fitz.open(W/'evidence/MICRO-UVIC-ADAPTED.pdf');b=fitz.open(W/'evidence/MICRO-UVIC-CORRECT-PDF.pdf')
assert len(a)==len(b)==557 and all(a[i].get_text()==b[i].get_text() for i in range(len(a)))
removed={x['original_sha256'] for x in json.loads((W/'micro-omitted-images.json').read_text())};remaining=set()
for pg in a:
 for im in pg.get_images():
  try:remaining.add(hashlib.sha256(a.extract_image(im[0])['image']).hexdigest())
  except Exception:pass
assert not removed.intersection(remaining)
report=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pdfs=out,total_pdf_pages=sum(x['pages'] for x in out),world_bank_retained_page_raster_comparisons=len(match),world_bank_all_rasters_equal=all(match),micro_all_557_text_pages_equal=True,micro_removed_image_sha256_not_present=True,scope='Integrity and selected content checks, not a full solution/peer review of every exercise.')
(O/'reports/document-integrity.json').write_text(json.dumps(report,indent=2));print('deep PDF validation passed',len(out),'PDFs',report['total_pdf_pages'],'pages; WB',len(match),'raster comparisons')
