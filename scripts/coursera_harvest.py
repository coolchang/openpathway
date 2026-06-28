#!/usr/bin/env python3
"""OpenPathway — Coursera public catalog harvester (capped). Public, no auth."""
import json, sys, time, urllib.request
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent/"data"; DATA.mkdir(exist_ok=True)
B="https://api.coursera.org/api/courses.v1"; P="https://api.coursera.org/api/partners.v1"
F="name,slug,description,photoUrl,primaryLanguages,partnerIds,domainTypes"
UA={"User-Agent":"OpenPathway/0.1","Accept":"application/json"}
CAP=int(sys.argv[1]) if len(sys.argv)>1 else 8000
def get(u):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40) as r:
                return json.loads(r.read().decode("utf-8","replace"))
        except Exception: time.sleep(1.5)
    return None
pmap={};s=0
while True:
    d=get(f"{P}?start={s}&limit=100&fields=name");
    if not d or not d.get("elements"): break
    for p in d["elements"]: pmap[str(p["id"])]=p.get("name")
    nx=d.get("paging",{}).get("next");
    if not nx: break
    s=int(nx)
out=open(DATA/"courses.jsonl","w"); n=0; start=0
while n<CAP:
    d=get(f"{B}?start={start}&limit=100&fields={F}")
    if not d or not d.get("elements"): break
    for c in d["elements"]:
        slug=c.get("slug"); langs=c.get("primaryLanguages") or []
        prov=[pmap.get(str(p)) for p in (c.get("partnerIds") or [])]; prov=[p for p in prov if p]
        out.write(json.dumps({"id":c["id"],"title":(c.get("name") or "").strip(),
            "provider":prov[0] if prov else "Coursera",
            "url":f"https://www.coursera.org/learn/{slug}" if slug else None,
            "description":c.get("description") or "","language":langs[0] if langs else None,
            "source":"coursera"},ensure_ascii=False)+"\n"); n+=1
    nx=d.get("paging",{}).get("next")
    if not nx: break
    start=int(nx); print(f"  courses={n}",flush=True)
out.close(); print(f"DONE courses={n}")
