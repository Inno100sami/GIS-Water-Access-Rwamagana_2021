"""
visualize.py
============
Generates index.html — an interactive dashboard for the MSc thesis:

    "Application of GIS for Mapping and Measuring Citizen's Access to
     Water Supply in Rwamagana District"

    Author : NDAGIJIMANA Innocent
    Year   : 2022
    Univ.  : University of Lay Adventists of Kigali (UNILAK)

Run:
    pip install plotly pandas
    python visualize.py
    --> produces index.html (open in browser or serve via GitHub Pages)
"""

import json
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

with open(os.path.join(DATA_DIR, "sector_coverage.json")) as f:
    sectors_raw = json.load(f)

with open(os.path.join(DATA_DIR, "water_tariffs.json")) as f:
    tariffs_raw = json.load(f)

with open(os.path.join(DATA_DIR, "key_indicators.json")) as f:
    indicators = json.load(f)

sectors_df = pd.DataFrame(sectors_raw)
sectors_df = sectors_df.sort_values("coverage_pct")
sectors_df["unserved_population"] = (
    sectors_df["total_population"] - sectors_df["served_population"]
)

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
TEAL      = "#0d9488"
TEAL_DARK = "#0f766e"
AMBER     = "#f59e0b"
RED       = "#ef4444"
BLUE      = "#3b82f6"
GRAY      = "#e5e7eb"
BG        = "#f8fafc"
TEXT      = "#1e293b"


def coverage_color(pct):
    """Return a hex colour based on coverage percentage."""
    if pct >= 75:
        return "#22c55e"   # green
    elif pct >= 50:
        return TEAL        # teal
    elif pct >= 40:
        return AMBER       # amber
    else:
        return RED         # red


# ---------------------------------------------------------------------------
# Figure 1 – Coverage per sector (horizontal bar)
# ---------------------------------------------------------------------------
bar_colors = [coverage_color(p) for p in sectors_df["coverage_pct"]]

fig_coverage = go.Figure()
fig_coverage.add_trace(go.Bar(
    y=sectors_df["sector"],
    x=sectors_df["coverage_pct"],
    orientation="h",
    marker_color=bar_colors,
    text=[f"{p}%" for p in sectors_df["coverage_pct"]],
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Coverage: %{x}%<br>"
        "Served: %{customdata[0]:,} people<br>"
        "Total: %{customdata[1]:,} people<extra></extra>"
    ),
    customdata=sectors_df[["served_population", "total_population"]].values,
))
fig_coverage.add_vline(
    x=100, line_dash="dot", line_color="#94a3b8",
    annotation_text="100% target", annotation_position="top right"
)
fig_coverage.update_layout(
    title=dict(text="Water Service Coverage by Sector (%)", font_size=16),
    xaxis=dict(title="Coverage (%)", range=[0, 115]),
    yaxis=dict(title=""),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=500,
    margin=dict(l=20, r=40, t=50, b=40),
)

# ---------------------------------------------------------------------------
# Figure 2 – Served vs Unserved population (stacked bar)
# ---------------------------------------------------------------------------
fig_population = go.Figure()
fig_population.add_trace(go.Bar(
    name="Served Population",
    y=sectors_df["sector"],
    x=sectors_df["served_population"],
    orientation="h",
    marker_color=TEAL,
    hovertemplate="%{y}: %{x:,} served<extra></extra>",
))
fig_population.add_trace(go.Bar(
    name="Unserved Population",
    y=sectors_df["sector"],
    x=sectors_df["unserved_population"],
    orientation="h",
    marker_color=RED,
    opacity=0.7,
    hovertemplate="%{y}: %{x:,} unserved<extra></extra>",
))
fig_population.update_layout(
    barmode="stack",
    title=dict(text="Served vs Unserved Population per Sector", font_size=16),
    xaxis=dict(title="Population"),
    yaxis=dict(title=""),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=500,
    margin=dict(l=20, r=20, t=50, b=40),
    legend=dict(orientation="h", y=-0.15),
)

