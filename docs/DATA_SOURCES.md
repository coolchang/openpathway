# Public Data Sources — verification (2026-06-27)

All sources are public and openly licensed. No proprietary / employer data is
used anywhere in OpenPathway.

## ✅ ESCO (European Skills, Competences, Qualifications and Occupations)
- API: `https://ec.europa.eu/esco/api` — **public, no auth** (verified 200).
- Search: `/search?text=data%20scientist&type=occupation&language=en` → 188 hits.
- Provides: ~3,000 occupations, ~13,000 skills, and **skill↔occupation links**
  (essential/optional) — the graph backbone is ready out of the box.
- Multilingual (28 languages) — supports multilingual normalization demo.
- License: open (EU ESCO terms, CC-BY-style attribution).
- Resource fetch: `/resource/occupation?uri=...` , `/resource/skill?uri=...`.

## ✅ Coursera Catalog
- API: `https://api.coursera.org/api/courses.v1` — **public, no auth** (verified).
- `?start&limit&fields=name,slug,description,photoUrl,primaryLanguages,partnerIds,domainTypes`
- ~22,000 courses; partner names via `partners.v1`. url = `coursera.org/learn/<slug>`.
- ⚠️ skills NOT in catalog → derive via LLM tagging from title/description.
- License: store metadata + link-out only (descriptions are partner copyright).

## 🔑 O*NET (US occupations) — optional
- `services.onetcenter.org/ws` returns 401 → needs **free API key** (registration).
- Optional cross-walk to ESCO for US coverage. Defer to later phase.

## 🟡 Open Badges (public credentials) — optional
- Public OB2/OB3 issuer endpoints (e.g. Badgr/Canvas `/public/issuers/<id>/badges`,
  openbadge-global OB2). Use only clearly-public issuers; store metadata + link.
- Adds the "credential" node type; can ship v1 with courses only and add later.

## Build order
1. ESCO → Skill + Occupation nodes + REQUIRES edges (backbone).
2. Coursera → Course nodes; LLM-tag course→ESCO skill (TEACHES edges).
3. (optional) public Open Badges → Credential nodes; VALIDATES edges.
4. Recommend: occupation → required skills → courses teaching them → ordered path.
