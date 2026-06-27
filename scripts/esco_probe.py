#!/usr/bin/env python3
"""
OpenPathway — ESCO backbone probe.
Fetch an occupation and its essential/optional skills from the public ESCO API
(no auth). This is the graph backbone: Occupation -[REQUIRES]-> Skill.
Usage: python3 esco_probe.py "data scientist"
"""
import json, sys, urllib.request, urllib.parse
API = "https://ec.europa.eu/esco/api"
UA = {"User-Agent": "OpenPathway/0.1", "Accept": "application/json"}

def get(path):
    with urllib.request.urlopen(urllib.request.Request(API + path, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def search_occupation(text):
    q = urllib.parse.urlencode({"text": text, "type": "occupation", "language": "en", "limit": 1, "full": "false"})
    d = get(f"/search?{q}")
    res = (d.get("_embedded", {}).get("results") or [])
    return res[0] if res else None

def occupation_skills(uri):
    q = urllib.parse.urlencode({"uri": uri, "language": "en"})
    d = get(f"/resource/occupation?{q}")
    title = d.get("title")
    links = d.get("_links", {})
    out = {"essential": [], "optional": []}
    for rel, key in [("hasEssentialSkill", "essential"), ("hasOptionalSkill", "optional")]:
        for s in links.get(rel, []) or []:
            out[key].append(s.get("title"))
    return title, out

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "data scientist"
    occ = search_occupation(term)
    if not occ:
        print("no occupation found"); sys.exit(1)
    uri = occ["uri"]; 
    title, skills = occupation_skills(uri)
    print(f"Occupation: {title}\n  ({uri})")
    print(f"  essential skills: {len(skills['essential'])}, optional: {len(skills['optional'])}")
    for s in skills["essential"][:12]:
        print(f"    • {s}")
