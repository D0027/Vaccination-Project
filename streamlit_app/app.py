import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import run_query, db_is_reachable

st.set_page_config(
    page_title="Vaccination Intelligence Platform",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================== THEME (dark)
BG = "#0E1420"
SURFACE = "#161D2E"
SURFACE2 = "#1C2438"
BORDER = "#293450"
NAVY = "#8FA6D6"          # headings on dark bg
GREEN = "#2BD9A0"
AMBER = "#F0B255"
RED = "#F0716F"
INK = "#E7ECF3"           # body text
MUTE = "#8A93AC"
PALETTE = ["#2BD9A0", "#6C8FE0", "#F0B255", "#B48CE0", "#F0716F", "#4FC3D9"]

st.markdown(f"""
<style>
    #MainMenu, footer {{visibility: hidden;}}

    /* ---- FIX: hide the built-in Streamlit header toolbar so page titles
       never render underneath it (this was the "heading cut off" bug) ---- */
    header[data-testid="stHeader"] {{
        background: transparent;
        height: 0rem;
        visibility: hidden;
    }}
    div[data-testid="stToolbar"] {{ visibility: hidden; height: 0; }}
    div[data-testid="stDecoration"] {{ visibility: hidden; height: 0; }}

    .main {{ background-color: {BG}; }}
    .stApp {{ background-color: {BG}; }}
    .block-container {{ padding-top: 2.2rem !important; }}
    body, p, span, div, label {{ color: {INK}; }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0B111C 0%, #121A2C 100%);
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] * {{ color: #EDF1F9 !important; }}
    section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.12); }}
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
        background-color: {GREEN} !important; color: #06231A !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: {SURFACE2} !important; border-color: {BORDER} !important;
    }}

    .hero {{
        background: linear-gradient(120deg, #0F1830 0%, #16233F 55%, #1C2C52 100%);
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 22px;
        color: #EDF1F9;
    }}
    .hero h1 {{ margin: 0; font-size: 30px; font-weight: 800; color: #FFFFFF; line-height: 1.3; }}
    .hero p {{ margin: 6px 0 0 0; opacity: 0.8; font-size: 14.5px; }}
    .hero .tag {{
        display:inline-block; background: rgba(43,217,160,0.15); color: {GREEN};
        border: 1px solid rgba(43,217,160,0.4); border-radius: 20px;
        padding: 3px 12px; font-size: 12px; font-weight: 600; letter-spacing: .04em;
        margin-bottom: 10px;
    }}

    .kpi-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-left: 4px solid {GREEN};
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }}
    .kpi-value {{ font-size: 26px; font-weight: 800; color: #FFFFFF; line-height: 1.15; }}
    .kpi-label {{ font-size: 12.5px; color: {MUTE}; margin-top: 3px; font-weight: 500; }}

    .section-title {{ color: #FFFFFF; font-weight: 800; font-size: 21px; margin: 10px 0 2px 0; line-height: 1.4; }}
    .section-sub {{ color: {MUTE}; font-size: 13.5px; margin-bottom: 14px; }}

    div[data-testid="stMetric"] {{
        background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 10px 14px;
    }}
    div[data-testid="stMetricValue"] {{ color: #FFFFFF; }}
    div[data-testid="stMetricLabel"] {{ color: {MUTE}; }}

    .stTabs [data-baseweb="tab"] {{ font-weight: 600; color: {MUTE}; }}
    .stTabs [aria-selected="true"] {{ color: {GREEN} !important; }}

    .stDataFrame, [data-testid="stDataFrame"] {{ background-color: {SURFACE}; }}

    .badge-live {{
        background:rgba(43,217,160,0.15); color:{GREEN}; padding:3px 10px; border-radius:20px;
        font-size:12px; font-weight:700; border:1px solid rgba(43,217,160,0.35);
    }}
    .badge-demo {{ background:rgba(240,178,85,0.15); color:{AMBER}; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid rgba(240,178,85,0.35); }}

    /* ---- pulsing live dot used on Risk & Gaps ---- */
    .pulse-dot {{
        display:inline-block; width:9px; height:9px; border-radius:50%;
        background:{GREEN}; margin-right:6px; box-shadow: 0 0 0 rgba(43,217,160,0.6);
        animation: pulse 1.6s infinite;
    }}
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(43,217,160,0.55); }}
        70% {{ box-shadow: 0 0 0 9px rgba(43,217,160,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(43,217,160,0); }}
    }}
    .live-strip {{
        display:flex; align-items:center; gap:8px; background:{SURFACE}; border:1px solid {BORDER};
        border-radius: 10px; padding: 7px 14px; font-size: 12.5px; color:{MUTE}; width: fit-content; margin-bottom: 14px;
    }}

    .progress-track {{
        background: {SURFACE2}; border-radius: 20px; height: 12px; width: 100%; overflow: hidden; border: 1px solid {BORDER};
    }}
    .progress-fill {{
        height: 100%; border-radius: 20px;
        background: linear-gradient(90deg, {AMBER}, {GREEN});
    }}
</style>
""", unsafe_allow_html=True)

PLOT_TEMPLATE = dict(
    font=dict(family="Segoe UI, Arial", color=INK, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=SURFACE,
    margin=dict(l=10, r=10, t=48, b=10),
    title_font=dict(size=15, color="#FFFFFF"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)


def style(fig, height=420):
    fig.update_layout(height=height, **PLOT_TEMPLATE)
    return fig


def kpi_card(col, value, label):
    col.markdown(f"""<div class="kpi-card"><div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div></div>""", unsafe_allow_html=True)


def section(title, sub=""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="section-sub">{sub}</div>', unsafe_allow_html=True)


# ============================================================== DATA LAYER
LIVE = db_is_reachable()


@st.cache_data(ttl=3600)
def load_regions():
    if LIVE:
        df = run_query("SELECT DISTINCT who_region FROM countries WHERE who_region IS NOT NULL ORDER BY who_region")
        return df["who_region"].tolist()
    return ["AFRO", "AMRO", "EMRO", "EURO", "SEARO", "WPRO"]


def demo_map():
    rng = np.random.default_rng(7)
    rows = [
        ("IND", "India", "SEARO"), ("NGA", "Nigeria", "AFRO"), ("BRA", "Brazil", "AMRO"),
        ("DEU", "Germany", "EURO"), ("JPN", "Japan", "WPRO"), ("KEN", "Kenya", "AFRO"),
        ("MEX", "Mexico", "AMRO"), ("FRA", "France", "EURO"), ("EGY", "Egypt", "EMRO"),
        ("VNM", "Vietnam", "WPRO"), ("AGO", "Angola", "AFRO"), ("NER", "Niger", "AFRO"),
        ("ESP", "Spain", "EURO"), ("CHL", "Chile", "AMRO"), ("POL", "Poland", "EURO"),
        ("USA", "United States of America", "AMRO"), ("CHN", "China", "WPRO"),
        ("ZAF", "South Africa", "AFRO"), ("AUS", "Australia", "WPRO"), ("PAK", "Pakistan", "EMRO"),
    ]
    return pd.DataFrame({
        "code": [r[0] for r in rows], "name": [r[1] for r in rows], "who_region": [r[2] for r in rows],
        "avg_coverage": rng.uniform(45, 97, len(rows)).round(1),
    })


def demo_scatter():
    df = demo_map().copy()
    rng = np.random.default_rng(21)
    df["avg_coverage_pct"] = df["avg_coverage"]
    df["avg_incidence_rate"] = rng.uniform(0, 400, len(df)).round(1)
    return df


def demo_cases():
    rng = np.random.default_rng(5)
    years = list(range(1980, 2026, 2))
    diseases = ["MEASLES", "PERTUSSIS", "NTETANUS", "DIPHTHERIA"]
    return pd.DataFrame([
        {"year": y, "disease": d, "avg_cases": max(0, rng.normal(8000 - i * 1500, 1500) * np.exp(-(y - 1980) / 25))}
        for y in years for i, d in enumerate(diseases)
    ])


@st.cache_data(ttl=3600)
def load_country_list():
    if LIVE:
        return run_query("SELECT DISTINCT name FROM vw_coverage_summary ORDER BY name")["name"].tolist()
    return sorted(demo_map()["name"].unique())


@st.cache_data(ttl=3600)
def load_kpi():
    if LIVE:
        return run_query("SELECT * FROM vw_kpi_summary").iloc[0]
    return None


@st.cache_data(ttl=3600)
def load_map(regions):
    if LIVE:
        rf = "" if not regions else f"WHERE who_region IN ({','.join([repr(r) for r in regions])})"
        return run_query(f"""
            SELECT code, name, who_region, AVG(coverage) AS avg_coverage
            FROM vw_coverage_summary
            {rf}
            GROUP BY code, name, who_region
        """)
    df = demo_map()
    return df[df["who_region"].isin(regions)] if regions else df


@st.cache_data(ttl=3600)
def load_scatter(regions):
    if LIVE:
        rf = "" if not regions else f"WHERE who_region IN ({','.join([repr(r) for r in regions])})"
        return run_query(f"""
            SELECT name, who_region,
                   AVG(avg_coverage_pct) AS avg_coverage_pct,
                   AVG(avg_incidence_rate) AS avg_incidence_rate
            FROM vw_coverage_vs_incidence
            {rf}
            GROUP BY name, who_region
        """)
    df = demo_scatter()
    return df[df["who_region"].isin(regions)] if regions else df


@st.cache_data(ttl=3600)
def load_country_antigen(country):
    safe = country.replace("'", "''")
    if LIVE:
        return run_query(f"""
            SELECT antigen, antigen_description, AVG(coverage) AS avg_coverage
            FROM vw_coverage_summary WHERE name = '{safe}'
            GROUP BY antigen, antigen_description ORDER BY avg_coverage DESC LIMIT 15
        """)
    rng = np.random.default_rng(abs(hash(country)) % 1000)
    return pd.DataFrame({
        "antigen": ["BCG", "DTPCV1", "MCV1", "POL3", "HEPB3", "PCV1"],
        "antigen_description": ["BCG", "DTP dose 1", "Measles dose 1", "Polio dose 3", "Hep B dose 3", "PCV dose 1"],
        "avg_coverage": rng.uniform(70, 98, 6).round(1),
    }).sort_values("avg_coverage", ascending=False)


@st.cache_data(ttl=3600)
def load_country_trend(country):
    safe = country.replace("'", "''")
    if LIVE:
        return run_query(f"""
            SELECT year, AVG(coverage) AS avg_coverage
            FROM vw_coverage_summary WHERE name = '{safe}'
            GROUP BY year ORDER BY year
        """)
    rng = np.random.default_rng(abs(hash(country)) % 999)
    years = list(range(1990, 2026, 2))
    return pd.DataFrame({"year": years,
                          "avg_coverage": np.clip(70 + np.cumsum(rng.normal(0.5, 3, len(years))), 55, 95).round(1)})


@st.cache_data(ttl=3600)
def load_risk(regions):
    if LIVE:
        rf = "" if not regions else f"WHERE who_region IN ({','.join([repr(r) for r in regions])})"
        return run_query(f"""
            SELECT country_name, vaccine_description, who_region, schedule_rounds, target_pop_description, geoarea
            FROM vw_high_risk_schedule {rf} LIMIT 1000
        """)
    rng = np.random.default_rng(3)
    df = pd.DataFrame({
        "country_name": rng.choice(["Andorra", "Anguilla", "Argentina", "Armenia", "Austria"], 40),
        "vaccine_description": rng.choice(["Adult seasonal influenza vaccine", "HPV-9 vaccine", "MMR vaccine", "Pediatric Hepatitis B"], 40),
        "who_region": rng.choice(["EURO", "AMRO", "WPRO", "EMRO"], 40),
        "schedule_rounds": 1.0,
        "target_pop_description": rng.choice(["Adults", "Catch-up children"], 40),
        "geoarea": "NATIONAL",
    })
    return df[df["who_region"].isin(regions)] if regions else df


@st.cache_data(ttl=3600)
def load_cases_trend():
    if LIVE:
        return run_query("""SELECT year, disease, AVG(cases) AS avg_cases
                             FROM vw_cases_summary GROUP BY year, disease ORDER BY year""")
    return demo_cases()


@st.cache_data(ttl=3600)
def load_region_incidence():
    if LIVE:
        return run_query("""SELECT who_region, AVG(incidence_rate) AS avg_incidence_rate
                             FROM vw_incidence_summary GROUP BY who_region""")
    return pd.DataFrame({"who_region": ["AFRO", "WPRO", "SEARO", "EMRO", "EURO", "AMRO"],
                          "avg_incidence_rate": [150, 126, 70, 66, 39, 32]})


@st.cache_data(ttl=3600)
def load_measles_target():
    if LIVE:
        return run_query("SELECT * FROM vw_measles_2030 ORDER BY year")
    rng = np.random.default_rng(11)
    years = list(range(1980, 2026, 2))
    cov = np.clip(60 + np.cumsum(rng.normal(1, 2, len(years))), 55, 92).round(1)
    return pd.DataFrame({"year": years, "measles_coverage_pct": cov, "gap_to_95pct_target": (95 - cov).round(2)})


@st.cache_data(ttl=3600)
def load_intro_timeline():
    if LIVE:
        return run_query("SELECT year, who_region, vaccines_introduced FROM vw_intro_timeline ORDER BY year")
    rng = np.random.default_rng(9)
    years = list(range(1980, 2026, 2))
    return pd.DataFrame([
        {"year": y, "who_region": r, "vaccines_introduced": max(0, int(rng.normal((y - 1980) * 2, 5)))}
        for y in years for r in ["AFRO", "AMRO", "EMRO", "EURO", "SEARO", "WPRO"]
    ])


@st.cache_data(ttl=3600)
def load_raw_table(table, limit=500):
    allowed = {"countries", "coverage_data", "incidence_rate", "reported_cases",
               "vaccine_introduction", "vaccine_schedule"}
    if table not in allowed:
        return pd.DataFrame()
    if LIVE:
        return run_query(f"SELECT * FROM {table} LIMIT {int(limit)}")
    return pd.DataFrame()


# ============================================================== SIDEBAR
st.sidebar.markdown("### 💉 Vaccination Intelligence")
st.sidebar.caption("Global Coverage · Incidence · Impact Analytics")
st.sidebar.markdown(
    '<span class="badge-live">● LIVE — vaccination_db</span>' if LIVE
    else '<span class="badge-demo">◐ DEMO DATA</span>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🏠  Overview",
    "📈  Coverage vs Incidence",
    "🔎  Country Explorer",
    "⚠️  Risk & Gaps",
    "🦠  Disease Trends",
    "🎯  2030 Measles Target",
    "🗂️  Raw Data Explorer",
], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")
all_regions = load_regions()
selected_regions = st.sidebar.multiselect("WHO Region", all_regions, default=[])
st.sidebar.caption("Leave empty to include all regions.")
st.sidebar.markdown("---")
st.sidebar.caption("Data: WHO Global Vaccination & Immunization Datasets · MySQL `vaccination_db`")

# ============================================================== PAGES

if page == "🏠  Overview":
    st.markdown(f"""
    <div class="hero">
        <div class="tag">GLOBAL PUBLIC HEALTH ANALYTICS</div>
        <h1>Global Vaccination Coverage Overview</h1>
        <p>Live snapshot across {len(all_regions)} WHO regions — coverage, targets, and reach at a glance.</p>
    </div>
    """, unsafe_allow_html=True)

    kpi = load_kpi()
    map_df = load_map(selected_regions)

    c1, c2, c3, c4, c5 = st.columns(5)
    if LIVE and kpi is not None:
        kpi_card(c1, f'{int(kpi["total_countries"])}', "Countries Tracked")
        kpi_card(c2, f'{kpi["global_avg_coverage"]:.2f}%', "Global Avg Coverage")
        kpi_card(c3, f'{int(kpi["total_antigens"])}', "Antigens Monitored")
        kpi_card(c4, f'{int(kpi["records_above_80pct"]):,}', "Records \u2265 80%")
        kpi_card(c5, f'{int(kpi["records_above_95pct"]):,}', "Records \u2265 95%")
    else:
        kpi_card(c1, f'{map_df["name"].nunique()}', "Countries Tracked")
        kpi_card(c2, f'{map_df["avg_coverage"].mean():.1f}%', "Global Avg Coverage")
        kpi_card(c3, "69", "Antigens Monitored")
        kpi_card(c4, f'{(map_df["avg_coverage"] >= 80).sum()}', "Countries \u2265 80%")
        kpi_card(c5, f'{(map_df["avg_coverage"] >= 95).sum()}', "Countries \u2265 95%")

    st.write("")
    section("Coverage by Country", "Hover any country to see its name and average coverage")
    fig = px.choropleth(
        map_df, locations="code", locationmode="ISO-3", color="avg_coverage",
        hover_name="name", hover_data={"code": False, "who_region": True, "avg_coverage": ":.1f"},
        color_continuous_scale=[RED, AMBER, GREEN], range_color=(40, 100),
        labels={"avg_coverage": "Avg Coverage %", "who_region": "Region"},
    )
    fig.update_geos(bgcolor="rgba(0,0,0,0)", showframe=False, showcountries=True, countrycolor="#E7ECF3")
    style(fig, 480)
    st.plotly_chart(fig, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        top10 = map_df.nlargest(10, "avg_coverage").sort_values("avg_coverage")
        fig_top = px.bar(top10, x="avg_coverage", y="name", orientation="h", color_discrete_sequence=[GREEN])
        fig_top.update_layout(title="Top 10 — Highest Coverage")
        style(fig_top, 380)
        st.plotly_chart(fig_top, width="stretch")
    with col2:
        bottom10 = map_df.nsmallest(10, "avg_coverage").sort_values("avg_coverage", ascending=False)
        fig_bot = px.bar(bottom10, x="avg_coverage", y="name", orientation="h", color_discrete_sequence=[RED])
        fig_bot.update_layout(title="Bottom 10 — Lowest Coverage")
        style(fig_bot, 380)
        st.plotly_chart(fig_bot, width="stretch")

elif page == "📈  Coverage vs Incidence":
    st.markdown(f"""
    <div class="hero">
        <div class="tag">PRIORITY INTERVENTION MAP</div>
        <h1>Coverage vs Incidence</h1>
        <p>Where coverage is low and disease incidence is high — priority zone for intervention.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_scatter(selected_regions)
    tab1, tab2 = st.tabs(["Scatter View", "Data Table"])
    with tab1:
        fig = px.scatter(
            df, x="avg_coverage_pct", y="avg_incidence_rate", color="who_region",
            hover_name="name", color_discrete_sequence=PALETTE, opacity=0.85,
        )
        fig.update_traces(marker=dict(size=11, line=dict(width=1, color="white")))
        fig.add_vline(x=df["avg_coverage_pct"].median(), line_dash="dot", line_color=MUTE)
        fig.add_hline(y=df["avg_incidence_rate"].median(), line_dash="dot", line_color=MUTE)
        fig.update_layout(legend_title="WHO Region", xaxis_title="Avg Coverage %", yaxis_title="Avg Incidence Rate")
        style(fig, 540)
        st.plotly_chart(fig, width="stretch")
        st.caption("Dotted lines mark the median split. Top-left quadrant = low coverage & high incidence — highest priority.")
    with tab2:
        st.dataframe(df.sort_values("avg_incidence_rate", ascending=False), width="stretch", height=460)
        st.download_button("⬇ Download as CSV", df.to_csv(index=False), "coverage_vs_incidence.csv", "text/csv")

elif page == "🔎  Country Explorer":
    section("Country Explorer", "Antigen-level coverage and year-over-year trend for any country")

    countries_list = load_country_list()
    country = st.selectbox("Search a country", countries_list)

    ant = load_country_antigen(country)
    yr = load_country_trend(country)

    m1, m2, m3 = st.columns(3)
    m1.metric("Antigens Tracked", len(ant))
    m2.metric("Avg Coverage (top antigens)", f'{ant["avg_coverage"].mean():.1f}%')
    m3.metric("Latest Year on Record", int(yr["year"].max()) if not yr.empty else "—")

    col1, col2 = st.columns([1, 1.2])
    with col1:
        fig1 = px.bar(ant, x="avg_coverage", y="antigen", orientation="h",
                       color="avg_coverage", color_continuous_scale=[RED, AMBER, GREEN],
                       hover_data=["antigen_description"])
        fig1.update_layout(title=f"Coverage by Antigen — {country}", yaxis={"categoryorder": "total ascending"},
                            coloraxis_showscale=False)
        style(fig1, 430)
        st.plotly_chart(fig1, width="stretch")
    with col2:
        fig2 = px.area(yr, x="year", y="avg_coverage", color_discrete_sequence=[GREEN])
        fig2.update_layout(title=f"Coverage Trend — {country}")
        style(fig2, 430)
        st.plotly_chart(fig2, width="stretch")

    with st.expander("View raw antigen data"):
        st.dataframe(ant, width="stretch")

elif page == "⚠️  Risk & Gaps":
    st.markdown(f"""
    <div class="hero">
        <div class="tag">⚠ RISK INTELLIGENCE</div>
        <h1>Risk & Gaps Radar</h1>
        <p>Vaccines scheduled with only a single dose round across {len(all_regions)} WHO regions — potential reinforcement candidates.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""<div class="live-strip"><span class="pulse-dot"></span>
        {"LIVE feed — vaccination_db" if LIVE else "DEMO mode — connect MySQL for live risk data"}</div>""",
        unsafe_allow_html=True,
    )

    risk = load_risk(selected_regions)

    total_records = len(risk)
    countries_affected = risk["country_name"].nunique() if not risk.empty else 0
    vaccine_types = risk["vaccine_description"].nunique() if not risk.empty else 0
    top_region = risk["who_region"].value_counts().idxmax() if not risk.empty else "—"
    # composite risk score: density of gaps per affected country, capped 0-100
    risk_score = int(min(100, (total_records / max(countries_affected, 1)) * 12))

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, f"{total_records:,}", "At-Risk Records")
    kpi_card(c2, f"{countries_affected}", "Countries Affected")
    kpi_card(c3, f"{vaccine_types}", "Vaccine Types Involved")
    kpi_card(c4, top_region, "Highest-Risk Region")
    kpi_card(c5, f"{risk_score}/100", "Composite Risk Score")

    st.write("")

    if risk.empty:
        st.info("No risk records for the selected filters.")
    else:
        col1, col2 = st.columns([1.4, 1])
        with col1:
            section("Risk Matrix", "Countries ranked by number of single-dose vaccine gaps")
            matrix = risk.groupby(["country_name", "who_region"]).size().reset_index(name="gap_count")
            matrix = matrix.sort_values("gap_count", ascending=False).head(20)
            figm = px.bar(matrix.sort_values("gap_count"), x="gap_count", y="country_name",
                          color="who_region", orientation="h", color_discrete_sequence=PALETTE)
            figm.update_layout(title="Top 20 Countries by Risk Gaps", yaxis_title="", xaxis_title="Gap Count")
            style(figm, 480)
            st.plotly_chart(figm, width="stretch")
        with col2:
            section("Risk Composition", "Share of gaps by vaccine type")
            vc = risk["vaccine_description"].value_counts().reset_index()
            vc.columns = ["vaccine_description", "count"]
            figp = px.pie(vc.head(8), names="vaccine_description", values="count", hole=0.55,
                          color_discrete_sequence=PALETTE)
            figp.update_traces(textposition="inside", textinfo="percent")
            figp.update_layout(title="Top Vaccine Types at Risk")
            style(figp, 480)
            st.plotly_chart(figp, width="stretch")

        section("Regional Risk Treemap", "Region → vaccine type → gap count, sized and colored by volume")
        tm = risk.groupby(["who_region", "vaccine_description"]).size().reset_index(name="count")
        figt = px.treemap(tm, path=["who_region", "vaccine_description"], values="count",
                          color="count", color_continuous_scale=[GREEN, AMBER, RED])
        figt.update_layout(title=None)
        style(figt, 440)
        st.plotly_chart(figt, width="stretch")

        with st.expander("🔍 Full Risk Table"):
            st.dataframe(risk, width="stretch", height=420)
            st.download_button("⬇ Download as CSV", risk.to_csv(index=False), "risk_and_gaps.csv", "text/csv")

elif page == "🦠  Disease Trends":
    section("Disease Trends", "Historical case counts and regional incidence")

    cases = load_cases_trend()
    region_inc = load_region_incidence()

    disease_options = sorted(cases["disease"].unique())
    picked = st.multiselect("Filter diseases", disease_options, default=disease_options[:5])
    filtered = cases[cases["disease"].isin(picked)] if picked else cases

    col1, col2 = st.columns([1.4, 1])
    with col1:
        fig1 = px.area(filtered, x="year", y="avg_cases", color="disease", color_discrete_sequence=PALETTE)
        fig1.update_layout(title="Average Cases by Year and Disease")
        style(fig1, 460)
        st.plotly_chart(fig1, width="stretch")
    with col2:
        r = region_inc.sort_values("avg_incidence_rate")
        fig2 = px.bar(r, x="avg_incidence_rate", y="who_region", orientation="h", color_discrete_sequence=[GREEN])
        fig2.update_layout(title="Avg Incidence by WHO Region")
        style(fig2, 460)
        st.plotly_chart(fig2, width="stretch")

elif page == "🎯  2030 Measles Target":
    st.markdown(f"""
    <div class="hero">
        <div class="tag">🎯 WHO 2030 TARGET TRACKER</div>
        <h1>Measles Elimination Countdown</h1>
        <p>Tracking global progress toward the WHO 95%-by-2030 measles coverage target.</p>
    </div>
    """, unsafe_allow_html=True)

    trend = load_measles_target()
    intro = load_intro_timeline()
    latest_cov = float(trend["measles_coverage_pct"].iloc[-1])
    gap = float(trend["gap_to_95pct_target"].iloc[-1])
    latest_year = int(trend["year"].iloc[-1])
    years_left = max(0, 2030 - latest_year)

    # simple linear projection using the most recent points on record
    recent = trend.tail(5)
    slope = np.polyfit(recent["year"], recent["measles_coverage_pct"], 1)[0] if len(recent) >= 2 else 0.0
    projected_2030 = float(np.clip(latest_cov + slope * (2030 - latest_year), 0, 100))
    progress_pct = int(min(100, (latest_cov / 95) * 100))

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, f"{latest_cov:.1f}%", f"Coverage ({latest_year})")
    kpi_card(c2, f"{gap:.2f} pts", "Gap to 95% Target")
    kpi_card(c3, f"{years_left}", "Years Remaining")
    kpi_card(c4, f"{projected_2030:.1f}%", "Projected 2030 Coverage")

    st.write("")
    c1, c2 = st.columns([1, 2.2])
    with c1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=latest_cov,
            delta={"reference": 95, "increasing": {"color": GREEN}, "decreasing": {"color": RED}},
            number={"suffix": "%", "font": {"color": "#FFFFFF", "size": 40}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": MUTE},
                "bar": {"color": GREEN},
                "bgcolor": SURFACE,
                "steps": [
                    {"range": [0, 60], "color": "rgba(240,113,111,0.25)"},
                    {"range": [60, 85], "color": "rgba(240,178,85,0.25)"},
                    {"range": [85, 100], "color": "rgba(43,217,160,0.25)"},
                ],
                "threshold": {"line": {"color": RED, "width": 3}, "value": 95},
            },
        ))
        fig_gauge.update_layout(
            title="Latest Measles Coverage vs 95% Target", height=320,
            font=PLOT_TEMPLATE["font"], paper_bgcolor=PLOT_TEMPLATE["paper_bgcolor"],
            margin=PLOT_TEMPLATE["margin"],
        )
        st.plotly_chart(fig_gauge, width="stretch")

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label" style="margin-bottom:8px;">Progress toward 95% target</div>
            <div class="progress-track"><div class="progress-fill" style="width:{progress_pct}%;"></div></div>
            <div class="kpi-label" style="margin-top:8px;text-align:right;">{progress_pct}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        fig0 = px.area(trend, x="year", y="measles_coverage_pct", color_discrete_sequence=[GREEN])
        fig0.add_hline(y=95, line_dash="dot", line_color=RED, annotation_text="95% target")
        fig0.add_trace(go.Scatter(
            x=[latest_year, 2030], y=[latest_cov, projected_2030],
            mode="lines+markers", line=dict(color=AMBER, dash="dash"),
            marker=dict(size=8), name="Projected trajectory",
        ))
        fig0.update_layout(title="Measles Coverage Over Time + 2030 Projection")
        style(fig0, 300)
        st.plotly_chart(fig0, width="stretch")

        fig1 = px.area(intro, x="year", y="vaccines_introduced", color="who_region", color_discrete_sequence=PALETTE)
        fig1.update_layout(title="Vaccine Introductions by Region")
        style(fig1, 260)
        st.plotly_chart(fig1, width="stretch")

elif page == "🗂️  Raw Data Explorer":
    section("Raw Data Explorer", "Browse any base table directly from vaccination_db")

    if not LIVE:
        st.warning("Connect to MySQL (.env) to browse raw tables — not available in demo mode.")
    else:
        table = st.selectbox("Choose a table", [
            "countries", "coverage_data", "incidence_rate",
            "reported_cases", "vaccine_introduction", "vaccine_schedule",
        ])
        limit = st.slider("Rows to load", 50, 2000, 300, step=50)
        df = load_raw_table(table, limit)
        st.dataframe(df, width="stretch", height=520)
        st.download_button("⬇ Download as CSV", df.to_csv(index=False), f"{table}.csv", "text/csv")
