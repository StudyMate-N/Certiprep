from pathlib import Path
import argparse,json,urllib.request,urllib.error,hashlib,datetime,concurrent.futures,time
args=argparse.ArgumentParser();args.add_argument('--root',required=True,type=Path);args.add_argument('--workdir',required=True,type=Path);a=args.parse_args();W=a.workdir.resolve();O=a.root.resolve();C=json.loads((W/'storage-config-private.json').read_text());M=json.loads((W/'storage-map-private.json').read_text());TOKEN=(W/'cpa-storage-token').read_text();ENDPOINT='https://'+C['project']+'.supabase.co/functions/v1/'+C['function']
def require(ok,message):
 if not ok:raise ValueError(message)
def call(data,token=TOKEN):
 req=urllib.request.Request(ENDPOINT,json.dumps(data).encode(),headers={'content-type':'application/json','x-cpa-transfer-key':token},method='POST')
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
try:call({'action':'init'},'invalid-test-token');raise AssertionError('Unauthenticated request was accepted')
except urllib.error.HTTPError as e:require(e.code==403,'Unauthenticated transfer must be denied')
print('Unauthenticated transfer request denied',flush=True);bucket=call({'action':'init'});require(bucket.get('public') is False and bucket.get('upload_protocol')=='authenticated_exact_hash_proxy','Private exact-hash upload protocol required');print('Private bucket',bucket,flush=True)
def upload(m):
 b=(O/m['path']).read_bytes();require(len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],'Local size/hash mismatch')
 req=urllib.request.Request(ENDPOINT,b,headers={'content-type':m['mime'],'x-cpa-transfer-key':TOKEN,'x-cpa-object-path':m['object']},method='POST')
 for attempt in range(2):
  try:
   with urllib.request.urlopen(req,timeout=60) as r:require(r.status==200,'Upload status failure');r.read();return dict(path=m['path'],uploaded=True)
  except urllib.error.HTTPError as e:
   payload=e.read(4096).decode('utf-8','replace').lower()
   if e.code==409 or (e.code==400 and ('already exists' in payload or 'duplicate' in payload)):return dict(path=m['path'],uploaded=False,existing_requires_hash_verification=True)
   if attempt==1:return dict(path=m['path'],error='upload_http_'+str(e.code))
  except Exception as e:
   if attempt==1:return dict(path=m['path'],error='upload_'+type(e).__name__)
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for i,r in enumerate(pool.map(upload,M),1):
  results.append(r)
  if i%40==0:print('Uploaded',i,'of',len(M),flush=True)
fail=[x for x in results if x.get('error')];require(not fail,str(fail))
print('Upload pass complete; downloading every hosted object for SHA-256 comparison',flush=True)
downs=call({'action':'download','paths':[m['object'] for m in M]});DOWN={x['path']:x['url'] for x in downs['urls']};require(len(DOWN)==len(M) and all(DOWN.values()),'Incomplete signed-download set')
def verify(m):
 for attempt in range(2):
  try:
   with urllib.request.urlopen(DOWN[m['object']],timeout=60) as r:b=r.read(m['bytes']+1);status=r.status
   digest=hashlib.sha256(b).hexdigest();require(status==200 and len(b)==m['bytes'] and digest==m['sha256'],'Hosted size/hash mismatch')
   return dict(path=m['path'],object_path=m['object'],bytes=len(b),sha256=digest,download_verified=True)
  except Exception as e:
   if attempt==1:return dict(path=m['path'],error='verify_'+type(e).__name__)
verified=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for i,r in enumerate(pool.map(verify,M),1):
  verified.append(r)
  if i%40==0:print('Downloaded and hash-verified',i,'of',len(M),flush=True)
require(not [x for x in verified if x.get('error')],str([x for x in verified if x.get('error')]))
# Test that an ordinary public URL does not expose the private file.
public='https://'+C['project']+'.supabase.co/storage/v1/object/public/'+C['bucket']+'/'+M[0]['object'];denied=False
try:
 with urllib.request.urlopen(public,timeout=30) as r:denied=r.status!=200
except urllib.error.HTTPError as e:denied=e.code in [400,401,403,404]
require(denied,'Public access was unexpectedly permitted')
result=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),provider='Supabase Storage',project_ref=C['project'],bucket=C['bucket'],public=False,objects=len(verified),bytes=sum(x['bytes'] for x in verified),all_objects_downloaded_and_sha256_verified=True,unauthenticated_transfer_denied=True,public_download_denied=True,files=verified,temporary_transfer_function=C['function'],transfer_function_disable_pending=True)
(W/'storage-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='files'}),flush=True)
