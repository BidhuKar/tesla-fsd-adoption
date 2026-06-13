"""
Tesla FSD Global Adoption — Python analysis
Run: python python/fsd_analysis.py
Outputs: processed CSVs to data/processed/ and charts to docs/img/
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT, IMG = ROOT / "data/raw", ROOT / "data/processed", ROOT / "docs/img"
OUT.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)

# ---------- Load ----------
approvals = pd.read_csv(RAW / "fsd_country_approvals.csv", parse_dates=["approval_date"])
events = pd.read_csv(RAW / "us_regulatory_events.csv", parse_dates=["event_date"])
pipeline = pd.read_csv(RAW / "expansion_pipeline.csv")

# ---------- SQL layer (load into SQLite so the SQL scripts are reproducible) ----------
con = sqlite3.connect(ROOT / "data/processed/fsd.db")
approvals.to_sql("fsd_country_approvals", con, if_exists="replace", index=False)
events.to_sql("us_regulatory_events", con, if_exists="replace", index=False)
pipeline.to_sql("expansion_pipeline", con, if_exists="replace", index=False)

# ---------- Analysis 1: cumulative global access ----------
approvals = approvals.sort_values("approval_date")
approvals["cumulative_pct"] = approvals["pct_global_population"].cumsum()
approvals.to_csv(OUT / "cumulative_access.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.step(approvals["approval_date"], approvals["cumulative_pct"], where="post", lw=2)
ax.set_title("Share of global population with Tesla FSD access (cumulative)")
ax.set_ylabel("% of global population")
for _, r in approvals.iterrows():
    if r["pct_global_population"] > 1:
        ax.annotate(r["country"], (r["approval_date"], r["cumulative_pct"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
fig.tight_layout()
fig.savefig(IMG / "cumulative_access.png", dpi=150)

# ---------- Analysis 2: headline vs usable access ----------
live = approvals.loc[approvals.status == "live", "population"].sum()
total = approvals["population"].sum()
print(f"Headline 'access' population: {total:,}")
print(f"Truly live population:        {live:,} ({live/total:.0%} of headline)")

status = approvals.groupby("status")["population"].sum()
fig, ax = plt.subplots(figsize=(7, 5))
status.plot.bar(ax=ax, color=["#2f6f4f", "#c9a227", "#b04a3a"])
ax.set_title("'Access' headline vs reality: population by rollout status")
ax.set_ylabel("Population")
fig.tight_layout()
fig.savefig(IMG / "status_breakdown.png", dpi=150)

# ---------- Analysis 3: rollout velocity ----------
approvals["year"] = approvals["approval_date"].dt.year
velocity = approvals.groupby("year").agg(approvals_n=("country", "count"),
                                         population_added=("population", "sum"))
velocity.to_csv(OUT / "rollout_velocity.csv")

# ---------- Analysis 4: US regulatory scope growth ----------
scope = events.dropna(subset=["vehicles_in_scope"]).copy()
scope["vehicles_in_scope"] = pd.to_numeric(scope["vehicles_in_scope"], errors="coerce")
scope = scope.dropna(subset=["vehicles_in_scope"])
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(scope["event_date"], scope["vehicles_in_scope"] / 1e6, marker="o")
ax.set_title("NHTSA investigation scope: Tesla vehicles under FSD probes")
ax.set_ylabel("Vehicles (millions)")
fig.tight_layout()
fig.savefig(IMG / "nhtsa_scope.png", dpi=150)

# ---------- Analysis 5: pipeline opportunity ----------
pipeline_sorted = pipeline.sort_values("population", ascending=False)
pipeline_sorted.to_csv(OUT / "pipeline_ranked.csv", index=False)

print("\nTop pipeline markets by population:")
print(pipeline_sorted[["country", "population", "status_2026q2"]].head().to_string(index=False))
con.close()
print("\nDone. Charts in docs/img/, tables in data/processed/.")
