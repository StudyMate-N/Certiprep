from pathlib import Path
import csv,zipfile,io,json,sqlite3,tempfile,math
W=Path('research-work');out=[]
# Independently recompute values explicitly inspected in downloaded textbook pages.
checks=[('TXT-MA','PDF page 63 contribution margin',(25-10)*1000,15000),('TXT-MA','PDF page 63 operating income',(25-10)*1000-8000,7000),('TXT-MA','PDF page 66 break-even units',8000/(18-10),1000),('TXT-FINITE','PDF page 187 effective annual rate, 7.2% monthly compounding',round(((1+.072/12)**12-1)*100,2),7.44),('TXT-FINITE','PDF page 187 effective annual rate, 7.25% semiannually',round(((1+.0725/2)**2-1)*100,2),7.38),('TXT-MICRO','PDF page 425 producer surplus',(7.5-4.23)*110,359.7),('TXT-FA','PDF page 115 gross profit example FIFO',10-1,9),('TXT-FA','PDF page 115 gross profit example LIFO (US GAAP context)',10-3,7)]
for id,what,got,expected in checks:out.append({'resource_id':id,'check':what,'computed':got,'expected':expected,'pass':math.isclose(got,expected,rel_tol=1e-6,abs_tol=.01)})
# Source package integrity and concrete data availability.
for k in ['PY','SHEET','SQL']:
 p=W/f'evidence/CARP-{k}-SOURCE.html'
 with zipfile.ZipFile(p) as z:
  bad=z.testzip();assert bad is None
  names=z.namelist();data=[n for n in names if n.lower().endswith(('.csv','.tsv','.db','.sqlite','.xlsx','.ods'))]
  licences=[n for n in names if n.endswith('LICENSE.md')]
  assert licences
  out.append({'resource_id':'COURSE-'+k,'check':'ZIP CRC, licence and data inventory','pass':True,'archive_members':len(names),'data_files':data})
  for n in data:
   if n.lower().endswith('.csv'):
    b=z.read(n).decode('utf-8-sig');r=list(csv.reader(io.StringIO(b)))
    out.append({'resource_id':'COURSE-'+k,'check':'CSV parses','file':n,'rows':max(0,len(r)-1),'columns':len(r[0]) if r else 0,'pass':bool(r)})
   elif n.endswith('.db'):
    with tempfile.TemporaryDirectory() as d:
     f=Path(d)/'sample.db';f.write_bytes(z.read(n));con=sqlite3.connect('file:'+str(f)+'?mode=ro',uri=True)
     integrity=con.execute('pragma integrity_check').fetchone()[0];tables=con.execute("select name from sqlite_master where type='table'").fetchall();con.close()
     out.append({'resource_id':'COURSE-'+k,'check':'SQLite read-only integrity','file':n,'tables':[x[0] for x in tables],'pass':integrity=='ok'})
Path('research-work/example-qa.json').write_text(json.dumps(out,indent=2));print('checks',len(out),'failures',[x for x in out if not x['pass']])