# ---------------------------------------------------------------------------
# Figure 3 – Public water points per sector
# ---------------------------------------------------------------------------
pwp_df = sectors_df.sort_values("public_water_points")
fig_pwp = go.Figure(go.Bar(
    y=pwp_df["sector"],
    x=pwp_df["public_water_points"],
    orientation="h",
    marker_color=BLUE,
    text=pwp_df["public_water_points"],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Public Water Points: %{x}<extra></extra>",
))
fig_pwp.update_layout(
    title=dict(text="Number of Public Water Points per Sector", font_size=16),
    xaxis=dict(title="Number of Public Water Points", range=[0, 95]),
    yaxis=dict(title=""),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=500,
    margin=dict(l=20, r=40, t=50, b=40),
)

# ---------------------------------------------------------------------------
# Figure 4 – HH connections vs PWPs scatter
# ---------------------------------------------------------------------------
fig_scatter = go.Figure(go.Scatter(
    x=sectors_df["hh_connections"],
    y=sectors_df["coverage_pct"],
    mode="markers+text",
    text=sectors_df["sector"],
    textposition="top center",
    marker=dict(
        color=sectors_df["coverage_pct"],
        colorscale="RdYlGn",
        size=sectors_df["public_water_points"] / 2 + 8,
        showscale=True,
        colorbar=dict(title="Coverage %"),
        cmin=0, cmax=100,
    ),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "HH Connections: %{x:,}<br>"
        "Coverage: %{y}%<br>"
        "<extra></extra>"
    ),
))
fig_scatter.update_layout(
    title=dict(
        text="Household Connections vs Coverage (bubble size = no. of public water points)",
        font_size=14
    ),
    xaxis=dict(title="Household Connections"),
    yaxis=dict(title="Coverage (%)"),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=480,
    margin=dict(l=20, r=20, t=60, b=40),
)

# ---------------------------------------------------------------------------
# Figure 5 – WASAC water tariffs
# ---------------------------------------------------------------------------
wasac = tariffs_raw["wasac_tariffs"]["categories"]
wasac_df = pd.DataFrame(wasac)
wasac_df["label"] = wasac_df["customer"] + " — " + wasac_df["block"]

fig_wasac = go.Figure(go.Bar(
    x=wasac_df["label"],
    y=wasac_df["tariff_rwf_m3"],
    marker_color=TEAL,
    text=wasac_df["tariff_rwf_m3"],
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Tariff: %{y} RWF/m³<extra></extra>",
))
fig_wasac.update_layout(
    title=dict(text="WASAC Water Tariffs (RWF/m³, VAT exclusive)", font_size=16),
    xaxis=dict(title="", tickangle=-30),
    yaxis=dict(title="RWF per m³", range=[0, 1050]),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=430,
    margin=dict(l=20, r=20, t=50, b=120),
)

# ---------------------------------------------------------------------------
# Figure 6 – Rural water tariffs by system type
# ---------------------------------------------------------------------------
rural = tariffs_raw["rural_tariffs"]["systems"]
rural_df = pd.DataFrame(rural)

fig_rural = go.Figure()
fig_rural.add_trace(go.Bar(
    name="Excl. VAT (RWF/m³)",
    x=rural_df["system"],
    y=rural_df["tariff_excl_vat_m3"],
    marker_color=TEAL,
    text=rural_df["tariff_excl_vat_m3"],
    textposition="outside",
))
fig_rural.add_trace(go.Bar(
    name="Incl. VAT (RWF/m³)",
    x=rural_df["system"],
    y=rural_df["tariff_incl_vat_m3"],
    marker_color=AMBER,
    text=rural_df["tariff_incl_vat_m3"],
    textposition="outside",
))
fig_rural.update_layout(
    barmode="group",
    title=dict(text="Rural Water Tariffs by System Type (RWF/m³)", font_size=16),
    xaxis=dict(title=""),
    yaxis=dict(title="RWF per m³", range=[0, 1250]),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=400,
    margin=dict(l=20, r=20, t=50, b=40),
    legend=dict(orientation="h", y=-0.2),
)

