#!/usr/bin/env python3
"""Prepare an exact-content, temporary authenticated private storage transfer."""
from pathlib import Path
import argparse,json,hashlib,secrets,datetime,mimetypes,re,os

def require(ok,message):
 if not ok:raise ValueError(message)

parser=argparse.ArgumentParser();parser.add_argument('--root',required=True,type=Path);parser.add_argument('--workdir',required=True,type=Path)
selection=parser.add_mutually_exclusive_group(required=True);selection.add_argument('--paths-json',type=Path);selection.add_argument('--initial-mirror',action='store_true')
parser.add_argument('--verified-map-json',type=Path);parser.add_argument('--existing-total-bytes',type=int,required=True);parser.add_argument('--existing-cpa-bytes',type=int,required=True);a=parser.parse_args();root=a.root.resolve();w=a.workdir.resolve();bucket='cpa-verified-library'
require(a.existing_total_bytes>=a.existing_cpa_bytes>=0,'Invalid observed storage totals')
require(not a.initial_mirror or a.existing_cpa_bytes==0,'Existing mirror requires incremental selection and a verified map')
R=json.loads((root/'catalog/source-catalogue.json').read_text());F=json.loads((root/'catalog/file-manifest.json').read_text());H=json.loads((root/'catalog/hosting.json').read_text());project=H['project_ref'];require(re.fullmatch('[a-z0-9]{20}',project),'Invalid project ref')
selected=set(json.loads(a.paths_json.read_text())) if a.paths_json else {f['path'] for f in F};require(selected<={f['path'] for f in F},'Selection must contain inventoried paths only')
if not selected:print(json.dumps({'no_transfer_required':True,'reason':'No files selected'}));raise SystemExit(0)
require(a.existing_cpa_bytes==0 or a.verified_map_json is not None,'Existing mirror requires a current verified object map')
verified={}
if a.verified_map_json:
 v=json.loads(a.verified_map_json.read_text());require(isinstance(v,dict),'Verified map must include its project and bucket context')
 require(v.get('project_ref')==project and v.get('bucket')==bucket,'Verified map belongs to another project or bucket')
 require(v.get('public') is False and v.get('all_objects_downloaded_and_sha256_verified') is True,'Verified map must document private full-byte verification')
 for r in v.get('files',[]):
  if r.get('download_verified') is not True:continue
  require(r.get('object_path')=='sha256/'+r.get('sha256','')+'/'+r.get('path',''),'Verified object path does not match its content address')
  require(r['path'] not in verified,'Duplicate path in verified map');verified[r['path']]=r
accepted={r['id'] for r in R if r['decision']=='ACCEPT_FILE' and r['commercial_redistribution']=='conditional' and r.get('licence') and r.get('rights_evidence') and r.get('source_sha256') and r.get('rights_actions')};rows=[]
for f in F:
 if f['path'] not in selected:continue
 owners=set(f['resource_ids'].split('|'));require(owners and owners<=accepted,'Unapproved resource owner or incomplete rights evidence')
 path=(root/f['path']).resolve();require(path.is_relative_to(root/'media') and path.is_file(),'Unsafe or missing media path');b=path.read_bytes();require(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'Media size/hash mismatch');require(0<len(b)<=40000000,'Object must be nonempty and at most 40 MB')
 old=verified.get(f['path'],{})
 if old.get('sha256')==f['sha256'] and old.get('bytes')==f['bytes']:continue
 rows.append(dict(path=f['path'],sha256=f['sha256'],bytes=len(b),mime=mimetypes.guess_type(f['path'])[0] or 'application/octet-stream',object='sha256/'+f['sha256']+'/'+f['path']))
if not rows:print(json.dumps({'no_transfer_required':True,'reason':'All selected files match verified objects in the configured private bucket'}));raise SystemExit(0)
size=sum(r['bytes'] for r in rows)
require(a.existing_total_bytes+size<=800*1024*1024 and a.existing_cpa_bytes+size<=500*1024*1024,'Storage budget exceeded; retain current mirror and report capacity choice without upgrading')
require(not any((x/'.git').exists() for x in [w,*w.parents]),'Private work directory must be outside Git checkouts')
w.mkdir(mode=0o700,parents=True,exist_ok=False);token=secrets.token_urlsafe(64);key=w/'cpa-storage-token';fd=os.open(key,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
with os.fdopen(fd,'w') as stream:stream.write(token)
config=dict(key_sha256=hashlib.sha256(token.encode()).hexdigest(),expires=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)).isoformat(),bucket=bucket,project=project,function='cpa-library-storage-20261101');(w/'storage-map-private.json').write_text(json.dumps(rows));(w/'storage-config-private.json').write_text(json.dumps(config));template=(Path(__file__).parent/'storage_transfer_template.ts').read_text();values={'__BUCKET__':bucket,'__HASH__':config['key_sha256'],'__EXPIRES__':config['expires'],'__ALLOWED__':{r['object']:dict(bytes=r['bytes'],mime=r['mime'],sha256=r['sha256']) for r in rows}}
for marker,value in values.items():template=template.replace(marker,json.dumps(value,separators=(',',':')))
request=dict(project_id=project,name=config['function'],entrypoint_path='index.ts',files=[dict(name='index.ts',content=template)],verify_jwt=False);(w/'deployment-request-private.json').write_text(json.dumps(request));print(json.dumps(dict(approved_files=len(rows),bytes=size,request_file=str(w/'deployment-request-private.json'),authentication='Temporary 512-bit capability key, exact hash/size/MIME upload proxy, scoped allowlist, one-hour expiry; server credentials never leave the server.')))
