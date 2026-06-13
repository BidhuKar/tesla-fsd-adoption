-- Tesla FSD Global Adoption Analysis
-- Engine: SQLite (works in Python's sqlite3)
-- Tables loaded from /data/raw CSVs: fsd_country_approvals, us_regulatory_events, expansion_pipeline

-- 1. Cumulative % of global population with FSD access over time
SELECT
    approval_date,
    country,
    pct_global_population,
    ROUND(SUM(pct_global_population) OVER (ORDER BY approval_date), 2) AS cumulative_pct_global
FROM fsd_country_approvals
ORDER BY approval_date;

-- 2. Regional breakdown: population covered and country count
SELECT
    region,
    COUNT(*)                       AS countries,
    SUM(population)                AS population_covered,
    ROUND(SUM(pct_global_population), 2) AS pct_global
FROM fsd_country_approvals
GROUP BY region
ORDER BY population_covered DESC;

-- 3. Rollout velocity: countries approved per year
SELECT
    STRFTIME('%Y', approval_date) AS year,
    COUNT(*)                      AS approvals,
    SUM(population)               AS population_added
FROM fsd_country_approvals
GROUP BY year
ORDER BY year;

-- 4. The "China caveat": live vs limited/pending access
SELECT
    status,
    COUNT(*)        AS countries,
    SUM(population) AS population,
    ROUND(100.0 * SUM(population) / (SELECT SUM(population) FROM fsd_country_approvals), 1) AS pct_of_approved_pop
FROM fsd_country_approvals
GROUP BY status;
-- Insight: a single 'limited' market (China) holds ~67% of all "approved" population.

-- 5. Gap between announcement and headline number ("access" vs usable access)
SELECT
    SUM(CASE WHEN status = 'live' THEN population ELSE 0 END)              AS truly_live_population,
    SUM(population)                                                         AS headline_population,
    ROUND(100.0 * SUM(CASE WHEN status = 'live' THEN population ELSE 0 END)
        / SUM(population), 1)                                               AS pct_actually_live
FROM fsd_country_approvals;

-- 6. US regulatory pressure timeline: investigation scope growth
SELECT
    event_date,
    event_type,
    vehicles_in_scope,
    vehicles_in_scope - LAG(vehicles_in_scope) OVER (ORDER BY event_date) AS scope_increase
FROM us_regulatory_events
WHERE vehicles_in_scope IS NOT NULL AND vehicles_in_scope != ''
ORDER BY event_date;

-- 7. Expansion pipeline: biggest untapped markets
SELECT
    country, region, population, status_2026q2, key_blocker
FROM expansion_pipeline
ORDER BY population DESC
LIMIT 5;

-- 8. Days between consecutive approvals (rollout acceleration)
SELECT
    country,
    approval_date,
    JULIANDAY(approval_date) - JULIANDAY(LAG(approval_date) OVER (ORDER BY approval_date)) AS days_since_prev_approval
FROM fsd_country_approvals
ORDER BY approval_date;
-- Insight: 17 months between US→Canada; ~30 days between recent EU approvals.
