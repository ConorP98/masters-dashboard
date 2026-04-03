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

[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

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

[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stSlider > div > div > div {
    background: var(--green-dim) !important;
}
.stSlider > div > div > div > div {
    background: var(--green) !important;
}

.stMultiSelect > div, .stSelectbox > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

hr { border-color: var(--border) !important; }

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

.team-panel {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
}
.team-panel.valid   { border-color: #4ade80; box-shadow: 0 0 20px rgba(74,222,128,0.1); }
.team-panel.invalid { border-color: #f87171; box-shadow: 0 0 20px rgba(248,113,113,0.05); }

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

.scroll-container {
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
}

/* ── Mobile: show team panel at top, hide the desktop column copy ── */
@media (max-width: 768px) {
    .mobile-team-top { display: block !important; }
    .desktop-team-only { display: none !important; }
}
@media (min-width: 769px) {
    .mobile-team-top { display: none !important; }
    .desktop-team-only { display: block !important; }
}


/* Profile bio card */
.bio-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
}

/* Info grid */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}
.info-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 14px;
}
.info-item .ilabel {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.info-item .ivalue {
    font-family: 'DM Mono', monospace;
    font-size: 15px;
    font-weight: 500;
    color: var(--text);
}
.info-item .ivalue.highlight {
    color: var(--green);
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 900;
}

/* Suggestion card */
.suggest-card {
    background: var(--surface2);
    border: 1px solid rgba(74,222,128,0.12);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.suggest-card .sname {
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    font-weight: 700;
}
.suggest-card .smeta {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

@st.cache_data
def get_available_images():
    if not os.path.isdir("images"):
        return set()
    return {os.path.splitext(f)[0] for f in os.listdir("images") if f.lower().endswith(".jpg")}

@st.cache_data
def load_players():
    df = pd.read_csv("consolidated_player_data_2026.csv")
    # Fix decimal percentages (values <= 1 are decimals, multiply by 100)
    pct_cols = [c for c in df.columns if "percentage" in c.lower() or c.lower().endswith("_pct")]
    for col in pct_cols:
        if col in df.columns and df[col].dropna().max() <= 1.0:
            df[col] = df[col] * 100
    # Remove withdrawn players
    df = df[~((df["first_name"].str.lower() == "phil") & (df["last_name"].str.lower() == "mickelson"))]
    df = compute_value_scores(df)
    df["risk"] = df["odds"].apply(classify_risk)
    df["implied_prob"] = 1 / (df["odds"] + 1)
    return df

@st.cache_data
def load_historical_odds():
    path = "historical_odds.csv"
    if not os.path.exists(path):
        st.warning(f"⚠️ {path} not found.")
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_historical_scores():
    path = "historical_scores.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_historical_rounds():
    path = "historical_rounds.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_historical_teams():
    path = "historical_teams.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_historical_picks():
    path = "historical_picks.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_historical_winners():
    path = "historical_previous_winners.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

# ─────────────────────────────────────────────
# BUSINESS LOGIC
# ─────────────────────────────────────────────

def minmax(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - mn) / (mx - mn)

def minmax_val(val, series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return 0.5
    return (val - mn) / (mx - mn)

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

# Sort direction map: True = ascending is "better first"
SORT_ASC = {
    "odds":                      True,
    "age":                       True,
    "avg_round":                 True,
    "value_score":               False,
    "cuts_made_percentage":      False,
    "masters_wins":              False,
    "rounds_under_par_percentage": False,
}

def suggest_completions(df, selected_ids, top_n=5):
    """Suggest best players to complete a valid team."""
    selected_df = df[df["id"].isin(selected_ids)]
    n = len(selected_ids)
    current_odds = selected_df["odds"].sum() if n > 0 else 0
    slots_remaining = 3 - n
    candidates = df[~df["id"].isin(selected_ids)].copy()

    if slots_remaining == 1:
        needed = max(0, 150 - current_odds)
        candidates = candidates[candidates["odds"] >= needed]
    elif slots_remaining == 2:
        # Must be possible to reach 150 with 2 picks; rough filter: each pick avg >= half remaining
        needed_total = max(0, 150 - current_odds)
        candidates = candidates[candidates["odds"] >= needed_total * 0.3]

    return candidates.sort_values("odds", ascending=True).head(top_n)

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
    # Persist filter values
    if "filter_odds_range" not in st.session_state:
        st.session_state.filter_odds_range = None
    if "filter_age_range" not in st.session_state:
        st.session_state.filter_age_range = None
    if "filter_countries" not in st.session_state:
        st.session_state.filter_countries = []
    if "filter_masters_winners_only" not in st.session_state:
        st.session_state.filter_masters_winners_only = False
    if "filter_cuts_range" not in st.session_state:
        st.session_state.filter_cuts_range = None

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
        pages = ["Player Picker", "Player Profile", "Historical Dashboard"]
        for p in pages:
            active = "active" if st.session_state.page == p else ""
            icon = {"Player Picker": "⬜", "Player Profile": "👤", "Historical Dashboard": "📊"}[p]
            if st.button(f"{icon}  {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()

        st.markdown("---")

        if st.session_state.page == "Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)

            odds_min, odds_max = int(df["odds"].min()), int(df["odds"].max())
            if st.session_state.filter_odds_range is None:
                st.session_state.filter_odds_range = (odds_min, odds_max)
            odds_range = st.slider("Odds range", odds_min, odds_max,
                                   st.session_state.filter_odds_range, key="odds_slider")
            st.session_state.filter_odds_range = odds_range

            age_min, age_max = int(df["age"].min()), int(df["age"].max())
            if st.session_state.filter_age_range is None:
                st.session_state.filter_age_range = (age_min, age_max)
            age_range = st.slider("Age range", age_min, age_max,
                                  st.session_state.filter_age_range, key="age_slider")
            st.session_state.filter_age_range = age_range

            countries = sorted(df["country"].dropna().unique().tolist())
            selected_countries = st.multiselect("Country", countries,
                                                default=st.session_state.filter_countries,
                                                key="country_select")
            st.session_state.filter_countries = selected_countries

            masters_winners_only = st.toggle("Masters winners only",
                                             value=st.session_state.filter_masters_winners_only,
                                             key="winners_toggle")
            st.session_state.filter_masters_winners_only = masters_winners_only

            cuts_min = float(df["cuts_made_percentage"].min())
            cuts_max = float(df["cuts_made_percentage"].max())
            if st.session_state.filter_cuts_range is None:
                st.session_state.filter_cuts_range = (cuts_min, cuts_max)
            cuts_range = st.slider("Cuts made %", cuts_min, cuts_max,
                                   st.session_state.filter_cuts_range, key="cuts_slider")
            st.session_state.filter_cuts_range = cuts_range

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
    fdf = df.copy()
    fdf = fdf[fdf["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"]:
        fdf = fdf[fdf["country"].isin(filters["countries"])]
    if filters["masters_winners_only"]:
        fdf = fdf[fdf["masters_wins"] > 0]
    fdf = fdf[fdf["cuts_made_percentage"].between(*filters["cuts_range"])]

    # ── Mobile: team panel at top (hidden on desktop via CSS) ──
    st.markdown('<div class="mobile-team-top">', unsafe_allow_html=True)
    render_team_panel(df)
    st.markdown('</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        st.markdown('<div class="section-header">Player Pool</div>', unsafe_allow_html=True)
        st.caption(f"{len(fdf)} players · {len(st.session_state.selected_ids)}/3 selected")

        sort_col = st.selectbox(
            "Sort by",
            list(SORT_ASC.keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            label_visibility="collapsed",
        )
        if sort_col == "avg_round":
            # Rookies (avg_round == 0) always go to the bottom
            rookies = fdf[fdf["avg_round"] == 0]
            non_rookies = fdf[fdf["avg_round"] != 0].sort_values("avg_round", ascending=True)
            fdf = pd.concat([non_rookies, rookies])
        else:
            fdf = fdf.sort_values(sort_col, ascending=SORT_ASC.get(sort_col, True))

        for _, row in fdf.iterrows():
            pid = row["id"]
            is_selected = pid in st.session_state.selected_ids
            card_border = "border-color: var(--green);" if is_selected else ""

            col_a, col_b = st.columns([4, 1])
            with col_a:
                best = int(row.get("best_finish_position", 0))
                best_str = str(best) if best > 0 else "Rookie"
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
                    if st.button("Profile →", key=f"prof_{pid}"):
                        st.session_state.profile_id = pid
                        st.session_state.page = "Player Profile"
                        st.rerun()
                else:
                    disabled = len(st.session_state.selected_ids) >= 3
                    if st.button("+ Add", key=f"add_{pid}", disabled=disabled):
                        st.session_state.selected_ids.append(pid)
                        st.rerun()

    with right_col:
        st.markdown('<div class="desktop-team-only">', unsafe_allow_html=True)
        render_team_panel(df)
        st.markdown('</div>', unsafe_allow_html=True)


def render_team_panel(df):
    st.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)

    selected_df = df[df["id"].isin(st.session_state.selected_ids)]
    n = len(st.session_state.selected_ids)
    c_odds = combined_odds(selected_df) if n > 0 else 0
    t_strength = team_strength(selected_df) if n > 0 else 0
    is_valid = (n == 3) and (c_odds >= 150)
    panel_cls = "valid" if is_valid else ("invalid" if n == 3 else "")

    st.markdown(f'<div class="team-panel {panel_cls}">', unsafe_allow_html=True)

    if n == 0:
        st.markdown('<div style="color:var(--text-muted);font-family:\'DM Mono\';font-size:12px;text-align:center;padding:20px 0;">Select 3 golfers to build your team</div>', unsafe_allow_html=True)
    else:
        # Each selected player row with inline ✕ remove button
        for _, row in selected_df.iterrows():
            pid = row["id"]
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div style="padding:8px 0;border-bottom:1px solid var(--border);">
                    <div style="font-family:'Playfair Display';font-size:14px;font-weight:700;">
                        {row['first_name']} {row['last_name']}
                    </div>
                    <div style="font-family:'DM Mono';font-size:10px;color:var(--text-muted);">
                        {risk_badge_html(row['risk'])} &nbsp; {int(row['odds'])}/1 &nbsp; score: {row['value_score']:.3f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("✕", key=f"panel_rem_{pid}", help=f"Remove {row['first_name']} {row['last_name']}"):
                    st.session_state.selected_ids.remove(pid)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        odds_color = "#4ade80" if c_odds >= 150 else "#f87171"
        st.markdown(f"""
        <div class="stat-row">
            <span class="label">COMBINED ODDS</span>
            <span class="value" style="color:{odds_color};font-family:'Playfair Display';font-size:20px;font-weight:900;">
                {int(c_odds)}
            </span>
        </div>
        <div class="stat-row">
            <span class="label">TEAM STRENGTH</span>
            <span class="value" style="font-family:'DM Mono';">{t_strength:.3f}</span>
        </div>
        <div class="stat-row">
            <span class="label">SLOTS FILLED</span>
            <span class="value" style="font-family:'DM Mono';">{n} / 3</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if n == 3 and not is_valid:
            st.markdown("""
            <div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.3);
                        border-radius:6px;padding:10px;font-family:'DM Mono';font-size:11px;color:#f87171;">
                ⚠ Combined odds must be ≥ 150 for a valid entry.
            </div>
            """, unsafe_allow_html=True)
        elif is_valid:
            st.markdown("""
            <div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.3);
                        border-radius:6px;padding:10px;font-family:'DM Mono';font-size:11px;color:#4ade80;">
                ✓ Valid team — ready to submit.
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="margin-top:10px;text-align:center;">
                <a href="https://eoghanobrien-bit.github.io/masters-sweepstake/"
                   target="_blank"
                   style="display:inline-block;padding:10px 20px;
                          background:rgba(74,222,128,0.12);
                          border:1px solid rgba(74,222,128,0.5);
                          border-radius:6px;
                          font-family:'DM Mono';font-size:12px;
                          color:#4ade80;text-decoration:none;
                          letter-spacing:0.06em;">
                    ⛳ Submit your team →
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Smart completion suggestions
    if 0 < n < 3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Suggested Additions</div>', unsafe_allow_html=True)
        suggestions = suggest_completions(df, st.session_state.selected_ids)
        if suggestions.empty:
            st.caption("No valid completions found with current odds.")
        else:
            for _, srow in suggestions.iterrows():
                spid = srow["id"]
                sc1, sc2 = st.columns([4, 1])
                with sc1:
                    st.markdown(f"""
                    <div class="suggest-card">
                        <div>
                            <div class="sname">{srow['first_name']} {srow['last_name']}</div>
                            <div class="smeta">{int(srow['odds'])}/1 · score {srow['value_score']:.3f} · {risk_badge_html(srow['risk'])}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with sc2:
                    if st.button("+ Add", key=f"sug_{spid}"):
                        st.session_state.selected_ids.append(spid)
                        st.rerun()

    if n > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear team", use_container_width=True):
            st.session_state.selected_ids = []
            st.rerun()


# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────

def render_player_profile(df, available_images):
    player_options = df.apply(lambda r: f"{r['first_name']} {r['last_name']}", axis=1).tolist()
    player_ids = df["id"].tolist()

    default_idx = 0
    if st.session_state.profile_id in player_ids:
        default_idx = player_ids.index(st.session_state.profile_id)

    chosen_label = st.selectbox("Select player", player_options, index=default_idx)
    chosen_idx = player_options.index(chosen_label)
    row = df.iloc[chosen_idx]
    st.session_state.profile_id = row["id"]

    st.markdown("---")

    # ── Top section: photo + identity + add/remove ──
    top_left, top_mid, top_right = st.columns([1, 2, 1], gap="large")

    with top_left:
        img_key = f"{row['first_name']} {row['last_name']}"
        if img_key in available_images:
            st.image(f"images/{img_key}.jpg", width=180)
        else:
            initials = f"{row['first_name'][0]}{row['last_name'][0]}"
            st.markdown(f"""
            <div style="width:120px;height:120px;border-radius:50%;
                        background:var(--surface2);border:2px solid var(--border);
                        display:flex;align-items:center;justify-content:center;
                        font-family:'Playfair Display';font-size:36px;color:var(--text-muted);">
                {initials}
            </div>
            """, unsafe_allow_html=True)

    with top_mid:
        _world_rank = f" &nbsp;·&nbsp; World Rank #{int(row['world_ranking'])}" if pd.notna(row.get('world_ranking')) else ""
        _bio_val = str(row.get('overview', row.get('bio', '')))
        _bio_html = f'<div style="font-family:DM Sans;font-size:13px;color:var(--text-muted);margin-top:10px;line-height:1.5;">{_bio_val}</div>' if _bio_val not in ['', 'nan', 'None'] else ''
        _badge = risk_badge_html(row['risk'])
        st.markdown(f"""
        <div style="padding-top: 8px;">
            <div style="font-family:'Playfair Display';font-size:32px;font-weight:900;line-height:1.1;">
                {row['first_name']} {row['last_name']}
            </div>
            <div style="font-family:'DM Mono';font-size:11px;color:var(--text-muted);margin-top:6px;letter-spacing:0.08em;">
                {row.get('country','—')} &nbsp;·&nbsp; Age {int(row['age'])}{_world_rank}
            </div>
            <div style="margin-top:10px;">
                {_badge}
                <span style="font-family:'Playfair Display';font-size:28px;font-weight:900;color:var(--green);margin-left:16px;">{int(row['odds'])}/1</span>
            </div>
            {_bio_html}
        </div>
        """, unsafe_allow_html=True)

    with top_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if row["id"] not in st.session_state.selected_ids:
            if len(st.session_state.selected_ids) < 3:
                if st.button("+ Add to team", use_container_width=True, key="prof_add"):
                    st.session_state.selected_ids.append(row["id"])
                    st.rerun()
            else:
                st.button("Team full", use_container_width=True, disabled=True)
        else:
            if st.button("✕ Remove from team", use_container_width=True, key="prof_rem"):
                st.session_state.selected_ids.remove(row["id"])
                st.rerun()

    st.markdown("---")

    # ── Tabbed sections ──
    tab_overview, tab_stats, tab_masters, tab_radar = st.tabs(
        ["📋 Overview", "📊 Career Stats", "🏆 Masters Record", "🎯 Radar"]
    )

    with tab_overview:
        _render_profile_overview(row, df)

    with tab_stats:
        _render_profile_stats(row, df)

    with tab_masters:
        _render_profile_masters(row, df)

    with tab_radar:
        _render_profile_radar(row, df)


def _safe(row, col, default="—"):
    val = row.get(col, default)
    if pd.isna(val) if not isinstance(val, str) else val in ("", "nan"):
        return default
    return val


def _render_profile_overview(row, df):
    """Key facts, rankings, odds context."""
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-header">Player Overview</div>', unsafe_allow_html=True)

        # Build info grid items dynamically based on available columns
        grid_items = []
        if pd.notna(row.get("world_ranking")):
            grid_items.append(("WORLD RANKING", f"#{int(row['world_ranking'])}", True))
        if pd.notna(row.get("fedex_rank")):
            grid_items.append(("FEDEX RANK", f"#{int(row['fedex_rank'])}", False))
        if pd.notna(row.get("age")):
            grid_items.append(("AGE", str(int(row["age"])), False))
        if pd.notna(row.get("turned_pro")):
            grid_items.append(("TURNED PRO", str(int(row["turned_pro"])), False))
        if pd.notna(row.get("country")):
            grid_items.append(("COUNTRY", str(row["country"]), False))
        if pd.notna(row.get("college")):
            grid_items.append(("COLLEGE", str(row["college"]), False))

        html_items = ""
        for label, val, highlight in grid_items:
            cls = "highlight" if highlight else ""
            html_items += f"""
            <div class="info-item">
                <div class="ilabel">{label}</div>
                <div class="ivalue {cls}">{val}</div>
            </div>"""

        if html_items:
            st.markdown(f'<div class="info-grid">{html_items}</div>', unsafe_allow_html=True)

        # Implied probability and odds context
        implied = row["implied_prob"] * 100
        st.markdown(f"""
        <div class="bio-card" style="margin-top:8px;">
            <div class="section-header" style="border:none;margin-bottom:6px;">ODDS CONTEXT</div>
            <div style="display:flex;gap:20px;flex-wrap:wrap;">
                <div>
                    <div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">ODDS</div>
                    <div style="font-family:'Playfair Display';font-size:24px;font-weight:900;color:var(--green);">{int(row['odds'])}/1</div>
                </div>
                <div>
                    <div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">IMPLIED PROB</div>
                    <div style="font-family:'DM Mono';font-size:20px;font-weight:500;">{implied:.1f}%</div>
                </div>
                <div>
                    <div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">VALUE SCORE</div>
                    <div style="font-family:'DM Mono';font-size:20px;font-weight:500;">{row['value_score']:.3f}</div>
                </div>
                <div>
                    <div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">RISK TIER</div>
                    <div style="margin-top:4px;">{risk_badge_html(row['risk'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
        overview_text = str(row.get('overview', row.get('bio', '')))
        if overview_text not in ['', 'nan', 'None']:
            st.markdown(f'''
            <div class="bio-card" style="line-height:1.7;font-size:14px;color:var(--text-muted);">
                {overview_text}
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("No biography available for this player.")


def _render_profile_stats(row, df):
    """Full career stats panel."""
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-header">Masters at Augusta</div>', unsafe_allow_html=True)
        masters_fields = [
            ("masters_appearances", "Appearances"),
            ("masters_wins", "Wins"),
            ("cuts_made_percentage", "Cuts Made %"),
            ("avg_round", "Avg Round Score"),
            ("rounds_under_par_percentage", "Rounds Under Par %"),
            ("best_finish_position", "Best Finish"),
            ("avg_finish_position", "Avg Finish Position"),
            ("total_rounds_played", "Total Rounds Played"),
        ]
        for col_name, label in masters_fields:
            val = row.get(col_name)
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                if col_name == "best_finish_position":
                    bv = int(val)
                    display_val = str(bv) if bv > 0 else "Rookie"
                elif "percentage" in col_name:
                    display_val = f"{val:.1f}%"
                elif "avg_round" in col_name:
                    display_val = f"{val:.2f}"
                elif isinstance(val, float):
                    display_val = f"{val:.2f}"
                else:
                    display_val = str(int(val))
                st.markdown(f"""
                <div class="stat-row">
                    <span class="label">{label.upper()}</span>
                    <span class="value" style="font-family:'DM Mono';">{display_val}</span>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Career Overview</div>', unsafe_allow_html=True)
        career_fields = [
            ("pga_wins", "PGA Tour Wins"),
            ("major_wins", "Major Wins"),
            ("career_earnings", "Career Earnings ($)"),
            ("career_top10s", "Career Top 10s"),
            ("career_cuts_made", "Career Cuts Made"),
            ("career_events", "Career Events"),
            ("career_scoring_avg", "Career Scoring Avg"),
            ("weeks_at_world_number_1", "Weeks at World #1"),
        ]
        for col_name, label in career_fields:
            val = row.get(col_name)
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                if "earnings" in col_name and isinstance(val, (int, float)):
                    display_val = f"${val:,.0f}"
                elif isinstance(val, float):
                    display_val = f"{val:.2f}"
                else:
                    display_val = str(int(val))
                st.markdown(f"""
                <div class="stat-row">
                    <span class="label">{label.upper()}</span>
                    <span class="value" style="font-family:'DM Mono';">{display_val}</span>
                </div>
                """, unsafe_allow_html=True)

    # Odds vs field context chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Odds vs Field</div>', unsafe_allow_html=True)
    fig = go.Figure()
    # Distribution of all player odds
    fig.add_trace(go.Histogram(
        x=df["odds"],
        nbinsx=25,
        marker_color="rgba(74,222,128,0.25)",
        marker_line_color="rgba(74,222,128,0.5)",
        marker_line_width=1,
        name="Field",
    ))
    # This player's odds
    fig.add_vline(
        x=row["odds"],
        line_color="#4ade80",
        line_width=2,
        line_dash="dash",
        annotation_text=f"{row['first_name']} {row['last_name']} ({int(row['odds'])}/1)",
        annotation_font_color="#4ade80",
        annotation_font_size=11,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,17,0.4)",
        font=dict(family="DM Sans", color="#e8f0e8", size=11),
        xaxis=dict(title="Odds", gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
        yaxis=dict(title="# Players", gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
        margin=dict(l=40, r=20, t=30, b=40),
        height=260,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_profile_masters(row, df):
    """Masters-specific record and historical context."""
    st.markdown('<div class="section-header">Augusta National Record</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    metrics = [
        ("Masters Wins", "masters_wins", int),
        ("Appearances", "masters_appearances", int),
        ("Best Finish", "best_finish_position", lambda v: str(int(v)) if int(v) > 0 else "Rookie"),
        ("Cuts Made %", "cuts_made_percentage", lambda v: f"{v:.0f}%"),
        ("Avg Round", "avg_round", lambda v: f"{v:.2f}"),
        ("Rounds Under Par %", "rounds_under_par_percentage", lambda v: f"{v:.0f}%"),
    ]

    for i, (label, col_name, fmt) in enumerate(metrics):
        col = [col1, col2, col3][i % 3]
        val = row.get(col_name)
        if val is not None and not (isinstance(val, float) and np.isnan(val)):
            with col:
                display = fmt(val)
                st.metric(label, display)



def _render_profile_radar(row, df):
    """Performance radar using _norm columns, with optional player comparison."""
    norm_cols = [c for c in df.columns if c.endswith("_norm")]
    if not norm_cols:
        st.info("No normalised (_norm) columns found in player data.")
        return

    # Comparison player selector
    player_options = ["Field Average"] + df.apply(lambda r: f"{r['first_name']} {r['last_name']}", axis=1).tolist()
    compare_label = st.selectbox(
        "Compare against",
        player_options,
        index=0,
        key="radar_compare",
    )

    labels = [c.replace("_norm", "").replace("_", " ").title() for c in norm_cols]
    values = [row[c] for c in norm_cols]
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    if compare_label == "Field Average":
        compare_vals = [df[c].mean() for c in norm_cols]
        compare_name = "Field Average"
        compare_color = "#fbbf24"
        compare_fill = "rgba(251,191,36,0.06)"
    else:
        compare_row = df[df.apply(lambda r: f"{r['first_name']} {r['last_name']}" == compare_label, axis=1)].iloc[0]
        compare_vals = [compare_row[c] for c in norm_cols]
        compare_name = compare_label
        compare_color = "#f87171"
        compare_fill = "rgba(248,113,113,0.06)"

    compare_closed = compare_vals + [compare_vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=compare_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor=compare_fill,
        line=dict(color=compare_color, width=1.5, dash="dot"),
        name=compare_name,
    ))
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(74,222,128,0.12)",
        line=dict(color="#4ade80", width=2),
        marker=dict(color="#4ade80", size=5),
        name=f"{row['first_name']} {row['last_name']}",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(17,24,17,0)",
            radialaxis=dict(
                visible=True, range=[0, 1],
                gridcolor="rgba(74,222,128,0.15)",
                linecolor="rgba(74,222,128,0.15)",
                tickfont=dict(color="#7a9a7a", size=9, family="DM Mono"),
            ),
            angularaxis=dict(
                gridcolor="rgba(74,222,128,0.12)",
                linecolor="rgba(74,222,128,0.12)",
                tickfont=dict(color="#e8f0e8", size=10, family="DM Sans"),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=40, b=40),
        height=480,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8f0e8", size=10)),
    )
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
# HISTORICAL DASHBOARD PAGE
# ─────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,24,17,0.4)",
    font=dict(family="DM Sans", color="#e8f0e8", size=11),
    xaxis=dict(gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
    yaxis=dict(gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
    margin=dict(l=40, r=20, t=40, b=40),
)


def render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams):
    st.markdown('<div class="section-header">Historical Dashboard</div>', unsafe_allow_html=True)

    row1_l, row1_r = st.columns(2, gap="large")

    # 1. Most picked golfers
    with row1_l:
        st.markdown("**Most Picked Golfers**")
        if not hist_picks.empty and "num_picks" in hist_picks.columns:
            picks_agg = (
                hist_picks.groupby(["first", "last"], as_index=False)["num_picks"]
                .sum()
                .sort_values("num_picks", ascending=False)
                .head(15)
            )
            picks_agg["name"] = picks_agg["first"] + " " + picks_agg["last"]
            fig = go.Figure(go.Bar(
                x=picks_agg["num_picks"],
                y=picks_agg["name"],
                orientation="h",
                marker=dict(
                    color=picks_agg["num_picks"],
                    colorscale=[[0, "#166534"], [1, "#4ade80"]],
                    showscale=False,
                ),
            ))
            fig.update_layout(**CHART_LAYOUT, height=380,
                              yaxis=dict(autorange="reversed", gridcolor="rgba(74,222,128,0.08)"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No picks data available.")

    # 2. Avg combined odds per year
    with row1_r:
        st.markdown("**Average Combined Odds by Year**")
        if not hist_odds.empty and "combined_odds" in hist_odds.columns and "year" in hist_odds.columns:
            odds_by_year = (
                hist_odds.groupby("year", as_index=False)["combined_odds"]
                .mean()
                .sort_values("year")
            )
            fig = go.Figure(go.Scatter(
                x=odds_by_year["year"],
                y=odds_by_year["combined_odds"],
                mode="lines+markers",
                line=dict(color="#4ade80", width=2.5),
                marker=dict(color="#4ade80", size=7, line=dict(color="#0a0f0a", width=2)),
                fill="tozeroy",
                fillcolor="rgba(74,222,128,0.07)",
            ))
            fig.update_layout(**CHART_LAYOUT, height=380)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No odds data available.")

    st.markdown("---")
    row2_l, row2_r = st.columns(2, gap="large")

    # 3. Combined odds vs position scatter
    with row2_l:
        st.markdown("**Combined Odds vs Finishing Position**")
        if not hist_odds.empty and "combined_odds" in hist_odds.columns and "position" in hist_odds.columns:
            scatter_df = hist_odds.dropna(subset=["combined_odds", "position"]).copy()
            scatter_df["position"] = pd.to_numeric(scatter_df["position"], errors="coerce")
            scatter_df = scatter_df.dropna(subset=["position"])
            fig = go.Figure(go.Scatter(
                x=scatter_df["combined_odds"],
                y=scatter_df["position"],
                mode="markers",
                marker=dict(
                    color=scatter_df["combined_odds"],
                    colorscale=[[0, "#166534"], [1, "#4ade80"]],
                    size=8, opacity=0.7,
                    line=dict(color="#0a0f0a", width=1),
                ),
                text=scatter_df.get("participant", None),
                hovertemplate="<b>%{text}</b><br>Odds: %{x}<br>Position: %{y}<extra></extra>",
            ))
            fig.update_layout(**CHART_LAYOUT, height=340,
                              xaxis_title="Combined Odds",
                              yaxis_title="Position",
                              yaxis=dict(autorange="reversed", gridcolor="rgba(74,222,128,0.08)"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No odds/position data.")

    # 4. Previous winners table
    with row2_r:
        st.markdown("**Previous Masters Winners**")
        if not hist_winners.empty:
            show_cols = [c for c in ["year", "full_name", "participant"] if c in hist_winners.columns]
            winners_sorted = hist_winners[show_cols].sort_values("year", ascending=False)
            st.dataframe(
                winners_sorted.reset_index(drop=True),
                use_container_width=True,
                height=340,
                column_config={
                    "year":        st.column_config.NumberColumn("Year", format="%d"),
                    "full_name":   st.column_config.TextColumn("Winner"),
                    "participant": st.column_config.TextColumn("Entered By"),
                },
                hide_index=True,
            )
        else:
            st.info("No winners data.")

    # ── NEW: hist_rounds — Score distribution by year ──
    if not hist_rounds.empty:
        st.markdown("---")
        st.markdown("**Round Score Distribution by Year**")
        score_col = next((c for c in ["score", "round_score", "total"] if c in hist_rounds.columns), None)
        year_col = "year" if "year" in hist_rounds.columns else None
        if score_col and year_col:
            fig = go.Figure()
            years = sorted(hist_rounds[year_col].dropna().unique())
            green_shades = [f"rgba(74,222,128,{0.3 + 0.7*i/max(len(years)-1,1):.2f})" for i in range(len(years))]
            for i, yr in enumerate(years):
                yr_data = hist_rounds[hist_rounds[year_col] == yr][score_col].dropna()
                fig.add_trace(go.Box(
                    y=yr_data, name=str(int(yr)),
                    marker_color=green_shades[i],
                    line_color=green_shades[i],
                    fillcolor=f"rgba(74,222,128,{0.08 + 0.1*i/max(len(years)-1,1):.2f})",
                ))
            fig.update_layout(**CHART_LAYOUT, height=320,
                              yaxis_title="Round Score",
                              xaxis_title="Year",
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # ── NEW: hist_scores — Player consistency across years ──
    if not hist_scores.empty:
        st.markdown("---")
        row3_l, row3_r = st.columns(2, gap="large")

        with row3_l:
            st.markdown("**Top Players by Avg Score (All Years)**")
            score_col = next((c for c in ["total_score", "score", "avg_score"] if c in hist_scores.columns), None)
            name_col = next((c for c in ["full_name", "player", "name"] if c in hist_scores.columns), None)
            if score_col and name_col:
                agg = (
                    hist_scores.groupby(name_col, as_index=False)[score_col]
                    .mean()
                    .sort_values(score_col)
                    .head(12)
                )
                fig = go.Figure(go.Bar(
                    x=agg[score_col], y=agg[name_col],
                    orientation="h",
                    marker=dict(color="#4ade80", opacity=0.8),
                ))
                fig.update_layout(**CHART_LAYOUT, height=340,
                                  xaxis_title="Avg Score",
                                  yaxis=dict(autorange="reversed", gridcolor="rgba(74,222,128,0.08)"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Expected score/name columns not found in historical_scores.csv.")

        with row3_r:
            st.markdown("**Score Trends Over Years**")
            year_col = "year" if "year" in hist_scores.columns else None
            if score_col and year_col:
                yearly_avg = (
                    hist_scores.groupby(year_col, as_index=False)[score_col]
                    .mean()
                    .sort_values(year_col)
                )
                fig = go.Figure(go.Scatter(
                    x=yearly_avg[year_col], y=yearly_avg[score_col],
                    mode="lines+markers",
                    line=dict(color="#fbbf24", width=2.5),
                    marker=dict(color="#fbbf24", size=7, line=dict(color="#0a0f0a", width=2)),
                    fill="tozeroy",
                    fillcolor="rgba(251,191,36,0.06)",
                ))
                fig.update_layout(**CHART_LAYOUT, height=340,
                                  xaxis_title="Year",
                                  yaxis_title="Avg Score")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Year/score columns not found in historical_scores.csv.")

    # ── NEW: hist_teams — Team score vs position analysis ──
    if not hist_teams.empty:
        st.markdown("---")
        st.markdown("**Team Score vs Position (Does Value Score Predict Results?)**")
        score_col = next((c for c in ["team_score", "total_score", "combined_score"] if c in hist_teams.columns), None)
        pos_col = next((c for c in ["position", "finishing_position", "rank"] if c in hist_teams.columns), None)
        participant_col = next((c for c in ["participant", "name", "player"] if c in hist_teams.columns), None)
        year_col = "year" if "year" in hist_teams.columns else None

        if score_col and pos_col:
            tdf = hist_teams.copy()
            tdf[pos_col] = pd.to_numeric(tdf[pos_col], errors="coerce")
            tdf[score_col] = pd.to_numeric(tdf[score_col], errors="coerce")
            tdf = tdf.dropna(subset=[score_col, pos_col])

            fig = go.Figure(go.Scatter(
                x=tdf[score_col],
                y=tdf[pos_col],
                mode="markers",
                marker=dict(
                    color=tdf[year_col] if year_col else "#4ade80",
                    colorscale=[[0, "#166534"], [1, "#4ade80"]],
                    size=9, opacity=0.75,
                    line=dict(color="#0a0f0a", width=1),
                    colorbar=dict(title="Year", tickfont=dict(color="#e8f0e8", size=9)) if year_col else None,
                    showscale=bool(year_col),
                ),
                text=tdf[participant_col] if participant_col else None,
                hovertemplate=("<b>%{text}</b><br>Score: %{x}<br>Position: %{y}<extra></extra>"
                               if participant_col else "Score: %{x}<br>Position: %{y}<extra></extra>"),
            ))

            # Add trend line
            valid = tdf[[score_col, pos_col]].dropna()
            if len(valid) > 2:
                m, b = np.polyfit(valid[score_col], valid[pos_col], 1)
                x_range = np.linspace(valid[score_col].min(), valid[score_col].max(), 50)
                fig.add_trace(go.Scatter(
                    x=x_range, y=m * x_range + b,
                    mode="lines",
                    line=dict(color="#f87171", width=1.5, dash="dash"),
                    name="Trend",
                    showlegend=True,
                ))

            fig.update_layout(**CHART_LAYOUT, height=360,
                              xaxis_title="Team Combined Score",
                              yaxis_title="Finishing Position",
                              yaxis=dict(autorange="reversed", gridcolor="rgba(74,222,128,0.08)"),
                              legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Expected team score/position columns not found in historical_teams.csv.")

        # Participant performance leaderboard
        if participant_col and pos_col:
            st.markdown("---")
            st.markdown("**Participant Performance Over the Years**")
            part_stats = (
                hist_teams.groupby(participant_col)[pos_col]
                .agg(["mean", "min", "count"])
                .rename(columns={"mean": "Avg Position", "min": "Best Position", "count": "Years Entered"})
                .sort_values("Avg Position")
                .reset_index()
            )
            part_stats["Avg Position"] = part_stats["Avg Position"].round(1)
            part_stats["Best Position"] = part_stats["Best Position"].astype(int)
            st.dataframe(
                part_stats,
                use_container_width=True,
                height=300,
                hide_index=True,
                column_config={
                    participant_col:   st.column_config.TextColumn("Participant"),
                    "Avg Position":    st.column_config.NumberColumn("Avg Finish", format="%.1f"),
                    "Best Position":   st.column_config.NumberColumn("Best Finish"),
                    "Years Entered":   st.column_config.NumberColumn("Years Entered"),
                },
            )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    try:
        df = load_players()
    except FileNotFoundError:
        st.error("❌  `consolidated_player_data_2026.csv` not found. Place it in the same directory as app.py.")
        st.stop()

    available_images = get_available_images()

    hist_odds    = load_historical_odds()
    hist_picks   = load_historical_picks()
    hist_winners = load_historical_winners()
    hist_scores  = load_historical_scores()
    hist_rounds  = load_historical_rounds()
    hist_teams   = load_historical_teams()

    filters = render_sidebar(df)
    page = st.session_state.page

    if page == "Player Picker":
        st.markdown("""
        <div class="page-title">Player Picker</div>
        <div class="page-subtitle">Masters 2026 · Build your 3-man team · Min. 150 combined odds</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_picker(df, filters)

    elif page == "Player Profile":
        st.markdown("""
        <div class="page-title">Player Profile</div>
        <div class="page-subtitle">Detailed stats · Augusta record · Performance radar</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_profile(df, available_images)

    elif page == "Historical Dashboard":
        st.markdown("""
        <div class="page-title">Historical Dashboard</div>
        <div class="page-subtitle">Trends, picks & winners across previous years</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams)


if __name__ == "__main__":
    main()
