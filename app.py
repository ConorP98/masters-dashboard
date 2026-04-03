import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Masters 2026 · Decision Support",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --green:       #4ade80;
    --green-dim:   #166534;
    --green-glow:  rgba(74,222,128,0.15);
    --bg:          #0a0f0a;
    --surface:     #111811;
    --surface2:    #182018;
    --border:      rgba(74,222,128,0.18);
    --text:        #e8f0e8;
    --text-muted:  #7a9a7a;
    --red:         #f87171;
    --gold:        #fbbf24;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--text) !important;
}

code, .mono {
    font-family: 'DM Mono', monospace !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--green) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--green-glow) !important;
    border-color: var(--green) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Slider */
.stSlider > div > div > div {
    background: var(--green-dim) !important;
}
.stSlider > div > div > div > div {
    background: var(--green) !important;
}

/* Select */
.stMultiSelect > div, .stSelectbox > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Nav pills */
.nav-pill {
    display: inline-block;
    padding: 6px 18px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
    margin-right: 8px;
}
.nav-pill.active {
    background: var(--green-glow);
    border-color: var(--green);
    color: var(--green);
}

/* Player card */
.player-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.player-card:hover { border-color: var(--green); }

.player-card .name {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
}
.player-card .sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    margin-top: 2px;
}
.player-card .odds {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: var(--green);
}

