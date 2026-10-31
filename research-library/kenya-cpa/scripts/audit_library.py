#!/usr/bin/env python3
"""Classify actual media assets. Never count Git LFS pointers as PDF binaries."""
from pathlib import Path
import csv, hashlib, json
root=Path(__file__).resolve().parents[1]
result=[]
for p in sorted((root/"assets").rglob("*")):
    if not p.is_file(): continue
    head=p.read_bytes()[:150]
    status="lfs_pointer" if head.startswith(b"version https://git-lfs.github.com/spec/v1") else "pdf_binary" if head.startswith(b"%PDF-") else "other_binary"
    result.append({"path":str(p.relative_to(root)),"status":status,"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
print(json.dumps({"media_files":result,"verified_pdfs":sum(x["status"]=="pdf_binary" for x in result)},indent=2))
