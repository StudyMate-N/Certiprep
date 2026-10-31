from pathlib import Path
import fitz,json,hashlib
w=Path(__file__).parent
s=w/'evidence/LOC-MACRO-PDF.pdf';d=w/'evidence/MACRO-ADAPTED.pdf'
p=fitz.open(s);keep=[2,3]+list(range(6,len(p)))
p.select(keep);p.set_metadata({'title':'Principles of Macroeconomics 3e, 2022 licensed edition - covers and promotional pages omitted','author':'David Shapiro; Daniel MacDonald; Steven A. Greenlaw; OpenStax contributors','subject':'CC BY 4.0 legacy edition; not a claim about later editions. Omitted original pages 1,2,5,6. See accompanying attribution.'});p.save(d,garbage=4,deflate=True)
q=fitz.open(s);a=fitz.open(d)
assert all(a[j].get_text()==q[i].get_text() for j,i in enumerate(keep))
print('macro derivative',len(a),d.stat().st_size)
a[20].get_pixmap(matrix=fitz.Matrix(.8,.8)).save(w/'qa/macro-adapted-sample.png')
(w/'macro-adaptation.json').write_text(json.dumps({'original_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'adapted_sha256':hashlib.sha256(d.read_bytes()).hexdigest(),'omitted_original_physical_pages':[1,2,5,6],'retained_original_physical_pages':[i+1 for i in keep],'text_comparison':'all retained pages exactly equal','reason':'Exclude covers and promotional branding; preserve copyright/licence and all instructional content.'},indent=2))
