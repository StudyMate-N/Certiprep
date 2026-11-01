from pathlib import Path
import json,hashlib,csv
O=Path('Certiprep/research-library/kenya-cpa/session-2026-11-01');W=Path('research-work');R=json.loads((O/'catalog/source-catalogue.json').read_text());E=[json.loads(s) for s in (W/'fetch-events.jsonl').read_text().splitlines()];byhash={x.get('sha256'):x for x in E};paths={r['package_path']:[r['id']] for r in R if r['local_media_present']}
for r in R:
 for p in r.get('supplemental_package_paths',[]):paths[p]=[r['id']]
images={}
for h in json.loads((O/'catalog/html-adaptations.json').read_text()):
 for u in h['included_image_urls']:images.setdefault(u,[]).extend(paths.get(h['package_path'],[]))
rows=[]
for p in sorted((O/'media').rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(O).as_posix();b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();ev=byhash.get(sha,{});ids=paths.get(rel,images.get(ev.get('url'),[]));assert ids,('Unowned asset',rel)
 rows.append(dict(path=rel,bytes=len(b),sha256=sha,resource_ids='|'.join(sorted(set(ids))),source_url=ev.get('url','See resource catalogue and HTML adaptation register for derivative source'),kind='supporting_diagram' if '/images/' in rel else 'source_zip' if p.suffix=='.zip' else 'pdf' if p.suffix=='.pdf' else 'offline_html',is_lfs_pointer=b.startswith(b'version https://git-lfs.github.com/spec/v1'),github_media_present=False))
with (O/'catalog/file-manifest.csv').open('w',newline='') as f:w=csv.DictWriter(f,rows[0]);w.writeheader();w.writerows(rows)
(O/'catalog/file-manifest.json').write_text(json.dumps(rows,indent=2));print('media assets',len(rows),'bytes',sum(r['bytes'] for r in rows),'supporting diagrams',sum(r['kind']=='supporting_diagram' for r in rows))
# Preserve concise original-author HTML rights evidence, with actual source artifact hashes.
evidence=json.loads((O/'rights/licence-evidence.json').read_text())
from lxml import html
for key in ['MCM-GENLETT','MCM-PROPS','MCM-FEAS','MCM-ORAL']:
 p=W/f'evidence/{key}.html';d=html.fromstring(p.read_bytes())
 for e in d.xpath('//script|//style'):e.drop_tree()
 t=' '.join(d.text_content().split());evidence.append(dict(id=key,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),verbatim_notice=t[t.rfind('Information and programs provided'):],licence_links=d.xpath('//a[contains(@href,"creativecommons.org/licenses")]/@href')))
(O/'rights/licence-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
