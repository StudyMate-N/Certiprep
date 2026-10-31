from pathlib import Path
import fitz,json,hashlib
p=Path('research-work/evidence/MICRO-UVIC-CORRECT-PDF.pdf');d=fitz.open(p)
omit={953,958,961,964,987,1010,1060,1076,1079,1083,1091,1104,1112,1141,1146,1204,1208,1214,1221,1256,1261,1274,1303,1345,1370,1477,1507,1525,1539,1555,1616,1635,1665,1682,1688,1771,1838,1861,1912,2017,2028,2066,2088,2232,2312,2326,2339,1866}
rows=[]
for x in sorted(omit):
 pages=[i+1 for i,pg in enumerate(d) if any(y[0]==x for y in pg.get_images(full=True))]
 b=d.extract_image(x)['image'];rows.append({'xref':x,'pdf_pages':pages,'original_sha256':hashlib.sha256(b).hexdigest(),'reason':'decorative photograph, portrait, advertisement or third-party icon omitted; external component rights not independently cleared for commercial redistribution'})
 if pages:d[pages[0]-1].delete_image(x)
meta=d.metadata;meta['subject']='Certiprep rights-reviewed adaptation: 48 third-party/decorative image objects omitted. Original text, teaching charts, attributions and pagination retained. See accompanying change log. CC BY 4.0 text; component licences as stated.';d.set_metadata(meta)
o=Path('research-work/evidence/MICRO-UVIC-ADAPTED.pdf');d.save(o,garbage=4,deflate=True)
# Ensure no omitted image payload survives in the saved PDF.
r=fitz.open(o);hashes=set()
for pg in r:
 for x in pg.get_images(full=True):
  try:hashes.add(hashlib.sha256(r.extract_image(x[0])['image']).hexdigest())
  except:pass
assert not ({x['original_sha256'] for x in rows}&hashes)
Path('research-work/micro-omitted-images.json').write_text(json.dumps(rows,indent=2));print('adapted',r.page_count,'pages','removed',len(rows),'objects','bytes',o.stat().st_size)
