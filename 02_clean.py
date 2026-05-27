# 02_clean.py
# Loads the raw UHI dataset, checks for missing values,
# creates derived variables, and saves a cleaned version.

import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv('data/uhi_tracts.csv')

print("=== RAW DATA ===")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# ── Drop tracts with missing key variables ────────────────────────────────────
df = df.dropna(subset=['uhi_index', 'pct_poc', 'median_income', 'poverty_rate'])

# ── Drop very small tracts (population < 100) ─────────────────────────────────
df = df[df['population'] >= 100]

# ── Create income quintile variable ───────────────────────────────────────────
df['income_quintile'] = pd.qcut(
    df['median_income'],
    q=5,
    labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4', 'Q5 (Highest)']
)

# ── Create region grouping for later analysis ─────────────────────────────────
# Sun Belt: South + Southeast + Southwest
# Rust Belt / Midwest: Ohio Valley + Upper Midwest
# Coastal: Northeast + West + Northwest
df['region_group'] = df['region'].map({
    'South': 'Sun Belt',
    'Southeast': 'Sun Belt',
    'Southwest': 'Sun Belt',
    'Ohio Valley': 'Rust Belt / Midwest',
    'Upper Midwest': 'Rust Belt / Midwest',
    'Northeast': 'Coastal',
    'West': 'Coastal',
    'Northwest': 'Coastal'
})

# ── Summary statistics ─────────────────────────────────────────────────────────
print("\n=== CLEANED DATA ===")
print(f"Shape after cleaning: {df.shape}")
print(f"\nUHI Index summary:\n{df['uhi_index'].describe().round(2)}")
print(f"\nMedian UHI by region group:\n{df.groupby('region_group')['uhi_index'].median().round(2)}")

# ── Save cleaned data ──────────────────────────────────────────────────────────
df.to_csv('data/uhi_tracts_clean.csv', index=False)
print("\nSaved cleaned data to data/uhi_tracts_clean.csv")
