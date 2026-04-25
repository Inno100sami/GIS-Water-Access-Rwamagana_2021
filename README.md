# GIS Water Access Mapping — Rwamagana District

> **MSc Thesis:** Application of GIS for Mapping and Measuring Citizen's Access to Water Supply in Rwamagana District
>
> **Author:** NDAGIJIMANA Innocent · Reg No: M01287/2019
> **Institution:** University of Lay Adventists of Kigali (UNILAK), Faculty of Environmental Studies
> **Supervisor:** Dr. François Xavier Nshimiyimana (Ph.D.)
> **Submitted:** May 2022

---

## Live Dashboard

**[View Interactive Dashboard](https://Innocent-Ndagijimana.github.io/gis-water-access-rwamagana)**

The dashboard visualises all key research findings interactively — including sector-level water coverage maps, public water point distribution, tariff comparisons, reliability and quantity analysis.

---

## Research Summary

This study mapped and measured citizens' access to water supply across **14 sectors** of Rwamagana District, Eastern Province, Rwanda. It combined GIS spatial analysis with a household survey (n = 150) and secondary data from MININFRA, WASAC, and RURA.

### Key Findings

| Indicator | Value |
|---|---|
| Total district population studied | 392,513 |
| Population with water access | 220,527 (56.2%) |
| Total public water points | 415 |
| Total household connections | 15,064 |
| Mean water consumption | 29 L/capita/day |
| National minimum target | 20 L/capita/day |
| Sources with unreliable supply | 88% |

### Least-Served Sectors
| Sector | Coverage |
|---|---|
| Muyumbu | 29% |
| Nyakaliro | 37% |
| Nzige | 38% |
| Karenge | 41% |
| Muhazi | 44% |
| Gahengeri | 47% |

### Water Supply Systems
Three main operators manage water supply in the district:
- **WASAC** — Karenge WTP, Muhazi WTP, Gishari WTP
- **Ubuzima Bwiza MKM Ltd** — MKM WSS, Fumbwe-Gahengeri, Munyiginya WSS
- **Ayateke Star Ltd** — Byimana Gravity, Kabare-Nyabisindu, Gatare-Mabare-Byinza

---

## Repository Structure

```
gis-water-access-rwamagana/
├── index.html                  # Pre-built interactive dashboard (GitHub Pages entry point)
├── visualize.py                # Python script to regenerate index.html from data
├── requirements.txt            # Python dependencies (plotly, pandas)
├── data/
│   ├── sector_coverage.json    # Per-sector WSS, population, PWP, coverage data
│   ├── water_tariffs.json      # WASAC & rural water tariff tables (RURA 2021)
│   └── key_indicators.json     # District-wide indicators, reliability, quantity data
└── .github/
    └── workflows/
        └── deploy.yml          # GitHub Actions: auto-regenerate & deploy on push
```

---

## Getting Started

### View the dashboard locally

Simply open `index.html` in any modern browser — no server needed.

### Regenerate the dashboard from data

```bash
# 1. Clone the repository
git clone https://github.com/Innocent-Ndagijimana/gis-water-access-rwamagana.git
cd gis-water-access-rwamagana

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the visualisation script
python visualize.py

# 4. Open the output
open index.html   # macOS
start index.html  # Windows
```

### Update the data

Edit the JSON files in the `data/` folder and re-run `python visualize.py`.
Push to the `main` branch and GitHub Actions will automatically redeploy the dashboard.

---

## Enabling GitHub Pages

1. Go to **Settings → Pages** in your GitHub repository
2. Set **Source** to `GitHub Actions`
3. Push any commit to `main` — the workflow will build and deploy automatically

The live URL will be: `https://<your-username>.github.io/gis-water-access-rwamagana`

---

## Data Sources

| Source | Description |
|---|---|
| MININFRA WASH MIS (2021) | Water infrastructure inventory |
| RURA (2021) | Water tariff schedules |
| Rwamagana District (2021) | Sector population data |
| Household Survey (n=150) | Primary data: access, quantity, reliability, affordability |
| Government of Rwanda NST1 (2017–2024) | National water targets |

---

## Visualisations Included

1. **Water service coverage** — horizontal bar chart, colour-coded by coverage level
2. **Served vs unserved population** — stacked horizontal bar per sector
3. **Public water points** — bar chart by sector
4. **HH connections vs coverage** — bubble scatter (bubble = PWP count)
5. **Network length vs coverage** — scatter with colour scale
6. **Water quantity gauge** — actual vs national target
7. **Households vs 20 L/c/d target** — comparison bar
8. **Water supply reliability** — pie chart
9. **Household satisfaction** — pie chart
10. **WASAC tariffs** — bar chart by customer category
11. **Rural tariffs by system type** — grouped bar (excl. vs incl. VAT)

---

## Citation

```
NDAGIJIMANA, Innocent (2022). Application of GIS for Mapping and Measuring Citizen's
Access to Water Supply in Rwamagana District. MSc Thesis, Faculty of Environmental Studies,
University of Lay Adventists of Kigali (UNILAK), Rwanda.
```

---

*Submitted in partial fulfilment of the requirements for the award of Master of Science in Environmental and Development Studies, Option of Environmental Information System.*
