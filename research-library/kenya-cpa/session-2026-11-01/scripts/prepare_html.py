from pathlib import Path
from lxml import html,etree
import json,urllib.parse,hashlib,shutil,copy,re
ROOT=Path(__file__).resolve().parent.parent;W=ROOT/'research-work';O=ROOT/'Certiprep/research-library/kenya-cpa/session-2026-11-01'
style='body{max-width:920px;margin:2rem auto;padding:0 1.2rem;font:18px/1.65 system-ui;color:#152a35;background:#fff}h1,h2,h3{line-height:1.2}img{max-width:100%;height:auto}table{border-collapse:collapse;display:block;max-width:100%;overflow:auto}td,th{border:1px solid #bbc;padding:.35rem .55rem}pre{overflow:auto;background:#eef3f5;padding:1rem}blockquote{border-left:3px solid #bbc;padding-left:1rem}.provenance{font-size:.86rem;background:#edf3ef;border:1px solid #bccdc2;padding:1rem;margin-bottom:2rem}.omitted{font-size:.82rem;color:#65727b;font-style:italic}a{color:#165c8c}'
manifest=[]
def safe_export(source,title,url,dest,author,license='CC BY 4.0',images=None,note='',remove_quotes=False,selector='//main'):
 raw=source.read_bytes();d=html.fromstring(raw);found=d.xpath(selector);b=copy.deepcopy(found[0] if found else d)
 for bad in b.xpath('.//script|.//style|.//iframe|.//object|.//embed|.//form|.//button|.//input|.//video|.//audio|.//svg|.//nav'):
  bad.drop_tree()
 for e in b.iter():
  for a in list(e.attrib):
   if a.startswith('on') or a in ['srcset','style','integrity','crossorigin']:del e.attrib[a]
 for a in b.xpath('.//a[@href]'):
  u=a.get('href')
  if u.lower().startswith(('javascript:','data:')):a.attrib.pop('href',None)
  elif not u.startswith('#'):a.set('href',urllib.parse.urljoin(url,u))
 used=[];omitted=[]
 for im in list(b.xpath('.//img')):
  u=urllib.parse.urljoin(url,im.get('src',''))
  if images and u in images:
   local=images[u];im.set('src','images/'+local.name);used.append(u)
  else:
   omitted.append(u);span=html.Element('span',{'class':'omitted'});span.text='[Illustration omitted in this offline edition; see the linked source.]';im.getparent().replace(im,span)
 if remove_quotes:
  for q in list(b.xpath('.//blockquote')):
   q.text='[Third-party quoted passage omitted; consult the original source.]'
   for child in list(q):q.remove(child)
 body=html.tostring(b,encoding='unicode',method='html')
 attrib=f'Derived from {title} by {author}. Source: {url}. Licence: {license}. Changes: website navigation/scripts removed; external media not bundled. {note}'
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' data:; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>'+__import__('html').escape(title)+'</title><style>'+style+'</style><body><div class="provenance">'+__import__('html').escape(attrib)+' <a href="https://creativecommons.org/licenses/by/4.0/">Licence details</a></div>'+body+'</body></html>'
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
 manifest.append({'source':url,'source_sha256':hashlib.sha256(raw).hexdigest(),'package_path':str(dest.relative_to(O)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'title':title,'included_image_urls':used,'omitted_image_urls':omitted,'changes':attrib})
# Cost accounting: preserve original educational diagrams but omit decorative and uncleared external imagery.
rows=list(map(json.loads,(W/'cost-image-progress.jsonl').read_text().splitlines()));skip={'COST-IMG-'+str(n).zfill(3) for n in [1,2,6,12,13,19,27,44,75,90,91,111]}
imap={}
for r in rows:
 if r['id'] in skip:continue
 p=Path(r['local_path']);dest=O/'media/Intermediate/CA25/open-cost-accounting/images'/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);imap[r['url']]=dest
for p in sorted((W/'evidence').glob('COST*.html')):
 d=html.fromstring(p.read_bytes());title=d.xpath('string(//h1)');n=int(p.stem[-2:]);u=f'https://www.opencostaccounting.org/toc/chapter{n}/'
 safe_export(p,'Open Cost Accounting: '+title,u,O/f'media/Intermediate/CA25/open-cost-accounting/chapter{n:02}.html','Brian D. Knox',images=imap,note='Decorative photographs, portraits, tombstone image and unverified map omitted. Teaching diagrams retained under the author site licence.',selector='//article')
# Communication exports deliberately exclude images, embeds and quoted third-party passages.
q={x['id']:x for x in json.loads((W/'queue-comm.json').read_text())}
for sec in ['9.2','9.5','9.6','10.2','10.3','11.1']:
 x=q['COMM-'+sec];safe_export(W/('evidence/COMM-'+sec+'.html'),'Communication Essentials for Business: '+x['title'],x['url'],O/('media/Foundation/CA12/communication/section-'+sec.replace('.','-')+'.html'),'Suzan Last; Robin L. Potter; Tricia Nicola Hylton and credited contributors',note='Selected chapter text only; images, embedded media and block quotations omitted. The complete source book is not cleared for commercial redistribution.',remove_quotes=True,selector='//section[contains(@class,"chapter")] | //div[contains(@class,"ugc")]')
# Full lesson text and exercises, with source ZIPs containing pinned figures/data/code.
for k,repo in [('PY','swcarpentry/python-novice-gapminder'),('SHEET','datacarpentry/spreadsheet-ecology-lesson'),('SQL','swcarpentry/sql-novice-survey')]:
 safe_export(W/f'evidence/CARP-{k}-AIO.html',{'PY':'Plotting and Programming in Python','SHEET':'Data Organization in Spreadsheets','SQL':'Databases and SQL'}[k],'https://'+{'PY':'swcarpentry.github.io/python-novice-gapminder','SHEET':'datacarpentry.github.io/spreadsheet-ecology-lesson','SQL':'swcarpentry.github.io/sql-novice-survey'}[k]+'/aio.html',O/f'media/Practical/CA35P/data-skills/{k.lower()}-lesson.html','The Carpentries and credited contributors',note='Illustrations omitted from this text view; pinned source ZIP contains original lesson source, figures, code and available data. Embedded code licence is MIT.',selector='//main')
(O/'catalog/html-adaptations.json').write_text(json.dumps(manifest,indent=2))
print('offline HTML pages',len(manifest),'cost diagrams',len(imap),'omitted cost decorative objects',len(skip))
