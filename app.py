import streamlit as st
import pandas as pd
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

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }
code, .mono { font-family: 'DM Mono', monospace !important; }

/* Metric cards */
[data-testid="metric-container"] { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 12px !important; }

/* Buttons */
.stButton > button { background: transparent !important; border: 1px solid var(--border) !important; color: var(--green) !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; letter-spacing: 0.05em !important; border-radius: 4px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: var(--green-glow) !important; border-color: var(--green) !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }

/* Slider */
.stSlider > div > div > div { background: var(--green-dim) !important; }
.stSlider > div > div > div > div { background: var(--green) !important; }

/* Select */
.stMultiSelect > div, .stSelectbox > div { background: var(--surface2) !important; border-color: var(--border) !important; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Player card */
.player-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 16px; margin-bottom: 12px; transition: border-color 0.2s; }
.player-card:hover { border-color: var(--green); }
.player-card .name { font-family: 'Playfair Display', serif; font-size: 17px; font-weight: 700; color: var(--text); }
.player-card .sub { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--text-muted); letter-spacing: 0.06em; margin-top: 2px; }
.player-card .odds { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900; color: var(--green); }

/* Risk badge */
.badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 500; }
.badge-safe     { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.badge-balanced { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-high     { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

/* Team panel */
.team-panel { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
.team-panel.valid   { border-color: #4ade80; box-shadow: 0 0 20px rgba(74,222,128,0.1); }
.team-panel.invalid { border-color: #f87171; box-shadow: 0 0 20px rgba(248,113,113,0.05); }

/* Section header */
.section-header { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }

/* Stat row */
.stat-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(74,222,128,0.06); font-size: 13px; }
.stat-row .label { color: var(--text-muted); font-family: 'DM Mono', monospace; font-size: 11px; }
.stat-row .value { color: var(--text); font-weight: 500; }

/* Page title */
.page-title { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 900; line-height: 1.1; letter-spacing: -0.01em; background: linear-gradient(135deg, #e8f0e8 0%, #4ade80 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.page-subtitle { font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-top: 4px; }

/* Profile headshot placeholder */
.headshot-placeholder { width: 120px; height: 120px; border-radius: 50%; background: var(--surface2); border: 2px solid var(--border); display: flex; align-items: center; justify-content: center; font-family: 'Playfair Display', serif; font-size: 36px; color: var(--text-muted); }

/* Scrollable table container */
.scroll-container { max-height: 500px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px; }
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
    needed = ["avg_round", "cuts_made_percentage", "masters_wins", "rounds_under_par_percentage", "best_finish_position"]
    for c in needed: 
        if c not in df.columns: df[c]=0
    df["_n_avg_round"] = 1 - minmax(df["avg_round"])
    df["_n_cuts"] = minmax(df["cuts_made_percentage"])
    df["_n_wins"] = minmax(df["masters_wins"])
    df["_n_rup"] = minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"] = 1 - minmax(df["best_finish_position"])
    df["value_score"] = 0.3*df["_n_avg_round"] + 0.2*df["_n_cuts"] + 0.2*df["_n_wins"] + 0.15*df["_n_rup"] + 0.15*df["_n_best_finish"]
    df.drop(columns=[c for c in df.columns if c.startswith("_n_")], inplace=True)
    return df

def classify_risk(odds):
    if odds<25: return "Safe"
    elif odds<=60: return "Balanced"
    return "High Risk"

def risk_badge_html(risk):
    cls = {"Safe":"badge-safe","Balanced":"badge-balanced","High Risk":"badge-high"}.get(risk,"badge-safe")
    return f'<span class="badge {cls}">{risk}</span>'

def team_strength(df): return df["value_score"].sum()
def combined_odds(df): return df["odds"].sum()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    for key, val in [("selected_ids", []), ("page", "Player Picker"), ("profile_id", None)]: 
        if key not in st.session_state: st.session_state[key]=val
init_state()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(df):
    with st.sidebar:
        st.markdown('<div class="page-title" style="font-size:24px;">⛳ Masters 2026</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Decision Support Tool</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
        pages = ["Player Picker","Player Profile","Historical Dashboard"]
        for p in pages:
            active = "active" if st.session_state.page==p else ""
            icon = {"Player Picker":"⬜","Player Profile":"👤","Historical Dashboard":"📊"}[p]
            if st.button(f"{icon} {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page=p; st.rerun()
        st.markdown("---")
        if st.session_state.page=="Player Picker":
            odds_min, odds_max = int(df["odds"].min()), int(df["odds"].max())
            odds_range = st.slider("Odds range", odds_min, odds_max, (odds_min, odds_max))
            age_min, age_max = int(df["age"].min()), int(df["age"].max())
            age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))
            countries = sorted(df["country"].dropna().unique().tolist())
            selected_countries = st.multiselect("Country", countries)
            masters_winners_only = st.toggle("Masters winners only", value=False)
            cuts_min, cuts_max = float(df["cuts_made_percentage"].min()), float(df["cuts_made_percentage"].max())
            cuts_range = st.slider("Cuts made %", cuts_min, cuts_max, (cuts_min, cuts_max))
            return {"odds_range":odds_range,"age_range":age_range,"countries":selected_countries,"masters_winners_only":masters_winners_only,"cuts_range":cuts_range}
    return {}

# ─────────────────────────────────────────────
# PLAYER PICKER PAGE
# ─────────────────────────────────────────────
def render_player_picker(df, filters):
    fdf = df.copy()
    fdf = fdf[fdf["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"]: fdf=fdf[fdf["country"].isin(filters["countries"])]
    if filters["masters_winners_only"]: fdf=fdf[fdf["masters_wins"]>0]
    fdf=fdf[fdf["cuts_made_percentage"].between(*filters["cuts_range"])]

    left_col, right_col = st.columns([2,1], gap="large")
    with left_col:
        st.markdown('<div class="section-header">Player Pool</div>', unsafe_allow_html=True)
        st.caption(f"{len(fdf)} players · {len(st.session_state.selected_ids)}/3 selected")
        sort_col = st.selectbox("Sort by", ["odds","value_score","age","cuts_made_percentage","masters_wins"], format_func=lambda x:x.replace("_"," ").title(), label_visibility="collapsed")
        fdf=fdf.sort_values(sort_col, ascending=(sort_col=="odds"))

        for _, row in fdf.iterrows():
            pid=row["id"]; is_selected=pid in st.session_state.selected_ids
            card_border="border-color: var(--green);" if is_selected else ""
            col_a, col_b = st.columns([4,1])
            with col_a:
                st.markdown(f"""
                <div class="player-card" style="{card_border}">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{row.get('country','—')} · Age {int(row['age'])} · {risk_badge_html(row['risk'])}</div>
                    <div style="display:flex;gap:24px;margin-top:10px;align-items:flex-end;">
                        <div><div class="sub">ODDS</div><div class="odds">{int(row['odds'])}/1</div></div>
                        <div><div class="sub">VALUE</div><div style="font-size:18px;font-family:'DM Mono';color:var(--text);">{row['value_score']:.3f}</div></div>
                        <div><div class="sub">CUTS MADE</div><div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{row['cuts_made_percentage']:.0f}%</div></div>
                        <div><div class="sub">AVG RND</div><div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{row['avg_round']:.1f}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if is_selected:
                    if st.button("✕ Remove", key=f"rem_{pid}"): st.session_state.selected_ids.remove(pid); st.rerun()
                    if st.button("Profile →", key=f"prof_{pid}"): st.session_state.profile_id=pid; st.session_state.page="Player Profile"; st.rerun()
                else:
                    disabled = len(st.session_state.selected_ids)>=3
                    if st.button("+ Add", key=f"add_{pid}", disabled=disabled): st.session_state.selected_ids.append(pid); st.rerun()

    with right_col: render_team_panel(df)

def render_team_panel(df):
    st.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)
    selected_df=df[df["id"].isin(st.session_state.selected_ids)]
    n=len(st.session_state.selected_ids)
    c_odds=combined_odds(selected_df) if n>0 else 0
    t_strength=team_strength(selected_df) if n>0 else 0
    is_valid=(n==3) and (c_odds>=150)
    panel_cls="valid" if is_valid else ("invalid" if n==3 else "")
    st.markdown(f'<div class="team-panel {panel_cls}">', unsafe_allow_html=True)
    if n==0:
        st.markdown('<div style="color:var(--text-muted);font-family:\'DM Mono\';font-size:12px;text-align:center;padding:20px 0;">Select 3 golfers to build your team</div>', unsafe_allow_html=True)
    else:
        for _, row in selected_df.iterrows():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);">
                <div><div style="font-family:'Playfair Display';font-size:14px;font-weight:700;">{row['first_name']} {row['last_name']}</div>
                <div style="font-family:'DM Mono';font-size:11px;color:var(--text-muted);">{row.get('country','—')}</div></div>
                <div style="font-family:'Playfair Display';font-size:16px;font-weight:900;color:var(--green);">{int(row['odds'])}/1</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:12px;font-family:DM Mono;font-size:12px;color:var(--text-muted);'>Combined Odds: {int(c_odds)} · Team Value: {t_strength:.3f}</div>", unsafe_allow_html=True)
        if not is_valid: st.markdown(f"<div style='margin-top:6px;font-family:DM Mono;font-size:12px;color:var(--red);'>Team invalid: must have 3 players and combined odds ≥150</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────
def render_player_profile(df, historical_scores, historical_rounds, historical_winners):
    pid=st.session_state.profile_id
    if pid is None: st.warning("No player selected"); return
    player=df[df["id"]==pid].iloc[0]

    left_col, right_col = st.columns([2,1], gap="large")
    with left_col:
        st.markdown(f'<div class="page-title">{player["first_name"]} {player["last_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">{player.get("country","—")} · Age {int(player["age"])} · Odds: {int(player["odds"])}/1</div>', unsafe_allow_html=True)
        # Headshot
        img_path=f'images/{player["id"]}.jpg'
        if os.path.exists(img_path): st.image(img_path, width=120)
        else: st.markdown(f'<div class="headshot-placeholder">{player["first_name"][0]}{player["last_name"][0]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Stats & Career</div>', unsafe_allow_html=True)
        stats = {
            "Masters Wins": player.get("masters_wins",0),
            "Best Finish": player.get("best_finish","—"),
            "Best Finish Position": player.get("best_finish_position","—"),
            "Avg Round": player.get("avg_round","—"),
            "Low Round": player.get("low_round","—"),
            "High Round": player.get("high_round","—"),
            "Rounds Under Par %": f'{player.get("rounds_under_par_percentage",0):.0f}%',
            "Cuts Made %": f'{player.get("cuts_made_percentage",0):.0f}%',
            "Tournaments Played": player.get("tournaments_played","—"),
            "Money Earned": player.get("money_earned","—")
        }
        for k,v in stats.items(): st.markdown(f'<div class="stat-row"><div class="label">{k}</div><div class="value">{v}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Historical Masters Performance</div>', unsafe_allow_html=True)
        past_wins = historical_winners[historical_winners["Golfer"]==player["display_name"]] if not historical_winners.empty else pd.DataFrame()
        if not past_wins.empty: st.dataframe(past_wins)
        else: st.markdown('<div style="color:var(--text-muted);font-family:DM Mono;font-size:12px;">No historical wins data available</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-header">Advanced Insights</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-row"><div class="label">Value Score</div><div class="value">{player["value_score"]:.3f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-row"><div class="label">Risk</div><div class="value">{player["risk"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-row"><div class="label">Implied Probability</div><div class="value">{player["implied_prob"]:.2%}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HISTORICAL DASHBOARD PAGE
# ─────────────────────────────────────────────
def render_historical_dashboard(historical_scores, historical_rounds, historical_odds):
    st.markdown('<div class="page-title">Historical Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Past tournament insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Top 10 Past Performers by Score</div>', unsafe_allow_html=True)
    if not historical_scores.empty:
        top10 = historical_scores.groupby("Golfer")["Score"].mean().nsmallest(10).reset_index()
        st.dataframe(top10)
    else: st.markdown('<div style="color:var(--text-muted);font-family:DM Mono;font-size:12px;">No historical scores data</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    df = load_players()
    hist_odds = load_historical_odds()
    hist_scores = load_historical_scores()
    hist_rounds = load_historical_rounds()
    hist_teams = load_historical_teams()
    hist_picks = load_historical_picks()
    hist_winners = load_historical_winners()

    filters = render_sidebar(df)

    if st.session_state.page=="Player Picker": render_player_picker(df, filters)
    elif st.session_state.page=="Player Profile": render_player_profile(df, hist_scores, hist_rounds, hist_winners)
    elif st.session_state.page=="Historical Dashboard": render_historical_dashboard(hist_scores, hist_rounds, hist_odds)

if __name__=="__main__":
    main()
