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
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');
:root { --green:#4ade80;--green-dim:#166534;--green-glow:rgba(74,222,128,0.15);--bg:#0a0f0a;--surface:#111811;--surface2:#182018;--border:rgba(74,222,128,0.18);--text:#e8f0e8;--text-muted:#7a9a7a;--red:#f87171;--gold:#fbbf24; }
html, body, [data-testid="stAppViewContainer"] { background: var(--bg) !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }
code, .mono { font-family: 'DM Mono', monospace !important; }
[data-testid="metric-container"] { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 12px !important; }
.stButton > button { background: transparent !important; border: 1px solid var(--border) !important; color: var(--green) !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; letter-spacing: 0.05em !important; border-radius: 4px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: var(--green-glow) !important; border-color: var(--green) !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }
.stSlider > div > div > div { background: var(--green-dim) !important; }
.stSlider > div > div > div > div { background: var(--green) !important; }
.stMultiSelect > div, .stSelectbox > div { background: var(--surface2) !important; border-color: var(--border) !important; }
hr { border-color: var(--border) !important; }
.nav-pill { display: inline-block; padding: 6px 18px; border: 1px solid var(--border); border-radius: 20px; font-family: 'DM Mono', monospace; font-size: 13px; cursor: pointer; transition: all 0.2s; margin-right: 8px; }
.nav-pill.active { background: var(--green-glow); border-color: var(--green); color: var(--green); }
.player-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 16px; margin-bottom: 12px; transition: border-color 0.2s; }
.player-card:hover { border-color: var(--green); }
.player-card .name { font-family: 'Playfair Display', serif; font-size: 17px; font-weight: 700; color: var(--text); }
.player-card .sub { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--text-muted); letter-spacing: 0.06em; margin-top: 2px; }
.player-card .odds { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900; color: var(--green); }
.badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 500; }
.badge-safe { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.badge-balanced { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-high { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.team-panel { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
.team-panel.valid { border-color: #4ade80; box-shadow: 0 0 20px rgba(74,222,128,0.1); }
.team-panel.invalid { border-color: #f87171; box-shadow: 0 0 20px rgba(248,113,113,0.05); }
.section-header { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.stat-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(74,222,128,0.06); font-size: 13px; }
.stat-row .label { color: var(--text-muted); font-family: 'DM Mono', monospace; font-size: 11px; }
.stat-row .value { color: var(--text); font-weight: 500; }
.page-title { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 900; line-height: 1.1; letter-spacing: -0.01em; background: linear-gradient(135deg, #e8f0e8 0%, #4ade80 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.page-subtitle { font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-top: 4px; }
.headshot-placeholder { width: 120px; height: 120px; border-radius: 50%; background: var(--surface2); border: 2px solid var(--border); display: flex; align-items: center; justify-content: center; font-family: 'Playfair Display', serif; font-size: 36px; color: var(--text-muted); }
.scroll-container { max-height: 500px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px; }
</style>""", unsafe_allow_html=True)

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
def load_historical_odds(): return pd.read_csv("historical_odds.csv")
@st.cache_data
def load_historical_scores(): return pd.read_csv("historical_scores.csv")
@st.cache_data
def load_historical_rounds(): return pd.read_csv("historical_rounds.csv")
@st.cache_data
def load_historical_teams(): return pd.read_csv("historical_teams.csv")
@st.cache_data
def load_historical_picks(): return pd.read_csv("historical_picks.csv")
@st.cache_data
def load_historical_winners(): return pd.read_csv("historical_previous_winners.csv")

# ─────────────────────────────────────────────
# BUSINESS LOGIC
# ─────────────────────────────────────────────
def minmax(series):
    mn, mx = series.min(), series.max()
    return pd.Series([0.5]*len(series), index=series.index) if mn==mx else (series-mn)/(mx-mn)

def compute_value_scores(df):
    df = df.copy()
    for c in ["avg_round", "cuts_made_percentage", "masters_wins","rounds_under_par_percentage","best_finish_position"]:
        if c not in df: df[c]=0
    df["_n_avg_round"]=1-minmax(df["avg_round"])
    df["_n_cuts"]=minmax(df["cuts_made_percentage"])
    df["_n_wins"]=minmax(df["masters_wins"])
    df["_n_rup"]=minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"]=1-minmax(df["best_finish_position"])
    df["value_score"]=0.3*df["_n_avg_round"]+0.2*df["_n_cuts"]+0.2*df["_n_wins"]+0.15*df["_n_rup"]+0.15*df["_n_best_finish"]
    df.drop(columns=[c for c in df.columns if c.startswith("_n_")], inplace=True)
    return df

def classify_risk(odds):
    if odds<25: return "Safe"
    elif odds<=60: return "Balanced"
    return "High Risk"

def risk_badge_html(risk):
    cls={"Safe":"badge-safe","Balanced":"badge-balanced","High Risk":"badge-high"}.get(risk,"badge-safe")
    return f'<span class="badge {cls}">{risk}</span>'

def team_strength(players_df): return players_df["value_score"].sum()
def combined_odds(players_df): return players_df["odds"].sum()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    if "selected_ids" not in st.session_state: st.session_state.selected_ids=[]
    if "page" not in st.session_state: st.session_state.page="Player Picker"
    if "profile_id" not in st.session_state: st.session_state.profile_id=None
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
        pages=["Player Picker","Player Profile","Historical Dashboard"]
        for p in pages:
            active="active" if st.session_state.page==p else ""
            icon={"Player Picker":"⬜","Player Profile":"👤","Historical Dashboard":"📊"}[p]
            if st.button(f"{icon}  {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page=p
                st.rerun()
        st.markdown("---")
        # Filters (only on Player Picker)
        if st.session_state.page=="Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
            odds_min, odds_max=int(df["odds"].min()),int(df["odds"].max())
            odds_range=st.slider("Odds range", odds_min, odds_max,(odds_min, odds_max))
            age_min, age_max=int(df["age"].min()),int(df["age"].max())
            age_range=st.slider("Age range", age_min, age_max,(age_min, age_max))
            countries=sorted(df["country"].dropna().unique().tolist())
            selected_countries=st.multiselect("Country", countries)
            masters_winners_only=st.toggle("Masters winners only", value=False)
            cuts_min, cuts_max=float(df["cuts_made_percentage"].min()), float(df["cuts_made_percentage"].max())
            cuts_range=st.slider("Cuts made %", cuts_min, cuts_max,(cuts_min, cuts_max))
            return {"odds_range":odds_range,"age_range":age_range,"countries":selected_countries,"masters_winners_only":masters_winners_only,"cuts_range":cuts_range}
    return {}

# ─────────────────────────────────────────────
# PAGE RENDERING LOGIC (Player Picker, Profile, Historical)
# ─────────────────────────────────────────────
# --- (omitted here for brevity in this snippet, but it continues exactly like your original code)
# Keep your render_player_picker, render_team_panel, render_player_profile, render_historical functions exactly as in your original file.
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
