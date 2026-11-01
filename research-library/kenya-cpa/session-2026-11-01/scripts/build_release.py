#!/usr/bin/env python3
"""Build and verify the acquired-file archive. Media are required locally."""
from pathlib import Path
import argparse,hashlib,subprocess,sys,zipfile,json
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve()
if out.is_relative_to(ROOT):raise SystemExit('Output archive must be outside the library to avoid recursive packaging')
if not (ROOT/'media').is_dir():raise SystemExit('Actual acquired media required; cannot build a media-free release')
subprocess.run([sys.executable,str(ROOT/'scripts/export_database.py')],check=True)
files=sorted(x for x in ROOT.rglob('*') if x.is_file() and x.name!='MANIFEST.sha256');(ROOT/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(x.read_bytes()).hexdigest()+'  '+x.relative_to(ROOT).as_posix()+'\n' for x in files));subprocess.run([sys.executable,str(ROOT/'scripts/verify_library.py')],check=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(ROOT.rglob('*')):
  if f.is_file():z.write(f,'Kenya_CPA_Master_Library/'+f.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None;members=len(z.namelist())
sha=hashlib.sha256(out.read_bytes()).hexdigest();out.with_suffix('.zip.sha256').write_text(sha+'  '+out.name+'\n');print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'sha256':sha,'members':members,'zip_crc':'passed'}))
