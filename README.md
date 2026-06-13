# Tesla FSD Global Adoption — A Data Analyst's Deep Dive

**Question:** Tesla says ~25% of the world's population now has access to Full Self-Driving (Supervised). How real is that number, what's holding adoption back in the US, and what would it take to scale FSD globally under local laws?

**Stack:** SQL (SQLite) · Python (pandas, matplotlib) · Tableau Public

# Portfolio Page: https://bidhukar.github.io/tesla-fsd-adoption/   
## Key findings

1. **The 25% headline overstates usable access by ~3x.** China alone contributes ~17 of those 25 points, but its rollout is limited by data-compliance rules. Only **~31% of the "approved" population (≈639M people) can actually use FSD today.**
2. **Rollout velocity has flipped.** It took 17 months to go from the US to Canada (2020–2022). In April–June 2026, five European countries approved FSD in ~60 days — a regulatory domino effect triggered by the Dutch RDW approval.
3. **US adoption now faces a regulatory headwind, not a technical one.** NHTSA's investigation scope grew from 2.4M vehicles (Oct 2024) to a 3.2M-vehicle Engineering Analysis (Mar 2026) — the formal step before a recall — over camera-visibility failures and traffic-law violations.
4. **The biggest untapped markets have no framework at all.** India (1.45B) and Brazil (216M) lack any announced regulatory path for supervised L2+ systems.

<img width="1500" height="750" alt="image" src="https://github.com/user-attachments/assets/7b2838e9-7744-4bd4-bf9d-205f38846325" />

<img width="1500" height="750" alt="image" src="https://github.com/user-attachments/assets/e856121b-88b1-4346-86a1-1ee2cdcbe590" />

<img width="1050" height="750" alt="image" src="https://github.com/user-attachments/assets/2a652710-ffe2-4d29-a487-1a467953e101" />

## Repository structure

```
data/raw/          Source datasets (curated from public reporting — see Sources)
data/processed/    SQL-ready SQLite DB + derived tables
sql/               8 analysis queries (window functions, cohorts, status splits)
python/            Reproducible analysis + chart generation
tableau/           Dashboard build guide + data extract
docs/              Insights & recommendations report, charts, portfolio page
```

## Reproduce

```bash
pip install pandas matplotlib
python python/fsd_analysis.py        # builds fsd.db, processed tables, charts
# Open data/processed/fsd.db in DB Browser and run sql/analysis_queries.sql
```

## Recommendations (summary — full report in docs/INSIGHTS.md)

- Report "usable access" separately from "regulatory access" — the gap is the story.
- In the US, treat NHTSA's Engineering Analysis as the critical path: proactive camera-degradation alerts and faster data turnaround reduce recall risk.
- In Europe, ride the RDW template: prioritize countries that defer to Dutch type-approval logic.
- For China, ship the rebranded v14 with in-country data residency baked in.
- For India/Brazil, lead with regulator education and localized safety data collection (the UAE road-testing model), not product launch.

## Sources

- Not a Tesla App — FSD access & expansion tracking (June 2026)
- Tesla — FSD (Supervised) Vehicle Safety Report (tesla.com/fsd/safety)
- NHTSA — Standing General Order crash data, ODI investigations PE25012/EA, NCAP ADAS results
- Electrek, Reuters/Insurance Journal — investigation timeline reporting

*Population figures are as reported in source articles; "% of global population" uses the source's published shares.*
