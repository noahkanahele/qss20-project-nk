# 03_analyze.py
# Runs descriptive analysis and produces figures saved to output/
# Figures:
#   fig1_race_uhi.png    -- scatter: % POC vs UHI index
#   fig2_income_uhi.png  -- bar chart: median UHI by income quintile
#   fig3_region_uhi.png  -- bar chart: median UHI by region group

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/uhi_tracts_clean.csv')

# ── Figure 1: Race vs UHI ──────────────────────────────────────────────────────
sample = df.sample(1000, random_state=1)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(sample['pct_poc'], sample['uhi_index'],
           alpha=0.3, s=8, color='steelblue')
ax.set_xlabel('Percent People of Color (%)')
ax.set_ylabel('UHI Index (degrees F)')
ax.set_title('Race and Urban Heat Exposure by Census Tract')
plt.tight_layout()
plt.savefig('output/fig1_race_uhi.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig1_race_uhi.png")

# ── Figure 2: Income quintile vs UHI ──────────────────────────────────────────
quintile_order = ['Q1 (Lowest)', 'Q2', 'Q3', 'Q4', 'Q5 (Highest)']
medians = df.groupby('income_quintile', observed=True)['uhi_index'].median()
medians = medians.reindex(quintile_order)

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(medians.index, medians.values,
              color='steelblue', edgecolor='white', width=0.6)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05,
            f'{h:.1f}°F', ha='center', va='bottom', fontsize=10)
ax.set_xlabel('Household Income Quintile')
ax.set_ylabel('Median UHI Index (°F)')
ax.set_title('Urban Heat Exposure by Neighborhood Income\n(Census Tracts, 44 U.S. Cities)')
ax.set_ylim(0, 12)
ax.tick_params(axis='x', labelsize=9)
plt.tight_layout()
plt.savefig('output/fig2_income_uhi.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig2_income_uhi.png")

# ── Figure 3: Region group vs UHI ─────────────────────────────────────────────
region_medians = df.groupby('region_group')['uhi_index'].median().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(region_medians.index, region_medians.values,
              color='steelblue', edgecolor='white', width=0.5)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05,
            f'{h:.1f}°F', ha='center', va='bottom', fontsize=10)
ax.set_xlabel('Region')
ax.set_ylabel('Median UHI Index (°F)')
ax.set_title('Urban Heat Exposure by Region\n(Census Tracts, 44 U.S. Cities)')
ax.set_ylim(0, 12)
plt.tight_layout()
plt.savefig('output/fig3_region_uhi.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig3_region_uhi.png")

# ── Correlation table ──────────────────────────────────────────────────────────
corr_vars = ['uhi_index', 'pct_poc', 'median_income', 'poverty_rate', 'tree_canopy_pct']
corr_table = df[corr_vars].corr().round(2)
print("\nCorrelation matrix:")
print(corr_table)
corr_table.to_csv('output/correlation_table.csv')
print("Saved correlation_table.csv")