# ---------------------------------------------------------------------------
# Figure 7 – Water quantity (gauge)
# ---------------------------------------------------------------------------
qty = indicators["water_quantity"]
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=qty["mean_consumption_lpcd"],
    delta=dict(
        reference=qty["national_target_lpcd"],
        increasing=dict(color="#22c55e"),
        decreasing=dict(color=RED),
    ),
    gauge=dict(
        axis=dict(range=[0, 90]),
        bar=dict(color=TEAL),
        steps=[
            dict(range=[0, qty["national_target_lpcd"]], color="#fecaca"),
            dict(range=[qty["national_target_lpcd"], qty["mean_consumption_lpcd"]], color="#bbf7d0"),
            dict(range=[qty["mean_consumption_lpcd"], 90], color=GRAY),
        ],
        threshold=dict(
            line=dict(color=RED, width=3),
            thickness=0.8,
            value=qty["national_target_lpcd"],
        ),
    ),
    title=dict(text="Mean Water Consumption (litres/capita/day)<br><span style='font-size:12px'>Red line = national minimum target (20 L/capita/day)</span>"),
    number=dict(suffix=" L/c/d"),
))
fig_gauge.update_layout(
    paper_bgcolor="white",
    height=320,
    margin=dict(l=30, r=30, t=40, b=20),
)

# ---------------------------------------------------------------------------
# Figure 8 – Quantity satisfaction (pie)
# ---------------------------------------------------------------------------
fig_satisfaction = go.Figure(go.Pie(
    labels=["Satisfied (47.5%)", "Not Satisfied (37.5%)", "Neutral (15%)"],
    values=[47.5, 37.5, 15],
    hole=0.45,
    marker_colors=["#22c55e", RED, AMBER],
    textinfo="label+percent",
    hovertemplate="%{label}<extra></extra>",
))
fig_satisfaction.update_layout(
    title=dict(text="Household Satisfaction with Water Quantity", font_size=16),
    paper_bgcolor="white",
    height=340,
    margin=dict(l=20, r=20, t=50, b=20),
    showlegend=False,
)

# ---------------------------------------------------------------------------
# Figure 9 – Reliability (pie)
# ---------------------------------------------------------------------------
rel = indicators["water_reliability"]
fig_reliability = go.Figure(go.Pie(
    labels=[
        "Supply 1–2 days/week (unreliable)",
        "24-hour supply (boreholes/springs)",
        "Unimproved sources",
    ],
    values=[
        rel["sources_unreliable_pct"],
        rel["sources_24hr_supply_pct"],
        rel["sources_unimproved_pct"],
    ],
    hole=0.45,
    marker_colors=[RED, "#22c55e", AMBER],
    textinfo="label+percent",
    hovertemplate="%{label}: %{value}%<extra></extra>",
))
fig_reliability.update_layout(
    title=dict(text="Water Supply Reliability (% of Main Sources)", font_size=16),
    paper_bgcolor="white",
    height=360,
    margin=dict(l=20, r=20, t=50, b=20),
    showlegend=False,
)

# ---------------------------------------------------------------------------
# Figure 10 – Households meeting national water target
# ---------------------------------------------------------------------------
fig_target = go.Figure(go.Bar(
    x=["Meet/exceed target (≥20 L/c/d)", "Below target (<20 L/c/d)"],
    y=[qty["households_meeting_target_pct"], qty["households_below_target_pct"]],
    marker_color=["#22c55e", RED],
    text=[f"{qty['households_meeting_target_pct']}%", f"{qty['households_below_target_pct']}%"],
    textposition="outside",
    hovertemplate="%{x}: %{y}%<extra></extra>",
))
fig_target.update_layout(
    title=dict(text="Households vs National Water Target (20 L/capita/day)", font_size=16),
    yaxis=dict(title="%", range=[0, 80]),
    xaxis=dict(title=""),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=340,
    margin=dict(l=20, r=20, t=50, b=40),
)

