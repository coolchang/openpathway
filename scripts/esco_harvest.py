#!/usr/bin/env python3
"""
OpenPathway — ESCO backbone harvester (public, no auth).
Seeds a curated set of occupations, fetches each occupation's essential/optional
skills, and writes the graph backbone:
  data/esco_occupations.jsonl  {uri,title,essential:[{uri,title}],optional:[...]}
  data/esco_skills.jsonl       {uri,title}   (deduped)
"""
import json, urllib.request, urllib.parse, time
from pathlib import Path
API = "https://ec.europa.eu/esco/api"
UA = {"User-Agent": "OpenPathway/0.1", "Accept": "application/json"}
DATA = Path(__file__).resolve().parent.parent / "data"; DATA.mkdir(exist_ok=True)

SEED = [
 "data scientist","data engineer","data analyst","machine learning",
 "software developer","web developer","cloud engineer","devops",
 "database administrator","cyber security","systems analyst","ICT project manager",
 "business analyst","digital marketing","UX designer","product manager",
 "network engineer","AI engineer","statistician","information security",
]

def get(path):
    with urllib.request.urlopen(urllib.request.Request(API+path, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8","replace"))

def search_occ(text):
    q = urllib.parse.urlencode({"text":text,"type":"occupation","language":"en","limit":1,"full":"false"})
    res = (get(f"/search?{q}").get("_embedded",{}).get("results") or [])
    return res[0] if res else None

def link_items(links, rel):
    out=[]
    for s in links.get(rel,[]) or []:
        uri = s.get("uri") or s.get("href")
        if uri: out.append({"uri":uri,"title":s.get("title")})
    return out

def occ_detail(uri):
    q=urllib.parse.urlencode({"uri":uri,"language":"en"})
    d=get(f"/resource/occupation?{q}")
    links=d.get("_links",{})
    return {"uri":uri,"title":d.get("title"),
            "essential":link_items(links,"hasEssentialSkill"),
            "optional":link_items(links,"hasOptionalSkill")}

def main():
    occs=[]; skills={}
    for term in SEED:
        try:
            o=search_occ(term)
            if not o: print("  miss:",term); continue
            d=occ_detail(o["uri"]); occs.append(d)
            for s in d["essential"]+d["optional"]: skills[s["uri"]]=s["title"]
            print(f"  {d['title']:38s} ess={len(d['essential'])} opt={len(d['optional'])}")
            time.sleep(0.2)
        except Exception as e: print("  err",term,e)
    (DATA/"esco_occupations.jsonl").write_text("\n".join(json.dumps(o,ensure_ascii=False) for o in occs))
    (DATA/"esco_skills.jsonl").write_text("\n".join(json.dumps({"uri":u,"title":t},ensure_ascii=False) for u,t in skills.items()))
    print(f"DONE occupations={len(occs)} skills={len(skills)}")

if __name__=="__main__": main()
