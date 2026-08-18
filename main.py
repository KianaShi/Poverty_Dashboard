import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Poverty Lens | U.S. County Dashboard",
    page_icon="◒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    :root { --ink:#18232b; --muted:#718087; --line:#e7ecec; --paper:#ffffff; --canvas:#f3f6f5; --teal:#13a8a3; --pink:#ee86b7; --lime:#b9db72; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    .stApp { background:var(--canvas); }
    .block-container { max-width:1500px; padding:1.4rem 2rem 4rem; }
    [data-testid="stSidebar"] { background:#14201f; border-right:0; min-width:230px; max-width:230px; }
    [data-testid="stSidebar"] * { color:#eaf3f1 !important; }
    [data-testid="stSidebar"] .stRadio label { padding:.55rem .7rem; border-radius:10px; }
    [data-testid="stSidebar"] .stRadio label:has(input:checked) { background:#243432; }
    [data-testid="stSidebar"] hr { border-color:#31413f; }
    h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:var(--ink); }
    h2 { font-size:1.18rem !important; margin:.1rem 0 .8rem !important; }
    h3 { font-size:.98rem !important; }
    .hero { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin:.2rem 0 1.25rem; }
    .hero h1 { font-size:clamp(1.7rem,2.6vw,2.6rem); line-height:1.08; margin:.25rem 0 .4rem; max-width:850px; }
    .hero p { color:var(--muted); margin:0; max-width:760px; font-size:.96rem; }
    .eyebrow { color:var(--teal); font-weight:700; font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; }
    .year-badge { background:#e6f7f4; color:#087f7b; padding:.45rem .75rem; border-radius:999px; font-weight:700; font-size:.78rem; white-space:nowrap; }
    .section-card, [data-testid="stVerticalBlockBorderWrapper"] { background:var(--paper); border:1px solid var(--line) !important; border-radius:16px !important; box-shadow:0 8px 30px rgba(21,44,41,.045); }
    [data-testid="stVerticalBlockBorderWrapper"] { padding:.85rem 1rem; }
    div[data-testid="stSelectbox"] > label, div[data-testid="stSlider"] > label { color:#62716f; font-size:.78rem; font-weight:700; }
    div[data-baseweb="select"] > div { background:#fff; border-color:var(--line); border-radius:10px; }
    .kpi-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:.35rem 0 1.2rem; }
    .kpi { background:#fff; border:1px solid var(--line); border-radius:14px; padding:1rem 1.1rem; box-shadow:0 6px 22px rgba(21,44,41,.035); }
    .kpi-label { color:var(--muted); font-size:.75rem; font-weight:600; }
    .kpi-value { font-family:'Manrope',sans-serif; font-size:1.65rem; font-weight:800; letter-spacing:-.04em; margin:.2rem 0; }
    .kpi-note { color:#169e89; font-size:.72rem; font-weight:700; }
    .sidebar-brand { font-family:'Manrope',sans-serif; font-size:1.08rem; font-weight:800; padding:.5rem .1rem 1.1rem; }
    .sidebar-brand span { display:inline-grid; place-items:center; width:28px; height:28px; border-radius:9px; background:var(--teal); margin-right:8px; }
    .side-note { color:#a7b8b4 !important; font-size:.72rem; line-height:1.55; }
    hr { border:none; border-top:1px solid var(--line); margin:1.25rem 0; }
    [data-testid="stPlotlyChart"] { border-radius:14px; overflow:hidden; }
    [data-testid="stAlert"] { border-radius:11px; border:0; font-size:.82rem; }
    .stCaption { color:#8b9896; }
    @media (max-width:900px) { .block-container{padding:1rem;} .hero{flex-direction:column;} .kpi-grid{grid-template-columns:1fr;} [data-testid="stSidebar"]{min-width:200px;} }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-brand"><span>◒</span>Poverty Lens</div>', unsafe_allow_html=True)
    st.caption("EXPLORE")
    st.radio("Dashboard navigation", ["Overview", "State Map", "Distribution", "Occupation", "Child Poverty"], label_visibility="collapsed")
    st.divider()
    st.markdown('<div class="side-note">ACS county data<br>2015 + 2017 editions</div>', unsafe_allow_html=True)

# load data
df_2015 = pd.read_csv("data/acs2015_county_data.csv")
df_2017 = pd.read_csv("data/acs2017_county_data.csv")

df_2015["Year"] = 2015
df_2017["Year"] = 2017

df = pd.concat([df_2015, df_2017], ignore_index=True)
df.columns = df.columns.str.strip()

numeric_cols = [
    "Income", "IncomePerCap", "Poverty", "ChildPoverty",
    "Professional", "Service", "Office", "Construction", "Production",
    "Unemployment"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["State", "County", "Income", "Poverty"])

# title
st.markdown("""
<div class="hero">
  <div>
    <div class="eyebrow">United States · County intelligence</div>
    <h1>Poverty, work and childhood — in one view.</h1>
    <p>Explore how household income and occupational structure shape poverty across U.S. counties, with focused analysis for every chart.</p>
  </div>
  <div class="year-badge">ACS · 2 editions</div>
</div>
""", unsafe_allow_html=True)

# Feature Selection
f1, f2, f3 = st.columns(3)

with f1:
    year = st.selectbox("Year", [2015, 2017])

with f2:
    selected_state = st.selectbox(
        "State",
        ["All"] + sorted(df["State"].dropna().unique().tolist())
    )

with f3:
    poverty_range = st.slider(
        "Poverty Range",
        float(df["Poverty"].min()),
        float(df["Poverty"].max()),
        (float(df["Poverty"].min()), float(df["Poverty"].max()))
    )

# filter
filtered_df = df[df["Year"] == year].copy()

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]

filtered_df = filtered_df[
    (filtered_df["Poverty"] >= poverty_range[0]) &
    (filtered_df["Poverty"] <= poverty_range[1])
]

# KPI
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Counties in view</div><div class="kpi-value">{filtered_df.shape[0]:,}</div><div class="kpi-note">Filtered county sample</div></div>
  <div class="kpi"><div class="kpi-label">Average poverty</div><div class="kpi-value">{filtered_df['Poverty'].mean():.1f}%</div><div class="kpi-note">Share of residents</div></div>
  <div class="kpi"><div class="kpi-label">Average household income</div><div class="kpi-value">${filtered_df['Income'].mean():,.0f}</div><div class="kpi-note">Across selected counties</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}


# ===== section 1: State-Level Map =====
st.subheader(f"State-Level Poverty and Dominant Occupation ({year})")

occupation_cols = ["Professional", "Service", "Office", "Construction", "Production"]

# statesummary
state_summary = (
    filtered_df.groupby("State", as_index=False)
    .agg({
        "Poverty": "mean",
        "Income": "mean",
        **{col: "mean" for col in occupation_cols}
    })
)

# dominant occupation
national_avg = filtered_df[occupation_cols].mean()

for col in occupation_cols:
    state_summary[col + "_diff"] = state_summary[col] - national_avg[col]

diff_cols = [col + "_diff" for col in occupation_cols]

state_summary["Dominant Occupation"] = (
    state_summary[diff_cols]
    .idxmax(axis=1)
    .str.replace("_diff", "", regex=False)
)

# Short
occ_short = {
    "Professional": "Prof",
    "Service": "Serv",
    "Office": "Off",
    "Construction": "Const",
    "Production": "Prod"
}
state_summary["Occ Short"] = state_summary["Dominant Occupation"].map(occ_short)

# abbrev
state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}
state_summary["State Code"] = state_summary["State"].map(state_abbrev)
state_summary = state_summary.dropna(subset=["State Code"])

# show name
state_summary["Label"] = state_summary["State Code"] + "<br>" + state_summary["Occ Short"]

# mid point
state_centers = {
    "AL": (32.8, -86.8), "AK": (64.0, -152.0), "AZ": (34.2, -111.7), "AR": (34.8, -92.2),
    "CA": (37.2, -119.5), "CO": (39.0, -105.5), "CT": (41.6, -72.7), "DE": (39.0, -75.5),
    "FL": (28.4, -82.4), "GA": (32.7, -83.3), "HI": (20.8, -157.5), "ID": (44.2, -114.0),
    "IL": (40.0, -89.2), "IN": (40.0, -86.1), "IA": (42.1, -93.5), "KS": (38.5, -98.0),
    "KY": (37.5, -85.3), "LA": (31.0, -92.0), "ME": (45.3, -69.0), "MD": (39.0, -76.7),
    "MA": (42.3, -71.8), "MI": (44.3, -85.4), "MN": (46.3, -94.2), "MS": (32.7, -89.7),
    "MO": (38.5, -92.5), "MT": (46.9, -110.4), "NE": (41.5, -99.7), "NV": (39.3, -116.6),
    "NH": (43.7, -71.6), "NJ": (40.1, -74.7), "NM": (34.4, -106.1), "NY": (42.9, -75.0),
    "NC": (35.5, -79.4), "ND": (47.5, -100.5), "OH": (40.4, -82.8), "OK": (35.6, -97.5),
    "OR": (43.9, -120.6), "PA": (41.0, -77.6), "RI": (41.7, -71.5), "SC": (33.8, -80.9),
    "SD": (44.4, -100.2), "TN": (35.8, -86.4), "TX": (31.5, -99.3), "UT": (39.3, -111.7),
    "VT": (44.1, -72.7), "VA": (37.5, -78.7), "WA": (47.4, -120.7), "WV": (38.6, -80.6),
    "WI": (44.5, -89.5), "WY": (43.0, -107.6), "DC": (38.9, -77.0)
}

state_summary["lat"] = state_summary["State Code"].map(lambda x: state_centers[x][0])
state_summary["lon"] = state_summary["State Code"].map(lambda x: state_centers[x][1])

map_left, map_right = st.columns([4, 1.4])

with map_left:
    fig_map = px.choropleth(
        state_summary,
        locations="State Code",
        locationmode="USA-states",
        color="Poverty",
        scope="usa",
        hover_name="State",
        hover_data={
            "State Code": False,
            "Poverty": ':.1f',
            "Income": ':,.0f',
            "Dominant Occupation": True,
            "Occ Short": False,
            "lat": False,
            "lon": False,
            "Label": False
        },
        color_continuous_scale=[[0, "#e7f7f4"], [0.45, "#72d2cc"], [0.75, "#f1a7c8"], [1, "#d94f91"]],
        labels={
            "Poverty": "Avg Poverty Rate (%)",
            "Income": "Avg Income",
            "Dominant Occupation": "Dominant Occupation"
        }
    )

    # add name+occupation
    fig_map.add_scattergeo(
        locations=state_summary["State Code"],
        locationmode="USA-states",
        text=state_summary["Label"],
        mode="text",
        textfont=dict(size=9, color="black"),
        hoverinfo="skip"
    )

    fig_map.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#50605e"),
        coloraxis_colorbar=dict(thickness=8, outlinewidth=0),
        geo=dict(bgcolor="rgba(0,0,0,0)")
    )

    st.plotly_chart(fig_map, width="stretch")

with map_right:
  with st.container(border=True):
    st.markdown("### Map insight")

    if len(state_summary) > 0:
        top_state = state_summary.sort_values("Poverty", ascending=False).iloc[0]
        low_state = state_summary.sort_values("Poverty", ascending=True).iloc[0]

        occ_counts = (
            state_summary["Dominant Occupation"]
            .value_counts()
            .reset_index()
        )
        occ_counts.columns = ["Occupation", "State Count"]

        st.write(f"States shown: **{len(state_summary)}**")
        st.write(f"Highest avg poverty: **{top_state['State']} ({top_state['Poverty']:.1f}%)**")
        st.write(f"Lowest avg poverty: **{low_state['State']} ({low_state['Poverty']:.1f}%)**")

        st.markdown("**Dominant occupation across states:**")
        for _, row in occ_counts.iterrows():
            st.write(f"- {row['Occupation']}: **{row['State Count']} states**")

        st.info("Darker color means higher poverty. Labels pair each state with its dominant occupation.")
    else:
        st.write("No state-level data available for the current selection.")

st.caption("Color indicates average poverty rate. Each state label shows the state abbreviation and dominant occupation.")

st.markdown("---")

# ===== Section 2: Poverty Distribution =====
st.subheader(f"Poverty Distribution ({year})")

left1, right1 = st.columns([3, 1])

with left1:
    fig1 = px.histogram(
        filtered_df,
        x="Poverty",
        nbins=20,
        color_discrete_sequence=["#ee86b7"]
    )
    fig1.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfcfc",
        font=dict(family="DM Sans", color="#50605e"),
        xaxis_title="Poverty Rate",
        yaxis_title="Number of Counties",
        bargap=.12
    )
    st.plotly_chart(fig1, width="stretch")

with right1:
  with st.container(border=True):
    avg_poverty = filtered_df["Poverty"].mean()
    median_poverty = filtered_df["Poverty"].median()
    max_poverty = filtered_df["Poverty"].max()
    min_poverty = filtered_df["Poverty"].min()

    high_poverty_count = (filtered_df["Poverty"] >= 20).sum()
    high_poverty_pct = high_poverty_count / len(filtered_df) * 100 if len(filtered_df) > 0 else 0

    st.markdown("### Quick analysis")
    st.write(f"Average poverty rate: **{avg_poverty:.1f}%**")
    st.write(f"Median poverty rate: **{median_poverty:.1f}%**")
    st.write(f"Range: **{min_poverty:.1f}% – {max_poverty:.1f}%**")
    st.write(f"Counties with poverty ≥ 20%: **{high_poverty_count}**")
    st.write(f"Share of high-poverty counties: **{high_poverty_pct:.1f}%**")

    if avg_poverty >= 20:
        st.info("Poverty is relatively high in the current selection.")
    elif avg_poverty >= 12:
        st.info("Poverty is moderate in the current selection.")
    else:
        st.info("Poverty is relatively low in the current selection.")

st.caption("This chart shows how poverty rates are distributed across counties in the selected data.")

#occupation

st.markdown("---")

st.subheader("Select Occupation for Analysis")

occupation_col = st.selectbox(
    "Occupation",
    ["Professional", "Service", "Office", "Construction", "Production"]
)
st.markdown("---")

# ===== Section 3: Poverty vs Occupation =====

st.subheader(f"{occupation_col} vs Poverty ({year})")

left4, right4 = st.columns([3, 1])

# ===== left =====
with left4:
    fig4 = px.scatter(
        filtered_df,
        x=occupation_col,
        y="Poverty",
        hover_name="County",
        hover_data=["State"],
        trendline="ols",
        color_discrete_sequence=["#13a8a3"]
    )

    fig4.update_traces(marker=dict(size=5, opacity=0.5))

    fig4.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfcfc",
        font=dict(family="DM Sans", color="#50605e"),
        xaxis_title=occupation_col,
        yaxis_title="Poverty Rate"
    )

    st.plotly_chart(fig4, width="stretch")


# ===== right =====
with right4:
  with st.container(border=True):
    st.markdown("### Trend analysis")

    if len(filtered_df) > 0:
        corr = filtered_df[occupation_col].corr(filtered_df["Poverty"])
        avg_occ = filtered_df[occupation_col].mean()
        avg_poverty = filtered_df["Poverty"].mean()

        st.write(f"Average {occupation_col}: **{avg_occ:.1f}%**")
        st.write(f"Average poverty: **{avg_poverty:.1f}%**")
        st.write(f"Correlation: **{corr:.2f}**")

        # auto explain
        if corr > 0.4:
            st.warning("Positive relationship")
            st.write(f"Higher {occupation_col.lower()} share is associated with higher poverty.")
        elif corr < -0.4:
            st.success("Negative relationship")
            st.write(f"Higher {occupation_col.lower()} share is associated with lower poverty.")
        else:
            st.info("Weak relationship")
            st.write(f"{occupation_col} does not strongly explain poverty variation.")

    else:
        st.write("No data available.")

st.caption("The share of this occupational group may be associated with different poverty patterns.")

st.markdown("---")

# ===== Section 4: Top 10 Counties by Child Poverty =====
st.subheader(f"Top 10 Counties by Child Poverty ({year})")

left2, right2 = st.columns([3, 1])
top_counties = (
    filtered_df[["County", "State", "ChildPoverty"]]
    .sort_values("ChildPoverty", ascending=False)
    .head(10)
    .copy()
)


top_counties["Rank"] = range(len(top_counties), 0, -1)
top_counties["CountyLabel"] = top_counties["County"] + ", " + top_counties["State"]

with left2:
    fig2 = px.bar(
        top_counties,
        x="CountyLabel",
        y="ChildPoverty",
        color="Rank",
        color_continuous_scale=[[0, "#b7e4df"], [0.55, "#7ccfc8"], [1, "#ee86b7"]]
    )
    fig2.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fbfcfc",
        font=dict(family="DM Sans", color="#50605e"),
        xaxis_title="County",
        yaxis_title="Child Poverty Rate",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, width="stretch")

with right2:
  with st.container(border=True):
    st.markdown("### Quick analysis")

    if len(top_counties) > 0:
        top1 = top_counties.iloc[0]
        avg_top10 = top_counties["ChildPoverty"].mean()

        overall_avg = filtered_df["ChildPoverty"].mean()
        gap = top1["ChildPoverty"] - overall_avg

        st.write(f"Highest child-poverty county: **{top1['County']}, {top1['State']}**")
        st.write(f"Top child poverty rate: **{top1['ChildPoverty']:.1f}%**")
        st.write(f"Average among top 10 counties: **{avg_top10:.1f}%**")
        st.write(f"Gap from overall average: **{gap:.1f} percentage points**")

        if gap > 10:
            st.info("Child poverty is highly concentrated in the top counties, indicating strong inequality.")
        else:
            st.info("Child poverty levels are moderately higher in top counties.")
    else:
        st.write("No data available for the current selection.")

st.caption("This chart highlights counties with the highest child poverty rates.")

st.markdown("---")
