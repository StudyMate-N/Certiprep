from pathlib import Path
import json,csv,fitz,re,html
O=Path('Certiprep/research-library/kenya-cpa/session-2026-11-01');R={x['id']:x for x in json.loads((O/'catalog/source-catalogue.json').read_text())};rows=[]
def add(id,topic,page,answers,notes):rows.append(dict(resource_id=id,paper_codes='|'.join(R[id]['papers']),topic=topic,physical_pdf_page_or_html_section=page,answer_availability=answers,local_file=R[id]['package_path'],limitations=notes))
add('TXT-FA','Inventory FIFO/LIFO worked gross profit example','115','Worked explanation on same page','US GAAP example; LIFO is prohibited under IFRS. Not a current IFRS practice bank.')
add('TXT-MA','Contribution margin and operating profit','63','Worked calculations included','Spot-checked 15000 contribution and 7000 operating income; currency is illustrative.')
add('TXT-MA','Break-even units','66','Worked solution included','Spot-checked 1000 units; adapt only with appropriate share-alike attribution.')
add('TXT-FINITE','Linear functions problem set','9-10','Worked examples precede problem set; full answer key not verified','Section 1.1 problem set; calculator syntax differs by permitted examination hardware.')
add('TXT-FINITE','Gauss-Jordan linear systems','56-57','Worked methods in preceding section; full answer key not verified','Section 2.2 problem set.')
add('TXT-FINITE','Game theory chapter review','400-402','Worked chapter examples; full answer key not verified','Inspect required KASNEB topic depth before assigning.')
add('TXT-STATS','Conditional probability, smallpox table and guided practice','112','Guided-practice solution footnotes included','Physical PDF page 112 has printed page 111; accessible edition pagination differs from standard edition.')
add('TXT-STATS','Exercise solutions appendix','426-443','Selected exercise solutions; not every exercise','Appendix A starts physical PDF page 426, printed page 425; match exercise numbers rather than page numbers.')
add('TXT-MICRO','Opportunity cost case: Beer or Cancer','33-34','Solutions start physical page 35','Illustration-omitted edition retains text, graphs, captions and pagination.')
add('TXT-MICRO','Production possibilities and trade: Brexit case','73-77','Solutions start physical page 79','Historical case, not a statement of current trade arrangements.')
add('TXT-NETWORK','Project scheduling exercise set','173-176','Selected solutions appendix starts physical page 453','Printed page 169 corresponds to PDF 173; not every exercise has a solution.')
add('TXT-NETWORK','Finance skills: interest, bonds and compounding','226-230','Selected solutions appendix starts physical page 453','US instruments are illustrative, not Kenyan tax or market guidance.')
add('TXT-MACRO','Self-check question answer key','583','Chapter-organised selected self-check answers','Original deposited PDF answer key page 587 is physical page 583 in the cover-omitted derivative. Review/critical-thinking questions are not all answered.')
for id in ['COURSE-PY','COURSE-SHEET','COURSE-SQL']:add(id,'Lesson exercises and instructor solutions','Readable lesson HTML; source ZIP','Exercises and collapsible instructor solutions in lesson source','Pinned ZIP contains data/code and licences. Some course datasets require explicit download steps; only packaged files count as present.')
add('COST07','Standard direct-labour budget and variance','HTML section 7.1.6','Worked explanation included','Independently recomputed 20000 budget and 5000 unfavourable variance. Full chapter review pending.')
# Verify manually selected physical references against actual text; detect off-by-one pagination.
checks=[]
for id,pg,needle in [('TXT-FA',115,'FIFO'),('TXT-MA',63,'25'),('TXT-FINITE',9,'PROBLEM SET'),('TXT-FINITE',400,'PROBLEM SET'),('TXT-STATS',112,'smallpox'),('TXT-STATS',426,'Exercise solutions'),('TXT-MICRO',33,'Beer or Cancer'),('TXT-NETWORK',173,'Scheduling'),('TXT-NETWORK',453,'Solutions to Selected Exercises'),('TXT-MACRO',583,'ANSWER KEY')]:
 p=fitz.open(O/R[id]['package_path']);ok=needle.lower() in p[pg-1].get_text().lower();checks.append(dict(id=id,physical_page=pg,expected_heading=needle,passed=ok));assert ok,(id,pg,needle)
with (O/'catalog/practice-index.csv').open('w',newline='') as f:w=csv.DictWriter(f,rows[0]);w.writeheader();w.writerows(rows)
(O/'reports/practice-reference-checks.json').write_text(json.dumps(checks,indent=2))
lines=['# Acquired practice and worked-example index','','These are textbook/lesson questions and worked examples actually inside acquired files. They are not KASNEB past examinations. Full answer accuracy and examiner marking alignment are not certified. All PDF references below are **physical PDF pages**, except where printed-page differences are explicitly noted.','','| Resource | Topic | Location | Answers / limits |','|---|---|---|---|']
for r in rows:lines.append(f"| {r['resource_id']} | {r['topic']} | {r['physical_pdf_page_or_html_section']} | {r['answer_availability']}. {r['limitations']} |")
lines+=['','Use the source catalogue or START_HERE.html to open the corresponding local file. Do not recast overseas/old regulatory examples as Kenyan rules. No independently verified KASNEB past-paper answer key was obtained.']
(O/'reports/PRACTICE_INDEX.md').write_text('\n'.join(lines)+'\n');print('practice entries',len(rows),'page checks',len(checks))
