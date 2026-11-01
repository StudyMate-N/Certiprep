#!/usr/bin/env python3
"""Audit bytes actually present; a catalogue claim or LFS pointer is not media."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
def classify(p):
 b=p.read_bytes();kind='lfs_pointer' if b.startswith(b'version https://git-lfs.github.com/spec/v1') else 'pdf_binary' if b.startswith(b'%PDF-') else 'zip_binary' if b.startswith(b'PK\x03\x04') else 'other_file'
 return {'path':p.relative_to(root).as_posix(),'status':kind,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
legacy=[classify(p) for p in sorted((root/'assets').rglob('*')) if p.is_file()]
session=root/'session-2026-11-01';catalog=session/'catalog/source-catalogue.json';r=json.loads(catalog.read_text()) if catalog.exists() else []
local=[classify(p) for p in sorted((session/'media').rglob('*')) if p.is_file()]
checks=[]
for x in r:
 if not x.get('local_media_present'):continue
 p=session/x['package_path'];b=p.read_bytes() if p.is_file() else None
 checks.append({'resource_id':x['id'],'archive_claim':x['acquisition_status'],'file_present_in_this_checkout':b is not None,'hash_matches_catalogue':hashlib.sha256(b).hexdigest()==x['sha256'] if b is not None else None,'is_pointer':b.startswith(b'version https://git-lfs.github.com/spec/v1') if b is not None else False})
print(json.dumps({'legacy_assets':legacy,'legacy_unique_pdf_binaries':len({x['sha256'] for x in legacy if x['status']=='pdf_binary'}),'session_media_files_actually_present':len(local),'session_unique_pdf_binaries_actually_present':len({x['sha256'] for x in local if x['status']=='pdf_binary'}),'session_lfs_pointers':sum(x['status']=='lfs_pointer' for x in local),'session_resource_checks':checks,'note':'The catalogue describes the delivered ZIP. New session media are intentionally not committed to GitHub; absence in a GitHub checkout is expected, not a verified download.'},indent=2))
