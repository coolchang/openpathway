# Paper outline — OpenPathway

## Working title
**"OpenPathway: An Open Knowledge Graph for Skills-Grounded Learning and Career
Recommendation."**

## Positioning / contribution
First *open, reproducible* reference that unifies **credentials + courses +
skills + occupations** into one graph and recommends actionable learning paths.
Existing skills-intelligence systems (Lightcast, Eightfold, Faethm) are closed;
OpenPathway is open data + open code + open eval.

Claimed contributions:
1. A reproducible pipeline that links heterogeneous public learning supply
   (courses, credentials) to a standard skill/occupation taxonomy (ESCO).
2. A skill-normalization method (surface skills → ESCO canonical) with an
   evaluation of coverage/precision (incl. multilingual).
3. A graph-traversal + re-ranking recommender for occupation → learning path,
   with an LLM-judge evaluation harness.
4. An open dataset + benchmark task ("given a target occupation, recommend an
   ordered set of courses/credentials that cover its required skills").

## Target venues (realistic, in order)
- **arXiv preprint** first (immediate, citable, visibility).
- Workshop/short paper: **EDM** (Educational Data Mining), **LAK** (Learning
  Analytics & Knowledge), **RecSys** (LBR or EdRecSys / RecSys-in-HR workshop),
  **AIED**. These accept system + dataset papers and are the field's frontier.
- 1EdTech / open credentials community write-up for domain reach.

## Structure
1. Introduction — the learning→career gap; why open matters.
2. Related work — skills taxonomies (ESCO, O*NET, Lightcast), talent
   intelligence, course/credential metadata (Open Badges, CTDL), GraphRAG.
3. Data — ESCO, Coursera, Open Badges; licensing; stats.
4. Method — graph schema; skill normalization; LLM tagging; recommender.
5. Evaluation — skill-match coverage/precision; path quality (LLM-judge +
   small human study); multilingual.
6. Demo + reproducibility — open repo, one-command build.
7. Limitations — public-data bias, English-centric, no learner outcomes.
8. Conclusion + future work.

## Note
The paper and the repo are the same artifact viewed two ways: ship the repo,
write the paper from it. Both build the author's name in the field — and both
are clean (public data only, no employer IP).