/* Risk badge */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}
.badge-safe     { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.badge-balanced { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-high     { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

/* Team panel */
.team-panel {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
}
.team-panel.valid   { border-color: #4ade80; box-shadow: 0 0 20px rgba(74,222,128,0.1); }
.team-panel.invalid { border-color: #f87171; box-shadow: 0 0 20px rgba(248,113,113,0.05); }

/* Section header */
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
}

/* Stat row */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(74,222,128,0.06);
    font-size: 13px;
}
.stat-row .label { color: var(--text-muted); font-family: 'DM Mono', monospace; font-size: 11px; }
.stat-row .value { color: var(--text); font-weight: 500; }

/* Page title */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.01em;
    background: linear-gradient(135deg, #e8f0e8 0%, #4ade80 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 4px;
}

/* Profile headshot placeholder */
.headshot-placeholder {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--surface2);
    border: 2px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    color: var(--text-muted);
}

/* Scrollable table container */
.scroll-container {
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

@st.cache_data
def load_players():
    df = pd.read_csv("consolidated_player_data_2026.csv")
    df = compute_value_scores(df)
    df["risk"] = df["odds"].apply(classify_risk)
    df["implied_prob"] = 1 / (df["odds"] + 1)
    return df

@st.cache_data
def load_historical_odds():
    return pd.read_csv("historical_odds.csv")

@st.cache_data
def load_historical_scores():
    return pd.read_csv("historical_scores.csv")

@st.cache_data
def load_historical_rounds():
    return pd.read_csv("historical_rounds.csv")

@st.cache_data
def load_historical_teams():
    return pd.read_csv("historical_teams.csv")

@st.cache_data
def load_historical_picks():
    return pd.read_csv("historical_picks.csv")

@st.cache_data
def load_historical_winners():
    return pd.read_csv("historical_previous_winners.csv")

# ─────────────────────────────────────────────
# BUSINESS LOGIC
# ─────────────────────────────────────────────

def minmax(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - mn) / (mx - mn)

def compute_value_scores(df):
    df = df.copy()
    cols_needed = ["avg_round", "cuts_made_percentage", "masters_wins",
                   "rounds_under_par_percentage", "best_finish_position"]
    for c in cols_needed:
        if c not in df.columns:
            df[c] = 0

    df["_n_avg_round"]   = 1 - minmax(df["avg_round"])
    df["_n_cuts"]        = minmax(df["cuts_made_percentage"])
    df["_n_wins"]        = minmax(df["masters_wins"])
    df["_n_rup"]         = minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"] = 1 - minmax(df["best_finish_position"])

    df["value_score"] = (
        0.30 * df["_n_avg_round"] +
        0.20 * df["_n_cuts"] +
        0.20 * df["_n_wins"] +
        0.15 * df["_n_rup"] +
        0.15 * df["_n_best_finish"]
    )
    drop = [c for c in df.columns if c.startswith("_n_")]
    df.drop(columns=drop, inplace=True)
    return df

def classify_risk(odds):
    if odds < 25:
        return "Safe"
    elif odds <= 60:
        return "Balanced"
    return "High Risk"

def risk_badge_html(risk):
    cls = {"Safe": "badge-safe", "Balanced": "badge-balanced", "High Risk": "badge-high"}.get(risk, "badge-safe")
    return f'<span class="badge {cls}">{risk}</span>'

def team_strength(players_df):
    return players_df["value_score"].sum()

def combined_odds(players_df):
    return players_df["odds"].sum()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

def init_state():
    if "selected_ids" not in st.session_state:
        st.session_state.selected_ids = []
    if "page" not in st.session_state:
        st.session_state.page = "Player Picker"
    if "profile_id" not in st.session_state:
        st.session_state.profile_id = None

init_state()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.title("⛳ Masters 2026 Dashboard")
page_options = ["Player Picker", "Player Profile", "Historical Dashboard"]

for option in page_options:
    active = "active" if st.session_state.page == option else ""
    if st.sidebar.button(option):
        st.session_state.page = option

st.sidebar.markdown("---")
st.sidebar.markdown("Data & AI by Your Name | v1.0")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
players_df = load_players()
historical_odds_df = load_historical_odds()
historical_scores_df = load_historical_scores()
historical_rounds_df = load_historical_rounds()
historical_teams_df = load_historical_teams()
historical_picks_df = load_historical_picks()
historical_winners_df = load_historical_winners()

# ─────────────────────────────────────────────
# PLAYER PICKER PAGE
# ─────────────────────────────────────────────
if st.session_state.page == "Player Picker":
    st.markdown('<div class="page-title">Player Picker</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Select your Masters 2026 team</div>', unsafe_allow_html=True)
    st.markdown("---")

    search_name = st.text_input("Search player by name")
    if search_name:
        display_df = players_df[players_df["name"].str.contains(search_name, case=False, na=False)]
    else:
        display_df = players_df.copy()

    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
    for idx, row in display_df.iterrows():
        selected = idx in st.session_state.selected_ids
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f'<div class="player-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="name">{row["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sub">{row["nationality"]} | Age {row.get("age","-")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="odds">{row["odds"]}x</div>', unsafe_allow_html=True)
            st.markdown(risk_badge_html(row["risk"]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            if selected:
                if st.button("Remove", key=f"remove_{idx}"):
                    st.session_state.selected_ids.remove(idx)
            else:
                if st.button("Add", key=f"add_{idx}"):
                    st.session_state.selected_ids.append(idx)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.write(f"Selected Players: {len(st.session_state.selected_ids)}")
    if st.session_state.selected_ids:
        team_df = players_df.loc[st.session_state.selected_ids]
        st.write(team_df[["name","odds","risk","value_score"]])
        st.write(f"Team Strength: {team_strength(team_df):.2f}")
        st.write(f"Combined Odds: {combined_odds(team_df):.2f}")

# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "Player Profile":
    st.markdown('<div class="page-title">Player Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Individual player stats & history</div>', unsafe_allow_html=True)
    st.markdown("---")

    player_name = st.selectbox("Select Player", players_df["name"].tolist())
    profile = players_df[players_df["name"] == player_name].iloc[0]

    st.markdown('<div class="headshot-placeholder">', unsafe_allow_html=True)
    st.markdown(profile["name"][0], unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"**Nationality:** {profile['nationality']}")
    st.write(f"**Age:** {profile.get('age','-')}")
    st.write(f"**Masters Wins:** {profile.get('masters_wins',0)}")
    st.write(f"**Value Score:** {profile.get('value_score',0):.2f}")
    st.write(f"**Odds:** {profile.get('odds',0)}")
    st.write(f"**Risk:** {profile.get('risk','-')}")

    st.markdown("### Historical Performance")
    hist_scores = historical_scores_df[historical_scores_df["Golfer"] == player_name]
    if not hist_scores.empty:
        fig = px.line(hist_scores, x="Year", y="Score", title=f"{player_name} Score History")
        st.plotly_chart(fig)
    else:
        st.write("No historical score data available.")

# ─────────────────────────────────────────────
# HISTORICAL DASHBOARD PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "Historical Dashboard":
    st.markdown('<div class="page-title">Historical Masters Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Past winners, team stats, odds & performance trends</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Winners", "Teams", "Odds Trend"])

    with tab1:
        st.write(historical_winners_df.sort_values("Year", ascending=False))

    with tab2:
        fig = px.bar(historical_teams_df, x="Year", y="Team_Score", color="Team_Name",
                     title="Historical Team Scores by Year")
        st.plotly_chart(fig)

    with tab3:
        fig = go.Figure()
        for player in historical_odds_df["Golfer"].unique():
            temp = historical_odds_df[historical_odds_df["Golfer"] == player]
            fig.add_trace(go.Scatter(x=temp["Year"], y=temp["Odds"], mode="lines+markers", name=player))
        fig.update_layout(title="Historical Odds by Player", xaxis_title="Year", yaxis_title="Odds")
        st.plotly_chart(fig)
