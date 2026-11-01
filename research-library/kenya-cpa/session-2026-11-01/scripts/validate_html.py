from pathlib import Path
import json
from lxml import html
O=Path('Certiprep/research-library/kenya-cpa/session-2026-11-01');out=[]
for p in sorted((O/'media').rglob('*.html')):
 d=html.fromstring(p.read_bytes());bad=[]
 for tag in d.xpath('//script|//iframe|//object|//embed|//video|//audio|//form'):bad.append(tag.tag)
 for im in d.xpath('//img[@src]'):
  src=im.get('src') or ''
  if src.startswith(('http','//')) or not (p.parent/src).is_file():bad.append('image '+src)
 for el in d.iter():
  if any(k.startswith('on') for k in el.attrib):bad.append('event handler')
  if (el.get('href') or '').lower().startswith('javascript:'):bad.append('js href')
 t=' '.join(d.xpath('//body')[0].text_content().split());assert not bad,(p,bad)
 out.append(dict(path=str(p.relative_to(O)),body_characters=len(t),word_count=len(t.split()),unsafe_media=bad,licence_notice_present='CC BY 4.0' in t))
d=html.fromstring((O/'START_HERE.html').read_bytes());missing=[]
for u in d.xpath('//a/@href'):
 if u and not u.startswith(('http:','https:','#')) and not (O/u.split('#')[0]).is_file():missing.append(u)
assert not missing,missing
report=dict(html_pages=out,index_resource_cards=len(d.xpath('//article')),index_local_links_checked=True,browser_visual_test='Not performed: Chromium executable unavailable. HTML/content/local-path/no-remote-media checks passed.')
(O/'reports/offline-html-validation.json').write_text(json.dumps(report,indent=2));print('HTML pages',len(out),'cards',report['index_resource_cards'],'teaching words',sum(x['word_count'] for x in out))
