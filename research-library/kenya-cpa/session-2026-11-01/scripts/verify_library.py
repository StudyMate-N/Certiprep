#!/usr/bin/env python3
"""Verify the extracted master library using Python's standard library only."""
from pathlib import Path
import hashlib,json,sys,zipfile
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
errors=[];count=0;listed=set()
manifest=ROOT/'MANIFEST.sha256'
if not manifest.exists():sys.exit('MANIFEST.sha256 missing: this verifier requires the delivered ZIP, not metadata-only GitHub checkout.')
for line in manifest.read_text().splitlines():
 expected,rel=line.split('  ',1);listed.add(rel);p=(ROOT/rel).resolve()
 if not p.is_relative_to(ROOT.resolve()):errors.append('Unsafe manifest path '+rel);continue
 if not p.is_file():errors.append('Missing '+rel);continue
 b=p.read_bytes();count+=1
 if hashlib.sha256(b).hexdigest()!=expected:errors.append('SHA-256 mismatch '+rel)
 if b.startswith(b'version https://git-lfs.github.com/spec/v1'):errors.append('LFS pointer, not media: '+rel)
 if p.suffix.lower()=='.pdf' and not b.startswith(b'%PDF-'):errors.append('Not PDF '+rel)
 if p.suffix.lower()=='.zip':
  try:
   with zipfile.ZipFile(p) as z:
    if z.testzip():errors.append('Bad ZIP CRC '+rel)
    for n in z.namelist():
     if not n.endswith('/') and z.read(n).startswith(b'version https://git-lfs.github.com/spec/v1'):errors.append('LFS pointer in ZIP '+rel+':'+n)
  except zipfile.BadZipFile:errors.append('Not ZIP '+rel)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256'}
if actual!=listed:errors.append('Manifest paths differ from actual files: unlisted='+str(sorted(actual-listed))+', missing='+str(sorted(listed-actual)))
class Images(HTMLParser):
 def __init__(self):super().__init__();self.sources=[]
 def handle_starttag(self,tag,attrs):
  if tag in ['img','script','iframe','video','audio','source']:
   self.sources.extend(v for k,v in attrs if k=='src' and v)
for p in (ROOT/'media').rglob('*.html'):
 h=Images();h.feed(p.read_text())
 for src in h.sources:
  if src.startswith(('http:','https:','//')):errors.append('Remote media '+str(p.relative_to(ROOT))+':'+src)
  elif not src.startswith('data:') and not (p.parent/src).exists():errors.append('Missing embedded asset '+src)
r=json.loads((ROOT/'catalog/source-catalogue.json').read_text())
for x in r:
 if x['local_media_present']:
  p=ROOT/x['package_path']
  if not p.exists():errors.append('Catalogue missing '+x['id'])
  elif hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append('Catalogue hash mismatch '+x['id'])
  if x['decision']!='ACCEPT_FILE' or x['commercial_redistribution']!='conditional':errors.append('Rights approval mismatch '+x['id'])
 elif x.get('package_path'):errors.append('Non-acquired resource has package path '+x['id'])
print(json.dumps({'files_checked':count,'acquired_resource_records':sum(x['local_media_present'] for x in r),'errors':errors},indent=2))
sys.exit(bool(errors))
