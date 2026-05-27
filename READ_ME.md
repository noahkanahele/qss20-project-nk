# Urban Heat Inequality: Race, Income, and UHI Exposure Across U.S. Cities

**Noah Kanahele | QSS 20 | Dartmouth College | Spring 2026**

---

## Project Overview

This project investigates which neighborhood-level characteristics predict urban heat island (UHI) intensity across U.S. cities. Specifically, it asks whether racial composition and household income are associated with heat exposure at the census tract level, even after accounting for physical factors like tree canopy cover. The broader goal is to test whether heat falls disproportionately on lower-income and minority communities, and if so, whether that is a structural outcome or primarily explained by the physical environment.

**Unit of analysis:** Census tract (~19,000 tracts across 44 U.S. cities)  
**Dependent variable:** UHI index (°F above rural baseline) from Climate Central 2023  
**Independent variables:** % people of color, median household income, poverty rate, tree canopy % (Census ACS 2019)

---

## Repository Structure

```
uhi_project/
│
├── code/
│   ├── 01_data_pull.py     # Loads and generates the UHI + Census dataset
│   ├── 02_clean.py         # Cleans data, drops missing values, creates derived variables
│   └── 03_analyze.py       # Produces figures and correlation table
│
├── output/
│   ├── fig1_race_uhi.png         # Scatter: % POC vs UHI index
│   ├── fig2_income_uhi.png       # Bar chart: median UHI by income quintile
│   ├── fig3_region_uhi.png       # Bar chart: median UHI by region
│   └── correlation_table.csv     # Correlation matrix of key variables
│
├── data/
│   ├── uhi_tracts.csv            # Raw synthetic dataset (calibrated to Climate Central)
│   └── uhi_tracts_clean.csv      # Cleaned version used in analysis
│
└── README.md
```

---

## Data Sources

| Dataset | Description | Link |
|---|---|---|
| Climate Central UHI 2023 | Tract-level UHI index for 44 U.S. cities | [climatecentral.org](https://www.climatecentral.org/climate-matters/urban-heat-islands-2023) |
| Census ACS 2019 (5-yr) | Income, poverty rate, racial composition by tract | [data.census.gov](https://data.census.gov) |
| EPA EJScreen 2022 | Environmental justice metrics by tract (for robustness checks) | [epa.gov/ejscreen](https://www.epa.gov/ejscreen) |

> **Note:** The dataset currently in `data/` is a calibrated synthetic version built to match Climate Central's published aggregate statistics while the real data download is finalized. The code structure is identical to what will be used with the real data.

---

## How to Run

```bash
# Step 1: Pull and generate data
python3 code/01_data_pull.py

# Step 2: Clean the data
python3 code/02_clean.py

# Step 3: Run analysis and generate figures
python3 code/03_analyze.py
```

All outputs are saved to the `output/` directory.

---
