"""
MedPulse Analytics  -  Drug Sales Dataset Generator
Company: ZenithPharma India (fictional)
Period: Jan 2023 - Mar 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, json, os

np.random.seed(42)
random.seed(42)

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data") + os.sep
os.makedirs(OUT, exist_ok=True)

START = datetime(2023, 1, 1)
END   = datetime(2026, 3, 31)

# ── Master data ─────────────────────────────────────────
DRUGS = [
    {"drug_id":"D001","name":"CardioShield 10mg","category":"Cardiovascular","form":"Tablet","mrp":320,"cost":98,"launch":"2022-03-01","patent_expiry":"2027-06-01"},
    {"drug_id":"D002","name":"CardioShield 20mg","category":"Cardiovascular","form":"Tablet","mrp":580,"cost":172,"launch":"2022-03-01","patent_expiry":"2027-06-01"},
    {"drug_id":"D003","name":"DiabeGuard 500mg","category":"Diabetes","form":"Tablet","mrp":210,"cost":58,"launch":"2021-09-01","patent_expiry":"2026-09-01"},
    {"drug_id":"D004","name":"DiabeGuard Insulin","category":"Diabetes","form":"Injection","mrp":890,"cost":310,"launch":"2023-01-01","patent_expiry":"2029-01-01"},
    {"drug_id":"D005","name":"NeuroCalm 25mg","category":"Neurology","form":"Capsule","mrp":450,"cost":140,"launch":"2022-06-01","patent_expiry":"2028-06-01"},
    {"drug_id":"D006","name":"NeuroCalm 50mg","category":"Neurology","form":"Capsule","mrp":780,"cost":235,"launch":"2022-06-01","patent_expiry":"2028-06-01"},
    {"drug_id":"D007","name":"PulmoFlex Inhaler","category":"Respiratory","form":"Inhaler","mrp":1250,"cost":420,"launch":"2023-06-01","patent_expiry":"2030-01-01"},
    {"drug_id":"D008","name":"OncoClear 100mg","category":"Oncology","form":"Injection","mrp":8500,"cost":3200,"launch":"2023-09-01","patent_expiry":"2031-01-01"},
    {"drug_id":"D009","name":"OncoClear 250mg","category":"Oncology","form":"Injection","mrp":18500,"cost":6800,"launch":"2023-09-01","patent_expiry":"2031-01-01"},
    {"drug_id":"D010","name":"ImmunoBoost","category":"Immunology","form":"Tablet","mrp":650,"cost":195,"launch":"2024-01-01","patent_expiry":"2030-06-01"},
    {"drug_id":"D011","name":"GastroEase 40mg","category":"Gastroenterology","form":"Tablet","mrp":180,"cost":48,"launch":"2021-01-01","patent_expiry":"2025-12-01"},
    {"drug_id":"D012","name":"BoneDense 70mg","category":"Orthopedics","form":"Tablet","mrp":420,"cost":130,"launch":"2022-01-01","patent_expiry":"2028-01-01"},
]

REGIONS = [
    {"region_id":"R01","name":"North India","states":["Delhi","UP","Punjab","Haryana","Rajasthan"],"tier":"A"},
    {"region_id":"R02","name":"South India","states":["Karnataka","Tamil Nadu","Telangana","Kerala","AP"],"tier":"A"},
    {"region_id":"R03","name":"West India","states":["Maharashtra","Gujarat","Goa"],"tier":"A"},
    {"region_id":"R04","name":"East India","states":["West Bengal","Odisha","Bihar","Jharkhand"],"tier":"B"},
    {"region_id":"R05","name":"Central India","states":["MP","Chhattisgarh","UP-Central"],"tier":"B"},
    {"region_id":"R06","name":"Northeast India","states":["Assam","Meghalaya","Nagaland"],"tier":"C"},
]

CHANNELS = ["Hospital","Retail Pharmacy","E-Pharmacy","Government Tender","Clinic"]
CHAN_W    = [0.35, 0.30, 0.18, 0.10, 0.07]

REP_NAMES = [
    "Arjun Sharma","Priya Nair","Rahul Desai","Sneha Kulkarni","Vikram Reddy",
    "Ananya Singh","Deepak Mehta","Kavitha Raj","Suresh Iyer","Meera Pillai",
    "Rohan Kapoor","Divya Chatterjee","Anil Kumar","Pooja Verma","Sanjay Tiwari",
    "Lakshmi Subramanian","Nikhil Joshi","Ritu Agarwal","Vivek Pandey","Swati Bose",
]

# ── Generate reps ────────────────────────────────────────
reps = []
for i, name in enumerate(REP_NAMES):
    region = random.choice(REGIONS)
    reps.append({
        "rep_id": f"SR{i+1:03d}",
        "name": name,
        "region_id": region["region_id"],
        "region_name": region["name"],
        "experience_yr": round(random.uniform(1, 15), 1),
        "target_annual": random.choice([2400000, 3000000, 3600000, 4200000]),
    })

reps_df = pd.DataFrame(reps)
reps_df.to_csv(OUT+"reps.csv", index=False)

# ── Generate monthly drug sales ─────────────────────────
records = []
sid = 1

drugs_df = pd.DataFrame(DRUGS)
drugs_df.to_csv(OUT+"drugs.csv", index=False)

current = START
while current <= END:
    month_str = current.strftime("%Y-%m")
    months_since_start = (current.year - START.year)*12 + (current.month - START.month)

    # Seasonal multiplier (Q1 peak, Q3 dip in pharma)
    seasonal = 1.0 + 0.12 * np.sin((current.month - 3) * np.pi / 6)

    # Growth trend
    trend = 1 + 0.025 * months_since_start  # ~2.5% monthly growth

    for drug in DRUGS:
        launch = datetime.strptime(drug["launch"], "%Y-%m-%d")
        if current < launch:
            continue

        # Ramp-up for new drugs
        months_since_launch = (current.year - launch.year)*12 + (current.month - launch.month)
        ramp = min(1.0, 0.25 + 0.075 * months_since_launch)

        # Patent expiry concern (sales dip 6 months before)
        expiry = datetime.strptime(drug["patent_expiry"], "%Y-%m-%d")
        months_to_expiry = (expiry.year - current.year)*12 + (expiry.month - current.month)
        patent_factor = 0.85 if months_to_expiry < 6 else 1.0

        # Base units sold per drug per region
        base_units = {
            "Cardiovascular": 1200, "Diabetes": 1400, "Neurology": 800,
            "Respiratory": 600, "Oncology": 80, "Immunology": 500,
            "Gastroenterology": 1800, "Orthopedics": 700,
        }.get(drug["category"], 800)

        for region in REGIONS:
            tier_mult = {"A": 1.4, "B": 1.0, "C": 0.6}[region["tier"]]

            # Pick a rep for this region
            region_reps = [r for r in reps if r["region_id"] == region["region_id"]]
            rep = random.choice(region_reps) if region_reps else reps[0]

            for channel, cw in zip(CHANNELS, CHAN_W):
                units = int(base_units * cw * tier_mult * trend * seasonal * ramp * patent_factor
                            * np.random.uniform(0.75, 1.25))
                if units <= 0:
                    continue

                # Channel discount
                ch_disc = {"Hospital": 0.18, "Retail Pharmacy": 0.12,
                           "E-Pharmacy": 0.08, "Government Tender": 0.28, "Clinic": 0.10}[channel]

                gross_rev   = round(units * drug["mrp"], 2)
                discount    = round(gross_rev * ch_disc, 2)
                net_rev     = round(gross_rev - discount, 2)
                cogs        = round(units * drug["cost"], 2)
                gross_profit= round(net_rev - cogs, 2)
                gp_pct      = round(gross_profit / net_rev * 100, 2) if net_rev > 0 else 0
                returns     = round(gross_rev * random.uniform(0.01, 0.04), 2)

                records.append({
                    "sale_id":      f"S{sid:07d}",
                    "month":        month_str,
                    "drug_id":      drug["drug_id"],
                    "drug_name":    drug["name"],
                    "category":     drug["category"],
                    "form":         drug["form"],
                    "region_id":    region["region_id"],
                    "region_name":  region["name"],
                    "region_tier":  region["tier"],
                    "channel":      channel,
                    "rep_id":       rep["rep_id"],
                    "rep_name":     rep["name"],
                    "units_sold":   units,
                    "mrp":          drug["mrp"],
                    "gross_revenue":gross_rev,
                    "discount":     discount,
                    "discount_pct": round(ch_disc*100, 1),
                    "net_revenue":  net_rev,
                    "cogs":         cogs,
                    "gross_profit": gross_profit,
                    "gp_margin_pct":gp_pct,
                    "returns":      returns,
                    "year":         current.year,
                    "quarter":      f"Q{(current.month-1)//3+1}",
                    "month_num":    current.month,
                })
                sid += 1

    # next month
    if current.month == 12:
        current = current.replace(year=current.year+1, month=1)
    else:
        current = current.replace(month=current.month+1)

sales_df = pd.DataFrame(records)
sales_df.to_csv(OUT+"sales.csv", index=False)

# ── Rep targets vs actuals ────────────────────────────────
rep_actuals = sales_df.groupby(["rep_id","rep_name","year"])["net_revenue"].sum().reset_index()
rep_actuals = rep_actuals.merge(reps_df[["rep_id","target_annual","region_name","experience_yr"]], on="rep_id")
rep_actuals["achievement_pct"] = (rep_actuals["net_revenue"] / rep_actuals["target_annual"] * 100).round(1)
rep_actuals.to_csv(OUT+"rep_performance.csv", index=False)

# ── Summary KPIs ─────────────────────────────────────────
kpis = {
    "total_net_revenue": round(sales_df["net_revenue"].sum()),
    "total_units":       int(sales_df["units_sold"].sum()),
    "total_gross_profit":round(sales_df["gross_profit"].sum()),
    "avg_gp_margin":     round(sales_df["gp_margin_pct"].mean(), 1),
    "total_drugs":       sales_df["drug_id"].nunique(),
    "total_regions":     sales_df["region_id"].nunique(),
    "total_reps":        sales_df["rep_id"].nunique(),
    "months":            sales_df["month"].nunique(),
    "top_drug":          sales_df.groupby("drug_name")["net_revenue"].sum().idxmax(),
    "top_category":      sales_df.groupby("category")["net_revenue"].sum().idxmax(),
    "top_region":        sales_df.groupby("region_name")["net_revenue"].sum().idxmax(),
}
with open(OUT+"kpis.json","w") as f:
    json.dump(kpis, f, indent=2)

print("=" * 55)
print("  ZenithPharma India  -  Dataset Generated")
print("=" * 55)
print(f"  Sales records : {len(sales_df):,}")
print(f"  Drugs         : {sales_df['drug_id'].nunique()}")
print(f"  Regions       : {sales_df['region_id'].nunique()}")
print(f"  Months        : {sales_df['month'].nunique()}")
print(f"  Net Revenue   : Rs.{sales_df['net_revenue'].sum()/10000000:.2f} Cr")
print(f"  Avg GP Margin : {sales_df['gp_margin_pct'].mean():.1f}%")
print(f"  Top Drug      : {kpis['top_drug']}")
print(f"  Files saved to: {OUT}")
