const BUCKET = __BUCKET__;
const KEY_HASH = __HASH__;
const EXPIRES = Date.parse(__EXPIRES__);
const ALLOWED = __ALLOWED__;
const TYPES = ["application/json","application/pdf","application/zip","image/gif","image/png","text/html"];
const encoder = new TextEncoder();
function reply(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});}
async function hash(data){const b=typeof data==="string"?encoder.encode(data):data;return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",b))).map(x=>x.toString(16).padStart(2,"0")).join("");}
function same(a,b){if(a.length!==b.length)return false;let x=0;for(let i=0;i<a.length;i++)x|=a.charCodeAt(i)^b.charCodeAt(i);return x===0;}
Deno.serve(async(req)=>{
 if(req.method!=="POST")return reply({error:"method_not_allowed"},405);
 const token=req.headers.get("x-cpa-transfer-key")||"";
 if(Date.now()>EXPIRES||token.length<40||token.length>200||!same(await hash(token),KEY_HASH))return reply({error:"forbidden"},403);
 const base=(Deno.env.get("SUPABASE_URL")||"")+"/storage/v1";
 const key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");if(!key)return reply({error:"server_configuration"},500);
 const headers={"authorization":"Bearer "+key,"apikey":key,"content-type":"application/json"};
 async function api(path,method="GET",data){const r=await fetch(base+path,{method,headers,...(data===undefined?{}:{body:JSON.stringify(data)})});return {ok:r.ok,status:r.status,data:await r.json()};}
 async function privateBucket(create=false){
  let r=await api("/bucket/"+BUCKET);
  if(r.status===404 && create){await api("/bucket","POST",{id:BUCKET,name:BUCKET,public:false,file_size_limit:40000000,allowed_mime_types:TYPES});r=await api("/bucket/"+BUCKET);}
  const b=r.data,limit=Number(b?.file_size_limit),needed=Math.max(...Object.values(ALLOWED).map(x=>x.bytes));
  return r.ok && b?.public===false && limit>0 && limit<=40000000 && limit>=needed && Array.isArray(b.allowed_mime_types) && b.allowed_mime_types.every(x=>TYPES.includes(x)) && Object.values(ALLOWED).every(x=>b.allowed_mime_types.includes(x.mime));
 }
 const object=req.headers.get("x-cpa-object-path");
 if(object!==null){
  if(!Object.prototype.hasOwnProperty.call(ALLOWED,object))return reply({error:"path_not_approved"},400);
  const expected=ALLOWED[object];
  if(!await privateBucket())return reply({error:"bucket_privacy_or_limits_invalid"},409);
  if(req.headers.get("content-type")!==expected.mime)return reply({error:"mime_mismatch"},415);
  const declared=req.headers.get("content-length");if(declared!==null && Number(declared)!==expected.bytes)return reply({error:"size_mismatch"},400);
  if(!req.body)return reply({error:"body_required"},400);
  const data=new Uint8Array(expected.bytes),reader=req.body.getReader();let offset=0;
  for(;;){const part=await reader.read();if(part.done)break;if(offset+part.value.length>data.length){await reader.cancel();return reply({error:"size_exceeded"},413);}data.set(part.value,offset);offset+=part.value.length;}
  if(offset!==expected.bytes||!same(await hash(data),expected.sha256))return reply({error:"content_hash_mismatch"},422);
  const path=object.split("/").map(encodeURIComponent).join("/");
  const response=await fetch(base+"/object/"+BUCKET+"/"+path,{method:"POST",headers:{...headers,"content-type":expected.mime,"x-upsert":"false"},body:data});
  const result=await response.json();
  if(!response.ok){const m=String(result?.message||result?.error||"").toLowerCase();if(response.status===409||(response.status===400 && /already exists|duplicate/.test(m)))return reply({existing:true,requires_download_verification:true},409);return reply({error:"storage_upload_failed",status:response.status},502);}
  return reply({path:object,bytes:offset,sha256:expected.sha256,stored:true});
 }
 let body;try{body=await req.json();}catch{return reply({error:"invalid_json"},400);}
 if(!body||typeof body!=="object")return reply({error:"invalid_body"},400);
 if(body.action==="init"){
  if(!await privateBucket(true))return reply({error:"bucket_privacy_or_limits_invalid"},409);
  return reply({bucket:BUCKET,public:false,approved_paths:Object.keys(ALLOWED).length,upload_protocol:"authenticated_exact_hash_proxy"});
 }
 if(!Array.isArray(body.paths)||body.paths.length<1||body.paths.length>200||body.paths.some(p=>typeof p!=="string"||!Object.prototype.hasOwnProperty.call(ALLOWED,p)))return reply({error:"paths_not_approved"},400);
 if(body.action==="download"){
  if(!await privateBucket())return reply({error:"bucket_privacy_or_limits_invalid"},409);
  const r=await api("/object/sign/"+BUCKET,"POST",{expiresIn:900,paths:body.paths});
  if(!r.ok)return reply({error:"sign_download",status:r.status},500);
  return reply({urls:r.data.map(x=>({path:x.path,url:x.signedURL?base+x.signedURL:null,error:x.error||null}))});
 }
 return reply({error:"unsupported_action"},400);
});
