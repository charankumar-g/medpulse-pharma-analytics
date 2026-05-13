# MedPulse Analytics - ZenithPharma India
# Drug Sales & Revenue Intelligence Dashboard
# Author: Charan Kumar G | Business Intelligence Analyst
# Version 3.0 - Premium Dark UI

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json, os

st.set_page_config(
    page_title="MedPulse | ZenithPharma",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- FORCE dark theme via aggressive CSS injection --------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* -- FORCE dark everywhere -- */
html, body { background: #040812 !important; }
.stApp { background: #040812 !important; font-family: 'Inter', sans-serif !important; }
.main .block-container { background: #040812 !important; padding-top: 1.5rem !important; }
section[data-testid="stSidebar"] { background: #02060F !important; border-right: 1px solid #0F2044 !important; }
section[data-testid="stSidebar"] > div { background: #02060F !important; }
[data-testid="stHeader"] { background: rgba(4,8,18,0.95) !important; border-bottom: 1px solid #0F2044 !important; }

/* -- Force all text white -- */
html, body, .stApp, p, span, div, label, h1, h2, h3, h4 {
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* -- Sidebar internals -- */
[data-testid="stSidebar"] * { color: #94A3B8 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] { background: #0A1628 !important; }
[data-testid="stSidebar"] input { background: #0A1628 !important; }

/* -- Multiselect -- */
[data-baseweb="tag"] {
    background: rgba(59,130,246,0.25) !important;
    border: 1px solid rgba(59,130,246,0.4) !important;
}
[data-baseweb="tag"] span { color: #93C5FD !important; }

/* -- Tab bar -- */
div[data-baseweb="tab-list"] {
    background: #060D1E !important;
    border: 1px solid #0F2044 !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 3px !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    padding: 10px 18px !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"]:hover {
    background: rgba(59,130,246,0.1) !important;
    color: #93C5FD !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.45) !important;
}

/* -- Dataframe -- */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }
iframe { border-radius: 12px !important; }

/* -- Download button -- */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1D4ED8, #3B82F6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.35) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 6px 28px rgba(59,130,246,0.55) !important;
    transform: translateY(-2px) !important;
}

/* -- Multiselect dropdown -- */
[data-baseweb="popover"] { background: #0A1628 !important; border: 1px solid #1E3A5F !important; }
[data-baseweb="menu"] { background: #0A1628 !important; }
[data-baseweb="option"] { background: #0A1628 !important; color: #CBD5E1 !important; }
[data-baseweb="option"]:hover { background: #1E3A5F !important; }

/* -- Scrollbar -- */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #040812; }
::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2563EB; }

/* -- Divider -- */
hr { border-color: #0F2044 !important; }

/* -- Plotly chart background fix -- */
.js-plotly-plot { border-radius: 16px !important; }
</style>
""", unsafe_allow_html=True)

# -- Colour system ----------------------------------------
C = {
    "bg":      "#040812",
    "card":    "#060D1E",
    "card2":   "#080F20",
    "border":  "#0F2044",
    "border2": "#162952",
    "blue":    "#3B82F6",
    "blue2":   "#1D4ED8",
    "green":   "#10B981",
    "amber":   "#F59E0B",
    "red":     "#EF4444",
    "purple":  "#8B5CF6",
    "cyan":    "#06B6D4",
    "pink":    "#EC4899",
    "text":    "#E2E8F0",
    "muted":   "#475569",
    "dim":     "#1E293B",
}
PALETTE = ["#3B82F6","#10B981","#F59E0B","#EF4444","#8B5CF6","#06B6D4","#EC4899","#84CC16","#F97316","#14B8A6"]

# -- Plotly base layout -----------------------------------
def dark_fig(fig, title="", height=340, legend=True):
    fig.update_layout(
        title=dict(
            text=f'<span style="font-size:13px;font-weight:600;color:#94A3B8">{title}</span>',
            x=0, pad=dict(l=0, b=8)
        ),
        height=height,
        paper_bgcolor="rgba(6,13,30,0.0)",
        plot_bgcolor="rgba(6,13,30,0.0)",
        font=dict(family="Inter", size=11, color="#64748B"),
        margin=dict(l=8, r=8, t=44 if title else 12, b=8),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=10, color="#64748B"),
            bgcolor="rgba(0,0,0,0)", borderwidth=0
        ) if legend else dict(visible=False),
        hoverlabel=dict(
            bgcolor="#0F172A", bordercolor="#1E3A5F",
            font=dict(family="Inter", size=12, color="#E2E8F0")
        ),
        colorway=PALETTE,
        xaxis=dict(
            showgrid=False, zeroline=False,
            linecolor="#0F2044", tickcolor="#0F2044",
            tickfont=dict(color="#334155", size=10),
        ),
        yaxis=dict(
            gridcolor="rgba(15,32,68,0.8)",
            zeroline=False, linecolor="rgba(0,0,0,0)",
            tickfont=dict(color="#334155", size=10),
        ),
    )
    return fig

# -- Load data --------------------------------------------
@st.cache_data
def load():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    s  = pd.read_csv(f"{base}/sales.csv")
    d  = pd.read_csv(f"{base}/drugs.csv")
    r  = pd.read_csv(f"{base}/reps.csv")
    rp = pd.read_csv(f"{base}/rep_performance.csv")
    with open(f"{base}/kpis.json") as f: k = json.load(f)
    s["month_dt"] = pd.to_datetime(s["month"])
    return s, d, r, rp, k

sales, drugs, reps, rep_perf, kpis = load()

# -- Sidebar ----------------------------------------------
with st.sidebar:
    # Brand block
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #060D1E, #0A1628);
        border: 1px solid #0F2044;
        border-radius: 16px;
        padding: 22px 16px;
        margin: 12px 8px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
    ">
        <div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;
            border-radius:50%;background:rgba(59,130,246,0.08);"></div>
        <div style="font-size:38px;margin-bottom:8px">💊</div>
        <div style="font-size:18px;font-weight:800;color:#F1F5F9;letter-spacing:-0.5px">MedPulse</div>
        <div style="font-size:11px;color:#3B82F6;font-weight:600;margin-top:3px;letter-spacing:0.5px">
            ZENITHPHARMA INDIA
        </div>
        <div style="margin-top:12px;padding-top:12px;border-top:1px solid #0F2044;
            font-size:10px;color:#1E3A5F;font-weight:500;letter-spacing:0.5px">
            DRUG SALES INTELLIGENCE v3.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:10px;font-weight:700;letter-spacing:1.5px;color:#1E3A5F;text-transform:uppercase;margin:0 0 10px 4px">FILTERS</p>', unsafe_allow_html=True)

    years       = sorted(sales["year"].unique())
    sel_years   = st.multiselect("Fiscal Year", years, default=years)
    cats        = sorted(sales["category"].unique())
    sel_cats    = st.multiselect("Therapeutic Area", cats, default=cats)
    regions     = sorted(sales["region_name"].unique())
    sel_regions = st.multiselect("Region", regions, default=regions)
    channels    = sorted(sales["channel"].unique())
    sel_chans   = st.multiselect("Sales Channel", channels, default=channels)

    st.markdown(f"""
    <div style="margin-top:24px;padding:14px;border-radius:12px;
        background:#060D1E;border:1px solid #0F2044;text-align:center">
        <div style="font-size:10px;color:#1E3A5F;letter-spacing:1px;font-weight:600">PORTFOLIO PROJECT</div>
        <div style="font-size:13px;font-weight:700;color:#3B82F6;margin-top:6px">Charan Kumar G</div>
        <div style="font-size:11px;color:#334155;margin-top:3px">Business Intelligence Analyst</div>
        <div style="font-size:10px;color:#1E3A5F;margin-top:2px">April 2026</div>
    </div>
    """, unsafe_allow_html=True)

# -- Filter -----------------------------------------------
mask = (
    sales["year"].isin(sel_years) &
    sales["category"].isin(sel_cats) &
    sales["region_name"].isin(sel_regions) &
    sales["channel"].isin(sel_chans)
)
df = sales[mask].copy()

# -- Helpers ----------------------------------------------
def shdr(icon, text):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:28px 0 16px">
        <span style="font-size:16px">{icon}</span>
        <span style="font-size:10px;font-weight:700;letter-spacing:2px;
            text-transform:uppercase;color:#1D4ED8;white-space:nowrap">{text}</span>
        <div style="flex:1;height:1px;
            background:linear-gradient(90deg,#0F2044,transparent)"></div>
    </div>
    """, unsafe_allow_html=True)

def kcard(col, label, val_str, icon, top_color, delta=None):
    delta_html = ""
    if delta is not None:
        color = "#10B981" if delta >= 0 else "#EF4444"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div style="font-size:12px;font-weight:600;color:{color};margin-top:4px">{arrow} {abs(delta):.1f}% YoY</div>'
    col.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #060D1E 0%, #080F22 100%);
        border: 1px solid #0F2044;
        border-top: 3px solid {top_color};
        border-radius: 16px;
        padding: 20px 18px 16px;
        position: relative;
        overflow: hidden;
        min-height: 110px;
    ">
        <div style="position:absolute;right:14px;top:12px;font-size:26px;opacity:0.12">{icon}</div>
        <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
            text-transform:uppercase;color:#1E3A5F;margin-bottom:8px">{label}</div>
        <div style="font-size:24px;font-weight:800;color:#F1F5F9;
            letter-spacing:-0.5px;line-height:1">{val_str}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# -- Compute KPIs -----------------------------------------
total_rev    = df["net_revenue"].sum()
total_profit = df["gross_profit"].sum()
avg_gp       = df["gp_margin_pct"].mean()
total_units  = df["units_sold"].sum()
n_drugs      = df["drug_id"].nunique()
rev_2024     = df[df["year"]==2024]["net_revenue"].sum()
rev_2025     = df[df["year"]==2025]["net_revenue"].sum()
yoy          = (rev_2025-rev_2024)/rev_2024*100 if rev_2024>0 else 0

def fmt_cr(v): return f"Rs.{v/1e7:.2f}Cr" if v>=1e7 else f"Rs.{v/1e5:.1f}L"

# ==========================================================
# TABS
# ==========================================================
tabs = st.tabs(["📊  Executive","💊  Drug Intel","🗺️  Regions","👤  Sales Force","🔬  Strategy"])

# ================ TAB 1: EXECUTIVE =======================
with tabs[0]:
    # Page header
    st.markdown(f"""
    <div style="margin-bottom:24px">
        <div style="font-size:30px;font-weight:900;color:#F1F5F9;letter-spacing:-1px">
            Executive Overview
        </div>
        <div style="font-size:13px;color:#334155;margin-top:4px">
            ZenithPharma India &nbsp;·&nbsp; Drug Sales Intelligence &nbsp;·&nbsp; Jan 2023 - Mar 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k = st.columns(5, gap="small")
    kcard(k[0], "Net Revenue",   fmt_cr(total_rev),    "💰", C["blue"],   yoy)
    kcard(k[1], "Gross Profit",  fmt_cr(total_profit), "📈", C["green"],  None)
    kcard(k[2], "GP Margin",     f"{avg_gp:.1f}%",     "🎯", C["purple"], None)
    kcard(k[3], "Units Sold",    f"{total_units/1e6:.2f}M", "📦", C["amber"], None)
    kcard(k[4], "Active Drugs",  str(n_drugs),         "💊", C["cyan"],   None)

    shdr("📉", "Revenue Performance")
    c1, c2 = st.columns([2.2,1], gap="medium")

    with c1:
        mrev = df.groupby("month_dt").agg(
            rev=("net_revenue","sum"), gp=("gross_profit","sum")
        ).reset_index().sort_values("month_dt")
        mrev["ma3"] = mrev["rev"].rolling(3).mean()

        fig = go.Figure()
        # Area fill
        fig.add_trace(go.Scatter(
            x=mrev["month_dt"], y=mrev["rev"]/1e5,
            fill="tozeroy", fillcolor="rgba(59,130,246,0.06)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False,
            hoverinfo="skip"
        ))
        # Revenue line
        fig.add_trace(go.Scatter(
            x=mrev["month_dt"], y=mrev["rev"]/1e5,
            line=dict(color="#3B82F6", width=2.5),
            name="Net Revenue",
            hovertemplate="<b>%{x|%b %Y}</b><br>Rs.%{y:.1f}L<extra></extra>"
        ))
        # Profit line
        fig.add_trace(go.Scatter(
            x=mrev["month_dt"], y=mrev["gp"]/1e5,
            line=dict(color="#10B981", width=2, dash="dot"),
            name="Gross Profit",
            hovertemplate="<b>%{x|%b %Y}</b><br>Rs.%{y:.1f}L<extra></extra>"
        ))
        # MA line
        fig.add_trace(go.Scatter(
            x=mrev["month_dt"], y=mrev["ma3"]/1e5,
            line=dict(color="rgba(139,92,246,0.5)", width=1.5, dash="dash"),
            name="3M Moving Avg",
            hovertemplate="Rs.%{y:.1f}L<extra>3M Avg</extra>"
        ))
        # Peak annotation
        peak = mrev.loc[mrev["rev"].idxmax()]
        fig.add_annotation(
            x=peak["month_dt"], y=peak["rev"]/1e5,
            text=f"<b>Peak</b><br>Rs.{peak['rev']/1e5:.0f}L",
            showarrow=True, arrowhead=2, arrowcolor="#3B82F6",
            font=dict(size=10, color="#93C5FD", family="Inter"),
            bgcolor="#060D1E", bordercolor="#1D4ED8",
            borderwidth=1, borderpad=4, ax=0, ay=-44
        )
        dark_fig(fig, "Monthly Revenue & Profit Trend (Rs. Lakhs)", 320)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_rev = df.groupby("category")["net_revenue"].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=cat_rev["category"],
            values=cat_rev["net_revenue"],
            hole=0.65,
            marker=dict(colors=PALETTE, line=dict(color="#040812", width=3)),
            textposition="outside",
            textinfo="label+percent",
            textfont=dict(size=9, color="#64748B", family="Inter"),
            hovertemplate="<b>%{label}</b><br>Rs.%{value:,.0f}<br>%{percent}<extra></extra>"
        ))
        fig2.add_annotation(
            text=f"<b style='font-size:15px'>{fmt_cr(total_rev)}</b><br><span style='font-size:10px;color:#334155'>Total Rev</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#F1F5F9", family="Inter")
        )
        dark_fig(fig2, "Revenue by Therapeutic Area", 320, legend=False)
        st.plotly_chart(fig2, use_container_width=True)

    shdr("📊", "Channel & Quarterly Breakdown")
    c3, c4 = st.columns(2, gap="medium")

    with c3:
        chan = df.groupby("channel")["net_revenue"].sum().reset_index().sort_values("net_revenue")
        fig3 = go.Figure(go.Bar(
            y=chan["channel"], x=chan["net_revenue"]/1e5,
            orientation="h",
            marker=dict(
                color=chan["net_revenue"]/chan["net_revenue"].max(),
                colorscale=[[0,"#0F2044"],[0.5,"#1D4ED8"],[1,"#60A5FA"]],
                line=dict(color="rgba(0,0,0,0)")
            ),
            text=[f"Rs.{v:.0f}L" for v in chan["net_revenue"]/1e5],
            textposition="outside",
            textfont=dict(color="#475569", size=10),
            hovertemplate="<b>%{y}</b><br>Rs.%{x:.0f}L<extra></extra>"
        ))
        dark_fig(fig3, "Revenue by Sales Channel (Rs. Lakhs)", 270)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        qrev = df.groupby(["year","quarter"])["net_revenue"].sum().reset_index()
        qrev["year"] = qrev["year"].astype(str)
        yr_cols = {"2023":"#0F2044","2024":"#1D4ED8","2025":"#3B82F6","2026":"#93C5FD"}
        fig4 = px.bar(qrev, x="quarter", y="net_revenue", color="year",
                      barmode="group", color_discrete_map=yr_cols)
        fig4.update_traces(
            marker_line_color="rgba(0,0,0,0)", width=0.18,
            hovertemplate="<b>%{x} %{data.name}</b><br>Rs.%{y:,.0f}<extra></extra>"
        )
        fig4.update_layout(yaxis_tickformat=".2s")
        dark_fig(fig4, "Quarterly Revenue by Year", 270)
        st.plotly_chart(fig4, use_container_width=True)

    # Insight cards
    shdr("💡", "Auto-Generated Insights")
    top_cat   = df.groupby("category")["net_revenue"].sum().idxmax()
    top_chan  = df.groupby("channel")["net_revenue"].sum().idxmax()
    low_m_cat = df.groupby("category")["gp_margin_pct"].mean().idxmin()
    low_m_val = df.groupby("category")["gp_margin_pct"].mean().min()
    top_share = df[df["category"]==top_cat]["net_revenue"].sum()/total_rev*100

    i1, i2, i3 = st.columns(3, gap="small")
    for col, icon, color, bg, title, body in [
        (i1,"✅","#10B981","rgba(16,163,74,0.07)",
         "Top Therapeutic Area",
         f"{top_cat} leads at <b>{top_share:.0f}%</b> revenue share. Strong pipeline candidate for next portfolio expansion."),
        (i2,"📊","#3B82F6","rgba(59,130,246,0.07)",
         "Revenue Growth",
         f"{top_chan} channel dominates. YoY growth is <b>{yoy:+.1f}%</b> (2024-2025)  -  above pharma industry avg of 18-22%."),
        (i3,"⚠️","#F59E0B","rgba(245,158,11,0.07)",
         "Margin Alert",
         f"{low_m_cat} shows the lowest GP margin at <b>{low_m_val:.1f}%</b>. Renegotiate COGS and review discount policy urgently."),
    ]:
        col.markdown(f"""
        <div style="background:{bg};border:1px solid rgba(255,255,255,0.05);
            border-left:3px solid {color};border-radius:12px;
            padding:16px;min-height:110px">
            <div style="font-size:12px;font-weight:700;color:{color};margin-bottom:8px">
                {icon} {title}
            </div>
            <div style="font-size:12.5px;color:#64748B;line-height:1.7">{body}</div>
        </div>
        """, unsafe_allow_html=True)


# ================ TAB 2: DRUG INTEL ======================
with tabs[1]:
    st.markdown('<div style="font-size:30px;font-weight:900;color:#F1F5F9;letter-spacing:-1px;margin-bottom:4px">Drug Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:20px">Revenue, margins, growth, and competitive positioning by drug</div>', unsafe_allow_html=True)

    drug_sum = df.groupby(["drug_id","drug_name","category","form"]).agg(
        net_revenue=("net_revenue","sum"), units_sold=("units_sold","sum"),
        gross_profit=("gross_profit","sum"), avg_gp=("gp_margin_pct","mean"),
        avg_disc=("discount_pct","mean")
    ).reset_index().sort_values("net_revenue", ascending=False)
    drug_sum["rev_share"] = (drug_sum["net_revenue"]/drug_sum["net_revenue"].sum()*100).round(1)

    shdr("🏆", "Drug Revenue Ranking")
    c1, c2 = st.columns([3,2], gap="medium")

    with c1:
        top = drug_sum.head(10)
        fig = go.Figure(go.Bar(
            y=top["drug_name"], x=top["net_revenue"]/1e7,
            orientation="h",
            marker=dict(
                color=np.linspace(0.2, 1, len(top)),
                colorscale=[[0,"#0F2044"],[0.4,"#1D4ED8"],[0.7,"#3B82F6"],[1,"#93C5FD"]],
                line=dict(color="rgba(0,0,0,0)")
            ),
            text=[f"Rs.{v:.1f}Cr" for v in top["net_revenue"]/1e7],
            textposition="outside", textfont=dict(color="#475569",size=10),
            customdata=top[["category","rev_share"]].values,
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>Rs.%{x:.2f}Cr (%{customdata[1]:.1f}%)<extra></extra>"
        ))
        fig.update_layout(yaxis=dict(autorange="reversed"))
        dark_fig(fig, "Top 10 Drugs by Net Revenue (Rs. Crores)", 380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.scatter(drug_sum, x="avg_gp", y="net_revenue",
                          size="units_sold", color="category",
                          hover_name="drug_name",
                          color_discrete_sequence=PALETTE, size_max=44,
                          labels={"avg_gp":"GP Margin %","net_revenue":"Net Revenue"})
        fig2.update_traces(
            marker=dict(line=dict(color="rgba(0,0,0,0.4)",width=1), opacity=0.85),
            hovertemplate="<b>%{hovertext}</b><br>Rev: Rs.%{y:,.0f}<br>GP: %{x:.1f}%<extra></extra>"
        )
        mx = drug_sum["avg_gp"].median()
        my = drug_sum["net_revenue"].median()
        fig2.add_hline(y=my, line_dash="dot", line_color="rgba(15,32,68,0.8)", line_width=1)
        fig2.add_vline(x=mx, line_dash="dot", line_color="rgba(15,32,68,0.8)", line_width=1)
        fig2.add_annotation(x=drug_sum["avg_gp"].max()*0.9, y=drug_sum["net_revenue"].max()*0.95,
            text="STARS", font=dict(size=9, color="#10B981", family="Inter"),
            showarrow=False, bgcolor="rgba(16,185,129,0.1)",
            bordercolor="rgba(16,185,129,0.3)", borderwidth=1, borderpad=4)
        dark_fig(fig2, "Revenue vs Margin Matrix (size = units sold)", 380)
        st.plotly_chart(fig2, use_container_width=True)

    shdr("📈", "Multi-Drug Sales Trend")
    sel_drugs = st.multiselect("Select drugs to compare",
                                sorted(df["drug_name"].unique()),
                                default=list(drug_sum["drug_name"].head(4)))
    if sel_drugs:
        trend = df[df["drug_name"].isin(sel_drugs)].groupby(["month_dt","drug_name"])["net_revenue"].sum().reset_index()
        fig3  = px.line(trend, x="month_dt", y="net_revenue", color="drug_name",
                        color_discrete_sequence=PALETTE,
                        labels={"net_revenue":"Net Revenue","month_dt":"Month","drug_name":"Drug"})
        fig3.update_traces(mode="lines+markers",
                           marker=dict(size=5, line=dict(color="#040812",width=1)),
                           line=dict(width=2.2))
        dark_fig(fig3, "Monthly Net Revenue Trend by Drug", 300)
        st.plotly_chart(fig3, use_container_width=True)

    shdr("📋", "Drug Summary Table")
    tbl = drug_sum[["drug_name","category","form","net_revenue","units_sold","avg_gp","rev_share","avg_disc"]].copy()
    tbl.columns = ["Drug","Category","Form","Net Revenue","Units","GP Margin %","Rev Share %","Avg Discount %"]
    tbl["Net Revenue"]    = tbl["Net Revenue"].apply(lambda x: f"Rs.{x/1e7:.2f}Cr")
    tbl["GP Margin %"]    = tbl["GP Margin %"].apply(lambda x: f"{x:.1f}%")
    tbl["Rev Share %"]    = tbl["Rev Share %"].apply(lambda x: f"{x:.1f}%")
    tbl["Avg Discount %"] = tbl["Avg Discount %"].apply(lambda x: f"{x:.1f}%")
    tbl["Units"]          = tbl["Units"].apply(lambda x: f"{x:,}")
    st.dataframe(tbl, use_container_width=True, hide_index=True)


# ================ TAB 3: REGIONS =========================
with tabs[2]:
    st.markdown('<div style="font-size:30px;font-weight:900;color:#F1F5F9;letter-spacing:-1px;margin-bottom:4px">Regional Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:20px">Pan-India sales performance by region, tier, and therapeutic category</div>', unsafe_allow_html=True)

    reg = df.groupby(["region_name","region_tier"]).agg(
        rev=("net_revenue","sum"), units=("units_sold","sum"),
        gp=("gp_margin_pct","mean")
    ).reset_index().sort_values("rev", ascending=False)
    reg["share"] = (reg["rev"]/reg["rev"].sum()*100).round(1)

    shdr("🗺️","Regional Revenue")
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        tier_c = {"A":"#3B82F6","B":"#F59E0B","C":"#EF4444"}
        bc     = [tier_c.get(t,"#64748B") for t in reg["region_tier"]]
        fig    = go.Figure(go.Bar(
            y=reg["region_name"], x=reg["rev"]/1e7,
            orientation="h",
            marker=dict(color=bc, line=dict(color="rgba(0,0,0,0)")),
            text=[f"Rs.{v:.1f}Cr ({s:.0f}%)" for v,s in zip(reg["rev"]/1e7, reg["share"])],
            textposition="outside", textfont=dict(color="#475569",size=10),
            hovertemplate="<b>%{y}</b><br>Rs.%{x:.2f}Cr<extra></extra>"
        ))
        for tier, col in tier_c.items():
            fig.add_trace(go.Bar(x=[None],y=[None],name=f"Tier {tier}",
                                  marker_color=col, showlegend=True))
        dark_fig(fig, "Net Revenue by Region (Rs. Crores)", 320)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        heat  = df.groupby(["region_name","category"])["net_revenue"].sum().reset_index()
        pivot = heat.pivot(index="region_name",columns="category",values="net_revenue").fillna(0)
        fig2  = px.imshow(pivot/1e5, aspect="auto",
                          color_continuous_scale=[[0,"#040812"],[0.2,"#0F2044"],
                                                  [0.5,"#1D4ED8"],[0.8,"#3B82F6"],[1,"#93C5FD"]],
                          labels=dict(color="Rs.L"), text_auto=".0f")
        fig2.update_traces(
            textfont=dict(color="rgba(255,255,255,0.7)", size=9),
            hovertemplate="<b>%{y} x %{x}</b><br>Rs.%{z:.0f}L<extra></extra>"
        )
        fig2.update_coloraxes(colorbar=dict(
            tickfont=dict(color="#334155",size=9),
            title=dict(font=dict(color="#334155",size=9))
        ))
        dark_fig(fig2, "Revenue Heatmap: Region x Category (Rs. Lakhs)", 320, legend=False)
        st.plotly_chart(fig2, use_container_width=True)

    shdr("📊","Channel Mix by Region")
    chan_reg = df.groupby(["region_name","channel"])["net_revenue"].sum().reset_index()
    fig3 = px.bar(chan_reg, x="region_name", y="net_revenue", color="channel",
                  barmode="stack", color_discrete_sequence=PALETTE)
    fig3.update_traces(marker_line_color="rgba(0,0,0,0)",
                       hovertemplate="<b>%{x}</b> · %{data.name}<br>Rs.%{y:,.0f}<extra></extra>")
    dark_fig(fig3, "Channel Mix by Region (stacked)", 280)
    st.plotly_chart(fig3, use_container_width=True)

    tot = reg["rev"].sum()
    tA  = reg[reg["region_tier"]=="A"]["rev"].sum()
    tB  = reg[reg["region_tier"]=="B"]["rev"].sum()
    tC  = reg[reg["region_tier"]=="C"]["rev"].sum()
    for col,icon,color,title,body in zip(
        st.columns(3, gap="small"),
        ["🔵","🟡","🔴"],
        ["#3B82F6","#F59E0B","#EF4444"],
        ["Tier A  -  Core Markets","Tier B  -  Growth Zone","Tier C  -  Underserved"],
        [f"North, South & West India drive <b>{tA/tot*100:.0f}%</b> of revenue. Hospital and E-Pharmacy strongest.",
         f"East & Central India at <b>{tB/tot*100:.0f}%</b>. Deploy 4 reps  -  high potential in Diabetes/Cardio.",
         f"Northeast at only <b>{tC/tot*100:.0f}%</b>. Partner with local distributors. 3x ROI vs Tier A expansion."]
    ):
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
            border-left:3px solid {color};border-radius:12px;padding:16px">
            <div style="font-size:12px;font-weight:700;color:{color};margin-bottom:8px">{icon} {title}</div>
            <div style="font-size:12.5px;color:#64748B;line-height:1.7">{body}</div>
        </div>""", unsafe_allow_html=True)


# ================ TAB 4: SALES FORCE =====================
with tabs[3]:
    st.markdown('<div style="font-size:30px;font-weight:900;color:#F1F5F9;letter-spacing:-1px;margin-bottom:4px">Sales Force</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:20px">Rep-level achievement, rankings, and territory productivity</div>', unsafe_allow_html=True)

    rdf      = rep_perf[rep_perf["year"].isin(sel_years)].copy()
    avg_ach  = rdf["achievement_pct"].mean()
    top_rep  = rdf.loc[rdf["achievement_pct"].idxmax(),"rep_name"]
    top_ach  = rdf["achievement_pct"].max()
    pct_on   = (rdf["achievement_pct"]>=100).mean()*100

    k = st.columns(4, gap="small")
    kcard(k[0],"Avg Achievement", f"{avg_ach:.0f}%",    "🎯", C["blue"] if avg_ach>=100 else C["red"])
    kcard(k[1],"Top Performer",   f"{top_ach:.0f}%",    "🏆", C["green"])
    kcard(k[2],"On Target",       f"{pct_on:.0f}%",     "✅", C["purple"])
    kcard(k[3],"Active Reps",     str(rdf["rep_id"].nunique()), "👤", C["amber"])

    shdr("📊","Achievement vs Target")
    c1, c2 = st.columns([3,2], gap="medium")

    with c1:
        latest = rdf[rdf["year"]==rdf["year"].max()].sort_values("achievement_pct",ascending=True)
        bc2    = ["#10B981" if v>=100 else "#EF4444" for v in latest["achievement_pct"]]
        fig    = go.Figure(go.Bar(
            y=latest["rep_name"], x=latest["achievement_pct"],
            orientation="h",
            marker=dict(color=bc2, line=dict(color="rgba(0,0,0,0)")),
            text=[f"{v:.0f}%" for v in latest["achievement_pct"]],
            textposition="outside", textfont=dict(color="#475569",size=10),
            hovertemplate="<b>%{y}</b><br>Achievement: %{x:.1f}%<extra></extra>"
        ))
        fig.add_vline(x=100, line_dash="dash", line_color="rgba(59,130,246,0.4)",
                      line_width=1.5, annotation_text="Target 100%",
                      annotation_font=dict(color="#3B82F6",size=10),
                      annotation_position="top right")
        dark_fig(fig, f"Rep Achievement % ({rdf['year'].max()})", 460)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.histogram(rdf, x="achievement_pct", nbins=12,
                            color_discrete_sequence=["#3B82F6"])
        fig2.update_traces(marker_line_color="rgba(0,0,0,0)",
                           hovertemplate="%{x:.0f}%<br>Count: %{y}<extra></extra>")
        fig2.add_vline(x=100, line_dash="dash", line_color="#EF4444", line_width=1.5)
        dark_fig(fig2, "Achievement Distribution", 215)
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(rdf, x="experience_yr", y="net_revenue",
                          color="region_name", hover_name="rep_name",
                          color_discrete_sequence=PALETTE)
        fig3.update_traces(marker=dict(size=9, line=dict(color="#040812",width=1)),
                           hovertemplate="<b>%{hovertext}</b><br>%{x:.1f}yr exp<br>Rs.%{y:,.0f}<extra></extra>")
        dark_fig(fig3, "Experience vs Revenue Generated", 215)
        st.plotly_chart(fig3, use_container_width=True)

    shdr("🏅","Leaderboard")
    lb = rdf.groupby(["rep_name","region_name"]).agg(
        Revenue=("net_revenue","sum"), Achievement=("achievement_pct","mean")
    ).reset_index().sort_values("Revenue",ascending=False).reset_index(drop=True)
    lb.index += 1
    lb["Revenue"]     = lb["Revenue"].apply(lambda x: f"Rs.{x/1e5:.1f}L")
    lb["Achievement"] = lb["Achievement"].apply(lambda x: f"{x:.0f}%")
    lb.columns        = ["Rep Name","Region","Total Revenue","Avg Achievement"]
    st.dataframe(lb, use_container_width=True)


# ================ TAB 5: STRATEGY ========================
with tabs[4]:
    st.markdown('<div style="font-size:30px;font-weight:900;color:#F1F5F9;letter-spacing:-1px;margin-bottom:4px">Insights & Strategy</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:20px">Data-driven strategic recommendations for ZenithPharma leadership</div>', unsafe_allow_html=True)

    shdr("📈","Growth Analysis")
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        c24 = df[df["year"]==2024].groupby("category")["net_revenue"].sum()
        c25 = df[df["year"]==2025].groupby("category")["net_revenue"].sum()
        gr  = pd.DataFrame({"2024":c24,"2025":c25}).dropna()
        gr["pct"] = ((gr["2025"]-gr["2024"])/gr["2024"]*100).round(1)
        gr  = gr.reset_index().sort_values("pct",ascending=True)
        fig = go.Figure(go.Bar(
            y=gr["category"], x=gr["pct"], orientation="h",
            marker=dict(
                color=gr["pct"],
                colorscale=[[0,"#EF4444"],[0.45,"#F59E0B"],[0.7,"#10B981"],[1,"#34D399"]],
                line=dict(color="rgba(0,0,0,0)")
            ),
            text=[f"{v:+.1f}%" for v in gr["pct"]],
            textposition="outside", textfont=dict(color="#475569",size=10),
            hovertemplate="<b>%{y}</b><br>Growth: %{x:+.1f}%<extra></extra>"
        ))
        fig.add_vline(x=0, line_color="rgba(15,32,68,0.8)", line_width=1)
        dark_fig(fig, "YoY Revenue Growth by Category (2024 to 2025)", 300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cg = df.groupby("category").agg(rev=("net_revenue","sum"),gp=("gross_profit","sum")).reset_index()
        cg["margin"] = (cg["gp"]/cg["rev"]*100).round(1)
        cg = cg.sort_values("margin", ascending=False)
        fig2 = go.Figure(go.Bar(
            x=cg["category"], y=cg["margin"],
            marker=dict(
                color=cg["margin"],
                colorscale=[[0,"#7C3AED"],[0.4,"#2563EB"],[0.7,"#10B981"],[1,"#34D399"]],
                line=dict(color="rgba(0,0,0,0)")
            ),
            text=[f"{v:.1f}%" for v in cg["margin"]],
            textposition="outside", textfont=dict(color="#475569",size=10),
            hovertemplate="<b>%{x}</b><br>GP Margin: %{y:.1f}%<extra></extra>"
        ))
        avg_m = cg["margin"].mean()
        fig2.add_hline(y=avg_m, line_dash="dot", line_color="rgba(59,130,246,0.3)",
                       annotation_text=f"Avg {avg_m:.1f}%",
                       annotation_font=dict(color="#3B82F6",size=10),
                       annotation_position="right")
        dark_fig(fig2, "Gross Profit Margin by Therapeutic Area", 300)
        st.plotly_chart(fig2, use_container_width=True)

    shdr("⚠️","Patent Expiry Risk Monitor")
    patents = [
        ("GastroEase 40mg",   "Gastroenterology","Dec 2025", 0,  "6.1%", "EXPIRED",  "#8B5CF6","rgba(139,92,246,0.15)"),
        ("DiabeGuard 500mg",  "Diabetes",        "Sep 2026", 5,  "8.2%", "CRITICAL", "#EF4444","rgba(239,68,68,0.15)"),
        ("CardioShield 10mg", "Cardiovascular",  "Jun 2027", 14, "7.4%", "HIGH",     "#F97316","rgba(249,115,22,0.12)"),
        ("CardioShield 20mg", "Cardiovascular",  "Jun 2027", 14, "9.1%", "HIGH",     "#F97316","rgba(249,115,22,0.12)"),
        ("NeuroCalm 25mg",    "Neurology",       "Jun 2028", 26, "9.8%", "MEDIUM",   "#F59E0B","rgba(245,158,11,0.10)"),
        ("BoneDense 70mg",    "Orthopedics",     "Jan 2028", 21, "5.5%", "MEDIUM",   "#F59E0B","rgba(245,158,11,0.10)"),
        ("ImmunoBoost",       "Immunology",      "Jun 2030", 50, "7.3%", "LOW",      "#10B981","rgba(16,185,129,0.08)"),
        ("OncoClear 100mg",   "Oncology",        "Jan 2031", 57,"11.2%", "LOW",      "#10B981","rgba(16,185,129,0.08)"),
    ]
    rows = ""
    for drug,cat,expiry,months,share,risk,rc,bg in patents:
        bar_w = max(4, min(100, (60-months)/60*100)) if months>0 else 100
        bar_c = rc
        rows += f"""<tr>
            <td><b style="color:#E2E8F0">{drug}</b></td>
            <td style="color:#64748B">{cat}</td>
            <td style="color:#94A3B8">{expiry}</td>
            <td>
                <div style="display:flex;align-items:center;gap:8px">
                    <div style="width:60px;height:4px;background:#0F2044;border-radius:2px">
                        <div style="width:{bar_w}%;height:100%;background:{bar_c};border-radius:2px"></div>
                    </div>
                    <span style="color:#64748B;font-size:12px">{months}mo</span>
                </div>
            </td>
            <td><b style="color:#60A5FA">{share}</b></td>
            <td><span style="background:{bg};color:{rc};border:1px solid {rc}40;
                padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700">{risk}</span></td>
        </tr>"""

    st.markdown(f"""
    <table style="width:100%;border-collapse:separate;border-spacing:0 3px">
        <tr style="background:rgba(59,130,246,0.08)">
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left;border-radius:8px 0 0 8px">Drug</th>
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left">Category</th>
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left">Expiry</th>
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left">Time Left</th>
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left">Rev Share</th>
            <th style="padding:10px 14px;color:#1D4ED8;font-size:10px;letter-spacing:1px;
                text-transform:uppercase;font-weight:700;text-align:left;border-radius:0 8px 8px 0">Risk</th>
        </tr>
        {rows}
    </table>
    """, unsafe_allow_html=True)

    shdr("🚀","Strategic Recommendations")
    recs = [
        ("#EF4444","rgba(239,68,68,0.06)","🚨","CRITICAL  -  ACT NOW",
         "Defend Against DiabeGuard 500mg Patent Cliff",
         "Patent expires Sep 2026  -  only 5 months away. Contributes 8.2% of revenue. Accelerate DiabeGuard Insulin hospital penetration (target +40% vol in 6 months), pre-negotiate 2-year government tender lock-ins, and launch a doctor loyalty programme before generics enter."),
        ("#F59E0B","rgba(245,158,11,0.06)","📈","GROWTH LEVER",
         "Expand Oncology  -  Highest Margin Segment",
         "OncoClear carries 65%+ GP margin with a patent runway to 2031. Add 3 dedicated Oncology KAMs targeting cancer centres in South and West India. Increase hospital allocation by 20%. Explore combination therapy protocols with KOL partnerships."),
        ("#10B981","rgba(16,185,129,0.06)","🗺️","MARKET EXPANSION",
         "Unlock Tier B and C Region Revenue",
         "East India and Northeast cover 35% of India's population but generate only 20% of revenue. Deploy 6 new reps in Tier B focused on Diabetes and Cardiovascular. Use distributor partnerships for Tier C  -  delivers 3x ROI vs direct Tier A headcount."),
    ]
    for bc,bg,icon,badge,title,body in recs:
        st.markdown(f"""
        <div style="background:{bg};border:1px solid rgba(255,255,255,0.04);
            border-left:4px solid {bc};border-radius:14px;
            padding:20px 24px;margin-bottom:14px">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                <span style="font-size:22px">{icon}</span>
                <span style="background:rgba(255,255,255,0.05);color:{bc};
                    border:1px solid {bc}40;padding:3px 12px;border-radius:20px;
                    font-size:10px;font-weight:800;letter-spacing:1px">{badge}</span>
                <span style="font-size:15px;font-weight:700;color:#F1F5F9">{title}</span>
            </div>
            <div style="font-size:13px;color:#64748B;line-height:1.8;padding-left:32px">{body}</div>
        </div>""", unsafe_allow_html=True)

    shdr("⬇️","Export Data")
    d1, d2 = st.columns(2, gap="medium")
    d1.download_button("⬇️  Download Filtered Sales Data",
                       df.to_csv(index=False),
                       "zenithpharma_filtered_sales.csv","text/csv",
                       use_container_width=True)
    d2.download_button("⬇️  Download Drug Summary",
                       drug_sum.to_csv(index=False),
                       "zenithpharma_drug_summary.csv","text/csv",
                       use_container_width=True)
