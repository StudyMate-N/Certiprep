#!/usr/bin/env python3
"""Audit a CPA catalogue. Metadata-only mode never reports verified media."""
import argparse,hashlib,json,sys,zipfile
from pathlib import Path
p=argparse.ArgumentParser(description='Mechanical checks only; not legal or academic certification.');p.add_argument('--root',required=True,type=Path);p.add_argument('--metadata-only',action='store_true');a=p.parse_args();root=a.root.resolve();rows=json.loads((root/'catalog/source-catalogue.json').read_text());errors=[];seen=set();works=set();verified=0;accepted=0
for r in rows:
 ident=r.get('id');
 if not ident or ident in seen:errors.append('Missing/duplicate id '+str(ident))
 seen.add(ident)
 if not r.get('local_media_present'):
  if r.get('package_path'):errors.append('External resource has packaged path '+str(ident))
  continue
 accepted+=1;works.add(r.get('work_id',ident));rel=r.get('package_path','');target=(root/rel).resolve()
 if not rel or not target.is_relative_to(root):errors.append('Invalid package path '+str(ident));continue
 if r.get('decision')!='ACCEPT_FILE' or r.get('commercial_redistribution')!='conditional':errors.append('Approval mismatch '+str(ident))
 if not r.get('licence') or not r.get('rights_evidence') or not r.get('sha256') or not r.get('source_sha256'):errors.append('Missing exact-artifact rights/provenance '+str(ident))
 if not r.get('rights_actions'):errors.append('Missing action-specific rights '+str(ident))
 if a.metadata_only:continue
 if not target.is_file():errors.append('Missing bytes '+str(ident));continue
 before=len(errors);b=target.read_bytes()
 if b.startswith(b'version https://git-lfs.github.com/spec/v1'):errors.append('LFS pointer '+str(ident))
 if hashlib.sha256(b).hexdigest()!=r.get('sha256') or len(b)!=r.get('packaged_bytes'):errors.append('Hash/size mismatch '+str(ident))
 if target.suffix.lower()=='.pdf' and not b.startswith(b'%PDF-'):errors.append('Invalid PDF signature '+str(ident))
 if target.suffix.lower()=='.zip':
  try:
   with zipfile.ZipFile(target) as z:
    if z.testzip():errors.append('ZIP CRC failure '+str(ident))
    for n in z.namelist():
     if n.startswith('/') or '..' in Path(n).parts:errors.append('Unsafe ZIP member '+str(ident))
     if not n.endswith('/') and z.read(n).startswith(b'version https://git-lfs.github.com/spec/v1'):errors.append('Nested LFS pointer '+str(ident))
  except zipfile.BadZipFile:errors.append('Invalid ZIP '+str(ident))
 if len(errors)==before:verified+=1
if not a.metadata_only:
 manifest_path=root/'catalog/file-manifest.json'
 if not manifest_path.is_file():errors.append('Missing media file inventory')
 else:
  assets=json.loads(manifest_path.read_text());listed=set()
  for f in assets:
   rel=f['path'];t=(root/rel).resolve();listed.add(rel)
   if not t.is_relative_to(root) or not t.is_file():errors.append('Missing/unsafe inventoried asset '+rel);continue
   b=t.read_bytes()
   if hashlib.sha256(b).hexdigest()!=f['sha256'] or len(b)!=f['bytes']:errors.append('Asset hash/size mismatch '+rel)
  actual={x.relative_to(root).as_posix() for x in (root/'media').rglob('*') if x.is_file()}
  if actual!=listed:errors.append('Media inventory differs from actual media paths')
 manifest=root/'MANIFEST.sha256'
 if not manifest.is_file():errors.append('Missing complete release manifest; full release verification unavailable')
 else:
  listed=set()
  for line in manifest.read_text().splitlines():
   digest,rel=line.split('  ',1);listed.add(rel);f=(root/rel).resolve()
   if not f.is_relative_to(root) or not f.is_file():errors.append('Missing/unsafe release path '+rel);continue
   if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:errors.append('Release manifest mismatch '+rel)
  actual={f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file() and f.name!='MANIFEST.sha256'}
  if actual!=listed:errors.append('Release manifest is incomplete or lists extra paths')
print(json.dumps(dict(mode='metadata_only' if a.metadata_only else 'packaged_primary_files',source_records=len(rows),acquired_entries=accepted,grouped_substantial_works=len(works),primary_media_files_verified=verified,errors=errors),indent=2));sys.exit(bool(errors))
