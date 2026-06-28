#!/usr/bin/env python3
"""
OpenPathway — learning-path recommender (v0.1, string-match baseline).
occupation -> ESCO essential skills -> Coursera courses that teach them -> path.
Usage: python3 recommend.py "data scientist"
NOTE: v0.1 uses transparent keyword matching; embedding/LLM matching is the
quality upgrade (see PAPER_OUTLINE). Honest baseline, fully reproducible.
"""
import json, re, sys, unicodedata
from pathlib import Path
DATA=Path(__file__).resolve().parent.parent/"data"

def norm(s):
    s=unicodedata.normalize("NFKC",s or "").lower()
    s=re.sub(r"\(.*?\)"," ",s)              # drop ESCO parentheticals
    s=re.sub(r"[^a-z0-9+# ]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()

STOP=set("and or the a an of to for with in on use using apply able ability skills".split())
def keyterms(label):
    toks=[t for t in norm(label).split() if t not in STOP and len(t)>2]
    return toks

occs=[json.loads(l) for l in open(DATA/"esco_occupations.jsonl") if l.strip()]
courses=[json.loads(l) for l in open(DATA/"courses.jsonl") if l.strip()]
for c in courses: c["_t"]=norm(c["title"]); c["_d"]=norm(c["description"])[:400]

def best_course(skill_label):
    phrase=norm(skill_label); terms=keyterms(skill_label)
    if not terms: return None
    best=None;bs=0
    for c in courses:
        s=0
        if phrase and len(phrase)>4 and phrase in c["_t"]: s+=10
        elif phrase and len(phrase)>4 and phrase in c["_d"]: s+=4
        # keyterm coverage in title
        hit=sum(1 for t in terms if t in c["_t"])
        s+=hit*3
        s+=sum(1 for t in terms if t in c["_d"])*1
        if s>bs: bs=s; best=c
    return (best,bs) if bs>=6 else None   # threshold to avoid noise

def recommend(term):
    occ=next((o for o in occs if term.lower() in (o["title"] or "").lower()), None)
    if not occ: 
        print("occupation not found. available:", ", ".join(o["title"] for o in occs)); return
    print(f"\n🎯 Target occupation: {occ['title']}")
    print(f"   ESCO essential skills: {len(occ['essential'])}\n")
    print("📚 Recommended learning path (skill → course that teaches it):\n")
    seen=set();shown=0
    for sk in occ["essential"]:
        r=best_course(sk["title"])
        if not r: continue
        c,score=r
        if c["id"] in seen: continue
        seen.add(c["id"]); shown+=1
        print(f"  {shown:2d}. [{sk['title']}]")
        print(f"      → {c['title']}  ({c['provider']})")
        print(f"        {c['url']}")
    print(f"\n   {shown}/{len(occ['essential'])} essential skills matched to a course.")

if __name__=="__main__":
    recommend(sys.argv[1] if len(sys.argv)>1 else "data scientist")
