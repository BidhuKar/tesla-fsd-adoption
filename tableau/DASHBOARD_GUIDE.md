# Tableau Dashboard Build Guide

Goal: one-page dashboard — "FSD Access: Headline vs Reality" — published to **Tableau Public** (free; viewers need only the link).

## Data
Connect Tableau to `data/processed/` CSVs (or the raw CSVs):
- cumulative_access.csv
- rollout_velocity.csv
- pipeline_ranked.csv
- ../raw/us_regulatory_events.csv

## Sheets

1. **World map — access status.** Country on Detail, Status on Color (live = green, limited = amber, pending = grey). Tooltip: population, approval date, notes.
2. **Cumulative access step line.** approval_date (continuous) vs cumulative_pct. Annotate China (Feb 2025) and the EU wave (Apr–Jun 2026).
3. **Headline vs usable bar.** Two bars: total approved population vs live-only population. This is the hero stat (31%).
4. **NHTSA scope timeline.** event_date vs vehicles_in_scope, line + labeled milestones (PE → IR → EA).
5. **Pipeline opportunity.** Horizontal bar of pipeline countries by population, colored by status_2026q2.

## Dashboard layout
- Top banner: title + KPI cards (countries approved: 13 · headline access: ~25% · usable access: ~31% of headline).
- Left 60%: world map. Right 40%: cumulative line over headline-vs-usable bar.
- Bottom: NHTSA timeline + pipeline bar side by side.
- Add a "Status" filter acting on all sheets.

## Publish
Server → Tableau Public → Save. Copy the public URL into README.md and the portfolio page.
