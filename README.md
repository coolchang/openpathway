# OpenPathway

**An open, reproducible knowledge graph that recommends a learning path —
courses and credentials — for any skill or career goal.**

> Input a target occupation or skill → get *"earn these credentials, take these
> courses, in this order"*, grounded in a graph of **Skill ↔ Occupation ↔
> Course ↔ Credential**.

OpenPathway is the **open reference implementation** of skills-graph career &
learning recommendation. Everything here is built **only from public,
openly-licensed data** — no proprietary sources.

## Why

The field of "talent / learning recommendation" is dominated by closed
platforms (Eightfold, Lightcast, Gloat, Pearson/Faethm). There is no clean,
open, end-to-end reference that shows *how* you connect credentials, courses,
skills, and occupations into actionable pathways. OpenPathway is that reference.

## Architecture

```
[ESCO]      skills + occupations + skill↔occupation links  (EU, open) ─┐
[Coursera]  public course catalog                          (open API) ─┤→ normalize → Neo4j
[Open Badges] public credentials (optional)                            ─┘   (Skill·Occupation·Course·Credential)
                                                                            → recommend: goal → learning path
                                                                            → small web UI / API
```

- **Skill normalization**: course/credential skills → ESCO canonical skills.
- **Recommendation**: graph traversal (occupation → required skills → courses
  that teach them → ordered path) + optional embedding re-ranking.
- **LLM tagging**: fill missing course→skill links from title/description.

## Data sources (all public / open-licensed)

| Source | What | Access | License |
|---|---|---|---|
| **ESCO** (EU) | skills, occupations, skill↔occupation | `ec.europa.eu/esco/api` (no auth ✅) | CC-BY-style, open |
| **Coursera** | course catalog | `api.coursera.org/api/courses.v1` (no auth ✅) | metadata + link-out |
| O*NET (US) | occupations | web services (free API key) | open |
| Open Badges | public credentials | public issuer OB2/OB3 endpoints | per issuer |

See `docs/DATA_SOURCES.md` for verification details.

## Deliverables

1. **OpenPathway graph** — reproducible build from public data (this repo).
2. **Recommendation demo** — goal → learning path (CLI + minimal web UI).
3. **Blog series (3)** — (a) harvesting public credential APIs, (b) normalizing
   skills to ESCO, (c) graph-based learning-path recommendation.
4. **Paper** — short/workshop paper + arXiv preprint (`docs/PAPER_OUTLINE.md`).

## Status

**Working end-to-end (v0.1).** `esco_harvest.py` builds the ESCO backbone
(occupation → essential/optional skills); `coursera_harvest.py` loads the public
course catalog; `recommend.py` returns a learning path for a target occupation:

```
$ python3 scripts/recommend.py "data scientist"
🎯 Target occupation: data scientist
📚 Recommended learning path (skill → course that teaches it):
   2. [design database scheme] → Database Design and Basic SQL in PostgreSQL (U. Michigan)
  12. [data mining]            → Data Mining Pipeline (CU Boulder)
   5. [build recommender systems] → Building Recommender Systems with ML and AI
   ...
```

v0.1 uses a transparent keyword-matching baseline. **Next:** embedding/LLM
skill→course matching (quality upgrade), Neo4j loader + web UI, Open Badges
credential layer.

## License

Code: MIT. Data: redistributed only as permitted by each source; we store
metadata + links, never republish copyrighted course/credential bodies.
```
