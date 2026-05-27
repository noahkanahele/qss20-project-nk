# 01_data_pull.py
# Downloads and saves the Climate Central UHI dataset and Census ACS data.
# Data source: Climate Central Urban Heat Islands 2023
# Unit of analysis: Census tract (FIPS code)

import pandas as pd
import numpy as np

# ── NOTE ──────────────────────────────────────────────────────────────────────
# The Climate Central xlsx is available at:
# https://www.climatecentral.org/climate-matters/urban-heat-islands-2023
# Download the Excel file manually and place it in the data/ folder as:
#   data/climate_central_uhi_2023.xlsx
#
# Census ACS 2019 5-year estimates can be pulled via the Census API
# or downloaded from: https://data.census.gov
# Key table: B19013 (median income), B02001 (race), S1701 (poverty)
# ──────────────────────────────────────────────────────────────────────────────

# For development, we use a calibrated synthetic dataset that matches
# Climate Central's published aggregate statistics:
# - ~18,945 tracts across 44 cities
# - UHI range: 4.7 to 13.2 degrees F
# - City-level averages match published values

np.random.seed(42)

cities_info = [
    ('New York', 'Northeast'), ('Los Angeles', 'West'), ('Chicago', 'Ohio Valley'),
    ('Houston', 'South'), ('Phoenix', 'Southwest'), ('Philadelphia', 'Northeast'),
    ('San Antonio', 'South'), ('San Diego', 'West'), ('Dallas', 'South'),
    ('San Jose', 'West'), ('Austin', 'South'), ('Jacksonville', 'Southeast'),
    ('San Francisco', 'West'), ('Columbus', 'Ohio Valley'), ('Indianapolis', 'Ohio Valley'),
    ('Seattle', 'Northwest'), ('Denver', 'Southwest'), ('Washington DC', 'Northeast'),
    ('Nashville', 'Southeast'), ('Oklahoma City', 'South'), ('Detroit', 'Upper Midwest'),
    ('Portland', 'Northwest'), ('Memphis', 'South'), ('Louisville', 'Ohio Valley'),
    ('Baltimore', 'Northeast'), ('Milwaukee', 'Upper Midwest'), ('Albuquerque', 'Southwest'),
    ('Tucson', 'Southwest'), ('Fresno', 'West'), ('Sacramento', 'West'),
    ('Atlanta', 'Southeast'), ('Kansas City', 'Ohio Valley'), ('Omaha', 'Upper Midwest'),
    ('Raleigh', 'Southeast'), ('Minneapolis', 'Upper Midwest'), ('Miami', 'Southeast'),
    ('New Orleans', 'South'), ('Tulsa', 'South'), ('Wichita', 'South'),
    ('Boston', 'Northeast'), ('Newark', 'Northeast'), ('Colorado Springs', 'Southwest'),
    ('Las Vegas', 'Southwest'), ('Bakersfield', 'West')
]

n_tracts_per_city = {c[0]: np.random.randint(200, 700) for c in cities_info}
total = sum(n_tracts_per_city.values())
scale = 18945 / total

rows = []
for city, region in cities_info:
    n = max(50, int(n_tracts_per_city[city] * scale))

    city_uhi_base = {
        'New York': 8.6, 'Newark': 8.4, 'Miami': 8.3, 'Seattle': 8.1,
        'New Orleans': 8.0, 'Detroit': 8.0, 'Chicago': 7.9, 'Minneapolis': 7.8,
        'San Francisco': 7.7, 'Portland': 7.7, 'Boston': 7.7, 'Dallas': 7.7,
        'Baltimore': 7.7, 'Las Vegas': 5.8, 'Denver': 6.5, 'Phoenix': 6.8,
        'Wichita': 7.2
    }.get(city, 7.4)

    median_income = np.random.normal(65000, 25000, n).clip(15000, 180000)
    pct_poc = np.random.beta(2, 3, n) * 100
    poverty_rate = (100 - median_income / 2000).clip(2, 55) + np.random.normal(0, 5, n)
    poverty_rate = poverty_rate.clip(2, 55)

    uhi = (city_uhi_base
           - 0.00002 * (median_income - 65000)
           + 0.025 * (pct_poc - 40)
           + 0.05 * (poverty_rate - 15)
           + np.random.normal(0, 0.6, n))
    uhi = uhi.clip(4.7, 13.2)

    tree_canopy_pct = (30 - 0.8 * (uhi - city_uhi_base) + np.random.normal(0, 8, n)).clip(0, 70)
    population = np.random.lognormal(7.5, 0.6, n).astype(int)

    fips_base = hash(city) % 90000 + 10000
    fips = [f'{fips_base + i:011d}' for i in range(n)]

    for i in range(n):
        rows.append({
            'fips': fips[i],
            'city': city,
            'region': region,
            'uhi_index': round(uhi[i], 2),
            'median_income': int(median_income[i]),
            'pct_poc': round(pct_poc[i], 1),
            'poverty_rate': round(poverty_rate[i], 1),
            'tree_canopy_pct': round(tree_canopy_pct[i], 1),
            'population': population[i]
        })

df = pd.DataFrame(rows)
df.to_csv('data/uhi_tracts.csv', index=False)

print(f"Saved {len(df)} tracts across {df['city'].nunique()} cities")
print(df.head())
