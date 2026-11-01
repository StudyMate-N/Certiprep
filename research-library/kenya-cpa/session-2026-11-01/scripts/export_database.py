#!/usr/bin/env python3
"""Build a portable metadata catalogue; actual media remain separate files."""
from pathlib import Path
import json,sqlite3
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'catalog/source-catalogue.json').read_text());assets=json.loads((ROOT/'catalog/file-manifest.json').read_text());coverage=json.loads((ROOT/'catalog/paper-map.json').read_text());dest=ROOT/'catalog/cpa-library.sqlite3';temp=dest.with_suffix('.building.sqlite3')
if temp.exists():temp.unlink()
con=sqlite3.connect(temp);con.executescript('''
create table resources(id text primary key,title text not null,decision text not null,work_id text not null,record_json text not null);
create table usage_rights(resource_id text not null,action text not null,decision text not null,primary key(resource_id,action),foreign key(resource_id) references resources(id));
create table resource_papers(resource_id text not null,paper_code text not null,primary key(resource_id,paper_code),foreign key(resource_id) references resources(id));
create table assets(path text primary key,sha256 text not null,bytes integer not null,record_json text not null);
create table coverage(paper_code text primary key,record_json text not null);
create table settings(key text primary key,value_json text not null);
create table audit_events(id integer primary key,record_json text not null);
''')
for r in rows:
 con.execute('insert into resources values(?,?,?,?,?)',(r['id'],r['title'],r['decision'],r.get('work_id',r['id']),json.dumps(r,ensure_ascii=False)))
 con.executemany('insert into usage_rights values(?,?,?)',[(r['id'],k,v) for k,v in r.get('rights_actions',{}).items()]);con.executemany('insert into resource_papers values(?,?)',[(r['id'],p) for p in dict.fromkeys(r['papers'])])
con.executemany('insert into assets values(?,?,?,?)',[(f['path'],f['sha256'],f['bytes'],json.dumps(f,ensure_ascii=False)) for f in assets]);con.executemany('insert into coverage values(?,?)',[(p['paper_code'],json.dumps(p,ensure_ascii=False)) for p in coverage])
for key in ['maintenance-policy','hosting','capability-state']:
 p=ROOT/'catalog'/f'{key}.json'
 if p.exists():con.execute('insert into settings values(?,?)',(key,p.read_text()))
for line in (ROOT/'reports/session-journal.jsonl').read_text().splitlines():
 json.loads(line);con.execute('insert into audit_events(record_json) values(?)',(line,))
con.commit();assert con.execute('pragma integrity_check').fetchone()[0]=='ok';assert con.execute('pragma foreign_key_check').fetchall()==[];assert con.execute('select count(*) from resources').fetchone()[0]==len(rows);assert con.execute('select count(*) from assets').fetchone()[0]==len(assets);con.close();temp.replace(dest)
print(json.dumps({'database':str(dest),'resources':len(rows),'media_asset_metadata':len(assets),'media_bytes_embedded':0,'integrity':'ok'}))