# ---------------------------------------------------------------------------
# Figure 11 – Network length vs coverage scatter
# ---------------------------------------------------------------------------
# Remove the outlier (Muyumbu = 1231 km) for scale clarity — shown in tooltip
fig_network = go.Figure(go.Scatter(
    x=sectors_df["network_length_km"],
    y=sectors_df["coverage_pct"],
    mode="markers+text",
    text=sectors_df["sector"],
    textposition="top center",
    marker=dict(
        color=sectors_df["coverage_pct"],
        colorscale="RdYlGn",
        size=12,
        showscale=True,
        colorbar=dict(title="Coverage %"),
        cmin=0, cmax=100,
    ),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "Network: %{x} km<br>"
        "Coverage: %{y}%<extra></extra>"
    ),
))
fig_network.update_layout(
    title=dict(text="Network Length (km) vs Service Coverage per Sector", font_size=14),
    xaxis=dict(title="Network Length (km)"),
    yaxis=dict(title="Coverage (%)"),
    plot_bgcolor=BG,
    paper_bgcolor="white",
    height=440,
    margin=dict(l=20, r=20, t=60, b=40),
)

# ---------------------------------------------------------------------------
# Inline KPI numbers
# ---------------------------------------------------------------------------
total_pop    = sectors_df["total_population"].sum()
total_served = sectors_df["served_population"].sum()
avg_coverage = round(total_served / total_pop * 100, 1)
total_pwp    = sectors_df["public_water_points"].sum()
total_hh     = sectors_df["hh_connections"].sum()


def to_html_fig(fig, div_id):
    """Return fig as an HTML div (no full page, no Plotly.js)."""
    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        div_id=div_id,
        config={"responsive": True, "displayModeBar": True},
    )


