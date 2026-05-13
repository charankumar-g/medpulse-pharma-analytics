# MedPulse Analytics — ZenithPharma India
## Drug Sales & Revenue Intelligence Dashboard

**Built by Charan Kumar G | Business Intelligence Analyst | 2026**

---

## Business Problem

ZenithPharma India sells 12 drugs across 6 therapeutic areas through 5 sales channels and 20 medical representatives across India. Leadership needs a single dashboard to answer:

1. Which drugs and categories are driving revenue and margins?
2. Which regions are underperforming and why?
3. Which sales reps are above/below target — and why?
4. What patent expiry risks threaten future revenue?
5. Where should the business invest next?

---

## Dashboard — 5 Views

| Tab | What it shows |
|---|---|
| 📊 Executive Overview | Revenue trend, KPIs, channel mix, quarterly YoY |
| 💊 Drug Performance | Drug ranking, margin vs revenue scatter, trends |
| 🗺️ Regional Analysis | Region revenue, category heatmap, tier analysis |
| 👤 Sales Force | Rep achievement %, leaderboard, experience vs revenue |
| 🔬 Insights & Strategy | Growth analysis, patent risk table, 3 recommendations |

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate dataset (only needed once)
python generate_data.py

# 3. Launch dashboard
streamlit run app.py
```

Open browser at: **http://localhost:8501**

---

## Dataset

Synthetically generated using realistic Indian pharma market benchmarks:

- **13,047** monthly sales records
- **12 drugs** across 8 therapeutic areas
- **6 regions** (Tier A/B/C)
- **5 sales channels** (Hospital, Retail, E-Pharmacy, Government, Clinic)
- **20 medical reps** with targets and actuals
- **39 months** of data (Jan 2023 – Mar 2026)
- **Rs.215 Cr** total net revenue

---

## Key Findings

| Insight | Finding |
|---|---|
| Top Category | Diabetes — highest revenue volume |
| Top Margin | Oncology — 65%+ GP margin |
| Patent Risk | DiabeGuard 500mg expires Sep 2026 (5 months) |
| Rep Performance | Avg achievement 94% — 6 reps below target |
| Underserved Market | Northeast India — Tier C, massive growth potential |

---

## Technical Stack

- **Python 3.12** — data generation and processing
- **Pandas** — data manipulation and aggregation
- **Plotly** — interactive charts (line, bar, scatter, heatmap, donut)
- **Streamlit** — dashboard framework with sidebar filters
- **Custom CSS** — DM Sans font, KPI cards, insight boxes, responsive layout

---

## Files

```
pharma_project/
├── app.py                  # Main Streamlit dashboard
├── generate_data.py        # Dataset generator
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── data/
    ├── sales.csv           # 13,047 monthly sales records
    ├── drugs.csv           # 12 drug master records
    ├── reps.csv            # 20 sales rep profiles
    ├── rep_performance.csv # Rep targets vs actuals by year
    └── kpis.json           # Pre-computed summary KPIs
```

---

## Author

**Charan Kumar G** | Business Intelligence Analyst  
📧 charankumar.career@gmail.com  
🔗 linkedin.com/in/charan-kumar-g  
💻 github.com/charankumar-g
