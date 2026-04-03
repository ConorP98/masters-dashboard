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

    # Lower avg_round is better → invert
    df["_n_avg_round"]   = 1 - minmax(df["avg_round"])
    df["_n_cuts"]        = minmax(df["cuts_made_percentage"])
    df["_n_wins"]        = minmax(df["masters_wins"])
    df["_n_rup"]         = minmax(df["rounds_under_par_percentage"])
    # Lower best_finish_position is better → invert
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
# SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar(df):
    with st.sidebar:
        st.markdown('<div class="page-title" style="font-size:24px;">⛳ Masters 2026</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Decision Support Tool</div>', unsafe_allow_html=True)
        st.markdown("---")

        # Navigation
        st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
        pages = ["Player Picker", "Player Profile", "Historical Dashboard"]
        for p in pages:
            active = "active" if st.session_state.page == p else ""
            icon = {"Player Picker": "⬜", "Player Profile": "👤", "Historical Dashboard": "📊"}[p]
            if st.button(f"{icon}  {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()

        st.markdown("---")

        # Filters (only shown on Player Picker)
        if st.session_state.page == "Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)

            odds_min, odds_max = int(df["odds"].min()), int(df["odds"].max())
            odds_range = st.slider("Odds range", odds_min, odds_max, (odds_min, odds_max))

            age_min, age_max = int(df["age"].min()), int(df["age"].max())
            age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))

            countries = sorted(df["country"].dropna().unique().tolist())
            selected_countries = st.multiselect("Country", countries)

            masters_winners_only = st.toggle("Masters winners only", value=False)

            cuts_min = float(df["cuts_made_percentage"].min())
            cuts_max = float(df["cuts_made_percentage"].max())
            cuts_range = st.slider("Cuts made %", cuts_min, cuts_max, (cuts_min, cuts_max))

            return {
                "odds_range": odds_range,
                "age_range": age_range,
                "countries": selected_countries,
                "masters_winners_only": masters_winners_only,
                "cuts_range": cuts_range,
            }

    return {}

# ─────────────────────────────────────────────
# PLAYER PICKER PAGE
# ─────────────────────────────────────────────

def render_player_picker(df, filters):
    # Apply filters
    fdf = df.copy()
    fdf = fdf[fdf["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"]:
        fdf = fdf[fdf["country"].isin(filters["countries"])]
    if filters["masters_winners_only"]:
        fdf = fdf[fdf["masters_wins"] > 0]
    fdf = fdf[fdf["cuts_made_percentage"].between(*filters["cuts_range"])]

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        st.markdown('<div class="section-header">Player Pool</div>', unsafe_allow_html=True)
        st.caption(f"{len(fdf)} players · {len(st.session_state.selected_ids)}/3 selected")

        # Sort options
        sort_col = st.selectbox(
            "Sort by",
            ["odds", "value_score", "age", "cuts_made_percentage", "masters_wins"],
            format_func=lambda x: x.replace("_", " ").title(),
            label_visibility="collapsed",
        )
        fdf = fdf.sort_values(sort_col, ascending=(sort_col == "odds"))

        # Player list
        for _, row in fdf.iterrows():
            pid = row["id"]
            is_selected = pid in st.session_state.selected_ids
            card_border = "border-color: var(--green);" if is_selected else ""

            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"""
                <div class="player-card" style="{card_border}">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{row.get('country','—')} · Age {int(row['age'])} · 
                        {risk_badge_html(row['risk'])}
                    </div>
                    <div style="display:flex;gap:24px;margin-top:10px;align-items:flex-end;">
                        <div>
                            <div class="sub">ODDS</div>
                            <div class="odds">{int(row['odds'])}/1</div>
                        </div>
                        <div>
                            <div class="sub">VALUE</div>
                            <div style="font-size:18px;font-family:'DM Mono';color:var(--text);">{row['value_score']:.3f}</div>
                        </div>
                        <div>
                            <div class="sub">CUTS MADE</div>
                            <div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{row['cuts_made_percentage']:.0f}%</div>
                        </div>
                        <div>
                            <div class="sub">AVG RND</div>
                            <div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{row['avg_round']:.1f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                if is_selected:
                    if st.button("✕ Remove", key=f"rem_{pid}"):
                        st.session_state.selected_ids.remove(pid)
                        st.rerun()
                else:
                    if len(st.session_state.selected_ids) < 3:
                        if st.button("➕ Add", key=f"add_{pid}"):
                            st.session_state.selected_ids.append(pid)
                            st.rerun()

    with right_col:
        render_team_panel(df)

# ─────────────────────────────────────────────
# TEAM PANEL
# ─────────────────────────────────────────────

def render_team_panel(df):
    st.markdown('<div class="section-header">Selected Team</div>', unsafe_allow_html=True)
    if st.session_state.selected_ids:
        team_df = df[df["id"].isin(st.session_state.selected_ids)]
        for _, row in team_df.iterrows():
            st.markdown(f"""
                <div class="player-card">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{risk_badge_html(row['risk'])}</div>
                </div>
            """, unsafe_allow_html=True)

        # Summary metrics
        total_value = team_strength(team_df)
        total_odds  = combined_odds(team_df)
        st.markdown(f"<div class='stat-row'><span class='label'>Team Strength</span><span class='value'>{total_value:.3f}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-row'><span class='label'>Combined Odds</span><span class='value'>{int(total_odds)}/1</span></div>", unsafe_allow_html=True)
    else:
        st.info("Add up to 3 players to form your team.")

# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────

def render_player_profile(df):
    pid = st.session_state.profile_id
    if pid is None:
        st.warning("Select a player to view profile.")
        return
    row = df[df["id"]==pid].iloc[0]

    st.markdown(f"<h2 class='page-title'>{row['first_name']} {row['last_name']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-subtitle'>{row.get('country','—')} · Age {int(row['age'])} · {risk_badge_html(row['risk'])}</div>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="headshot-placeholder">?</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-row"><span class="label">Odds</span><span class="value">{int(row['odds'])}/1</span></div>
        <div class="stat-row"><span class="label">Value Score</span><span class="value">{row['value_score']:.3f}</span></div>
        <div class="stat-row"><span class="label">Cuts Made %</span><span class="value">{row['cuts_made_percentage']:.0f}%</span></div>
        <div class="stat-row"><span class="label">Average Round</span><span class="value">{row['avg_round']:.1f}</span></div>
        <div class="stat-row"><span class="label">Masters Wins</span><span class="value">{row['masters_wins']}</span></div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HISTORICAL DASHBOARD PAGE
# ─────────────────────────────────────────────

def render_historical(hist_odds, hist_picks, hist_winners):
    st.markdown("<h2 class='page-title'>Historical Masters Data</h2>", unsafe_allow_html=True)

    st.markdown("### Odds Trends")
    fig = px.line(hist_odds, x="Year", y="Combined_odds", color="Participant", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top Picks")
    top_picks = hist_picks.groupby("Golfer").size().sort_values(ascending=False).head(10)
    st.bar_chart(top_picks)

    st.markdown("### Previous Winners")
    st.dataframe(hist_winners)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

df_players = load_players()
hist_odds = load_historical_odds()
hist_scores = load_historical_scores()
hist_rounds = load_historical_rounds()
hist_teams = load_historical_teams()
hist_picks = load_historical_picks()
hist_winners = load_historical_winners()

filters = render_sidebar(df_players)

if st.session_state.page=="Player Picker":
    render_player_picker(df_players, filters)
elif st.session_state.page=="Player Profile":
    render_player_profile(df_players)
elif st.session_state.page=="Historical Dashboard":
    render_historical(hist_odds, hist_picks, hist_winners)