# ---------------------------------------------------------------------------
# Assemble full HTML page
# ---------------------------------------------------------------------------
html_parts = [
    f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>GIS Water Access — Rwamagana District | MSc Thesis Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #f1f5f9;
      color: {TEXT};
    }}
    /* ---- Header ---- */
    .hero {{
      background: linear-gradient(135deg, {TEAL_DARK} 0%, #1e40af 100%);
      color: white;
      padding: 3rem 2rem 2.5rem;
      text-align: center;
    }}
    .hero h1 {{ font-size: 1.8rem; font-weight: 700; max-width: 800px; margin: 0 auto 0.5rem; line-height: 1.3; }}
    .hero p  {{ opacity: 0.85; font-size: 0.95rem; max-width: 700px; margin: 0 auto; }}
    .hero .meta {{ margin-top: 1rem; font-size: 0.85rem; opacity: 0.7; }}

    /* ---- KPI strip ---- */
    .kpis {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      padding: 1.5rem 2rem;
      background: white;
      box-shadow: 0 1px 4px rgba(0,0,0,.08);
      justify-content: center;
    }}
    .kpi {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 1rem 1.5rem;
      text-align: center;
      min-width: 160px;
    }}
    .kpi .val {{ font-size: 1.9rem; font-weight: 700; color: {TEAL_DARK}; }}
    .kpi .lbl {{ font-size: 0.78rem; color: #64748b; margin-top: 4px; }}

    /* ---- Sections ---- */
    .section {{
      max-width: 1280px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }}
    .section-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: {TEAL_DARK};
      border-left: 4px solid {TEAL};
      padding-left: 0.75rem;
      margin-bottom: 1.2rem;
    }}
    .chart-card {{
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 1px 6px rgba(0,0,0,.07);
      margin-bottom: 1.5rem;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 1.5rem;
      margin-bottom: 1.5rem;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
      margin-bottom: 1.5rem;
    }}

    /* ---- Findings callout ---- */
    .callout {{
      background: #ecfdf5;
      border: 1px solid #6ee7b7;
      border-radius: 10px;
      padding: 1.2rem 1.5rem;
      margin-bottom: 1.5rem;
      font-size: 0.93rem;
      line-height: 1.6;
    }}
    .callout strong {{ color: {TEAL_DARK}; }}
    .callout.warn {{
      background: #fffbeb;
      border-color: #fcd34d;
    }}
    .callout.red {{
      background: #fff1f2;
      border-color: #fca5a5;
    }}

    /* ---- Footer ---- */
    footer {{
      text-align: center;
      padding: 2rem;
      font-size: 0.82rem;
      color: #94a3b8;
      border-top: 1px solid #e2e8f0;
      margin-top: 3rem;
    }}
    @media (max-width: 600px) {{
      .hero h1 {{ font-size: 1.3rem; }}
      .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<!-- ===== HERO ===== -->
<div class="hero">
  <h1>Application of GIS for Mapping and Measuring Citizen's Access to Water Supply in Rwamagana District</h1>
  <p>Interactive Research Dashboard — MSc Thesis in Environmental Information System</p>
  <div class="meta">
    NDAGIJIMANA Innocent &nbsp;|&nbsp; UNILAK &nbsp;|&nbsp; May 2022 &nbsp;|&nbsp;
    Supervisor: Dr. François Xavier Nshimiyimana
  </div>
</div>

<!-- ===== KPI STRIP ===== -->
<div class="kpis">
  <div class="kpi"><div class="val">14</div><div class="lbl">Sectors Studied</div></div>
  <div class="kpi"><div class="val">{total_pop:,}</div><div class="lbl">Total District Population</div></div>
  <div class="kpi"><div class="val">{total_served:,}</div><div class="lbl">Population with Water Access</div></div>
  <div class="kpi"><div class="val">{avg_coverage}%</div><div class="lbl">Average District Coverage</div></div>
  <div class="kpi"><div class="val">{total_pwp}</div><div class="lbl">Total Public Water Points</div></div>
  <div class="kpi"><div class="val">{total_hh:,}</div><div class="lbl">Household Connections</div></div>
  <div class="kpi"><div class="val">29 L</div><div class="lbl">Mean Consumption/Capita/Day</div></div>
  <div class="kpi"><div class="val">88%</div><div class="lbl">Sources: Unreliable Supply</div></div>
</div>

<!-- ===== SECTION 1: COVERAGE ===== -->
<div class="section">
  <div class="section-title">1. Water Service Coverage by Sector</div>

  <div class="callout">
    <strong>Key Finding:</strong> Water service coverage across Rwamagana district ranges from
    <strong>29% (Muyumbu)</strong> to <strong>100% (Kigabiro & Munyaga)</strong>.
    Six sectors remain critically underserved with coverage below 50%:
    Muyumbu (29%), Nyakaliro (37%), Nzige (38%), Karenge (41%), Muhazi (44%) and Gahengeri (47%).
  </div>

  <div class="chart-card">
    {to_html_fig(fig_coverage, "fig_coverage")}
  </div>

  <div class="chart-card">
    {to_html_fig(fig_population, "fig_population")}
  </div>
</div>

<!-- ===== SECTION 2: WATER POINTS ===== -->
<div class="section">
  <div class="section-title">2. Public Water Infrastructure</div>

  <div class="callout">
    <strong>Key Finding:</strong> Munyaga sector has the highest density of public water points (80),
    contributing to its 100% coverage. Muyumbu and Nzige each have only 12 water points despite
    large populations — a critical gap requiring urgent investment.
  </div>

  <div class="grid-2">
    <div class="chart-card">
      {to_html_fig(fig_pwp, "fig_pwp")}
    </div>
    <div class="chart-card">
      {to_html_fig(fig_scatter, "fig_scatter")}
    </div>
  </div>

  <div class="chart-card">
    {to_html_fig(fig_network, "fig_network")}
  </div>
</div>

<!-- ===== SECTION 3: RELIABILITY & QUANTITY ===== -->
<div class="section">
  <div class="section-title">3. Water Reliability &amp; Quantity</div>

  <div class="callout warn">
    <strong>Reliability:</strong> 88% of improved water sources supply water for only
    <strong>1–2 days per week</strong> — far below the national target of 24 hours daily.
    Only 5% of households (those using boreholes and springs) enjoy a 24-hour supply.
  </div>

  <div class="callout">
    <strong>Quantity:</strong> The mean water consumption of <strong>29 litres/capita/day</strong>
    exceeds the national minimum of 20 L/c/d. However, <strong>40% of households</strong>
    remain below this benchmark due to affordability constraints, unreliable supply, and
    access inconveniences.
  </div>

  <div class="grid-2">
    <div class="chart-card">
      {to_html_fig(fig_gauge, "fig_gauge")}
    </div>
    <div class="chart-card">
      {to_html_fig(fig_target, "fig_target")}
    </div>
  </div>

  <div class="grid-2">
    <div class="chart-card">
      {to_html_fig(fig_reliability, "fig_reliability")}
    </div>
    <div class="chart-card">
      {to_html_fig(fig_satisfaction, "fig_satisfaction")}
    </div>
  </div>
</div>

<!-- ===== SECTION 4: AFFORDABILITY ===== -->
<div class="section">
  <div class="section-title">4. Water Affordability</div>

  <div class="callout warn">
    <strong>Affordability:</strong> 75% of surveyed households paid for water services.
    Diesel-pumped rural water costs <strong>1,087 RWF/m³</strong> (incl. VAT) —
    more than <strong>3× the gravity tariff</strong> (338 RWF/m³), creating
    significant inequity between well-served and remote areas.
  </div>

  <div class="grid-2">
    <div class="chart-card">
      {to_html_fig(fig_wasac, "fig_wasac")}
    </div>
    <div class="chart-card">
      {to_html_fig(fig_rural, "fig_rural")}
    </div>
  </div>
</div>

<!-- ===== SECTION 5: CONCLUSIONS ===== -->
<div class="section">
  <div class="section-title">5. Key Conclusions &amp; Recommendations</div>

  <div class="callout">
    <strong>Coverage &amp; Access:</strong> 29.1% of households access public standpipes within
    500 m / 30 min (optimal access), while 27.3% must travel beyond this threshold.
    Physical proximity alone does not guarantee adequate water use — affordability and
    reliability are equally critical determinants.
  </div>

  <div class="callout red">
    <strong>Prioritise underserved sectors:</strong> Muyumbu, Nyakaliro, Nzige, Karenge,
    Muhazi and Gahengeri require immediate expansion of water infrastructure and rehabilitation
    of aging networks to achieve national coverage targets under NST1 2017–2024.
  </div>

  <div class="callout warn">
    <strong>Reliability gap:</strong> RURA must enforce the 24-hour supply mandate and
    MININFRA should prioritise network rehabilitation, especially in WASAC-managed systems
    where intermittent supply affects the majority of connected households.
  </div>

  <div class="callout">
    <strong>Equity in pricing:</strong> The tariff differential between gravity systems and
    diesel-pumped networks disadvantages remote rural communities the most.
    Progressive tariff reform and targeted subsidies are recommended.
  </div>
</div>

<!-- ===== FOOTER ===== -->
<footer>
  <p>MSc Thesis &mdash; NDAGIJIMANA Innocent &mdash; University of Lay Adventists of Kigali (UNILAK) &mdash; May 2022</p>
  <p style="margin-top:6px;">
    Data sources: MININFRA WASH MIS (2021), RURA (2021), Rwamagana District (2021), Household Survey (n=150).
    &nbsp;|&nbsp;
    <a href="https://github.com" style="color:{TEAL};">View on GitHub</a>
  </p>
</footer>

</body>
</html>
""",
]

output_path = os.path.join(BASE_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print(f"Dashboard written to: {output_path}")
print(f"  Total population:  {total_pop:,}")
print(f"  Total served:      {total_served:,}")
print(f"  Average coverage:  {avg_coverage}%")
print(f"  Total water points:{total_pwp}")
