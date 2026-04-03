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
        render_team_panel(df)


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
        for _, row in selected_df.iterrows():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:8px 0;border-bottom:1px solid var(--border);">
                <div>
                    <div style="font-family:'Playfair Display';font-size:14px;font-weight:700;">
                        {row['first_name']} {row['last_name']}
                    </div>
                    <div style="font-family:'DM Mono';font-size:10px;color:var(--text-muted);">
                        {risk_badge_html(row['risk'])} &nbsp; score: {row['value_score']:.3f}
                    </div>
                </div>
                <div style="font-family:'Playfair Display';font-size:18px;font-weight:900;color:var(--green);">
                    {int(row['odds'])}/1
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics
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

    st.markdown('</div>', unsafe_allow_html=True)

    if n > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear team", use_container_width=True):
            st.session_state.selected_ids = []
            st.rerun()


# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────

def render_player_profile(df):
    # Player selector at top
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

    left, right = st.columns([1, 2], gap="large")

    with left:
        # Headshot
        img_path = f"images/{row['first_name']} {row['last_name']}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, width=180)
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

        st.markdown(f"""
        <div style="margin-top:16px;">
            <div style="font-family:'Playfair Display';font-size:26px;font-weight:900;">
                {row['first_name']}<br>{row['last_name']}
            </div>
            <div style="font-family:'DM Mono';font-size:11px;color:var(--text-muted);margin-top:4px;letter-spacing:0.08em;">
                {row.get('country','—')} · {int(row['age'])} yrs
            </div>
            <div style="margin-top:12px;">{risk_badge_html(row['risk'])}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Key Stats</div>', unsafe_allow_html=True)

        stats = [
            ("Odds",             f"{int(row['odds'])}/1"),
            ("Value Score",      f"{row['value_score']:.3f}"),
            ("Masters Wins",     f"{int(row.get('masters_wins', 0))}"),
            ("Cuts Made",        f"{row.get('cuts_made_percentage', 0):.0f}%"),
            ("Avg Round",        f"{row.get('avg_round', 0):.2f}"),
            ("Rounds Under Par", f"{row.get('rounds_under_par_percentage', 0):.0f}%"),
            ("Best Finish",      f"T{int(row.get('best_finish_position', 0))}"),
            ("Implied Prob",     f"{row['implied_prob']*100:.1f}%"),
        ]
        for label, val in stats:
            st.markdown(f"""
            <div class="stat-row">
                <span class="label">{label.upper()}</span>
                <span class="value" style="font-family:'DM Mono';">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if row["id"] not in st.session_state.selected_ids:
            if len(st.session_state.selected_ids) < 3:
                if st.button("+ Add to team", use_container_width=True):
                    st.session_state.selected_ids.append(row["id"])
                    st.rerun()
        else:
            if st.button("✕ Remove from team", use_container_width=True):
                st.session_state.selected_ids.remove(row["id"])
                st.rerun()

    with right:
        st.markdown('<div class="section-header">Performance Radar</div>', unsafe_allow_html=True)

        norm_cols = [c for c in df.columns if c.endswith("_norm")]
        if norm_cols:
            values = [row[c] for c in norm_cols]
            labels = [c.replace("_norm", "").replace("_", " ").title() for c in norm_cols]
            values_closed = values + [values[0]]
            labels_closed = labels + [labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=labels_closed,
                fill="toself",
                fillcolor="rgba(74,222,128,0.12)",
                line=dict(color="#4ade80", width=2),
                marker=dict(color="#4ade80", size=5),
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
                height=420,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No normalised (_norm) columns found in player data.")


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

def render_historical(hist_odds, hist_picks, hist_winners):
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
                marker=dict(color="#4ade80", size=7,
                            line=dict(color="#0a0f0a", width=2)),
                fill="tozeroy",
                fillcolor="rgba(74,222,128,0.07)",
            ))
            fig.update_layout(**CHART_LAYOUT, height=380)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No odds data available.")

    st.markdown("---")
    row2_l, row2_r = st.columns(2, gap="large")

    # 3. combined_odds vs position scatter
    with row2_l:
        st.markdown("**Combined Odds vs Finishing Position**")
        if not hist_odds.empty and "combined_odds" in hist_odds.columns and "position" in hist_odds.columns:
            scatter_df = hist_odds.dropna(subset=["combined_odds", "position"]).copy()
            try:
                scatter_df["position"] = pd.to_numeric(scatter_df["position"], errors="coerce")
                scatter_df = scatter_df.dropna(subset=["position"])
            except Exception:
                pass

            fig = go.Figure(go.Scatter(
                x=scatter_df["combined_odds"],
                y=scatter_df["position"],
                mode="markers",
                marker=dict(
                    color=scatter_df["combined_odds"],
                    colorscale=[[0, "#166534"], [1, "#4ade80"]],
                    size=8,
                    opacity=0.7,
                    line=dict(color="#0a0f0a", width=1),
                ),
                text=scatter_df.get("participant", None),
                hovertemplate="<b>%{text}</b><br>Odds: %{x}<br>Position: %{y}<extra></extra>",
            ))
            fig.update_layout(**CHART_LAYOUT, height=340,
                              xaxis_title="Combined Odds",
                              yaxis_title="Position",
                              yaxis=dict(autorange="reversed",
                                         gridcolor="rgba(74,222,128,0.08)"))
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


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    # Load all data
    try:
        df = load_players()
    except FileNotFoundError:
        st.error("❌  `consolidated_player_data_2026.csv` not found. Place it in the same directory as app.py.")
        st.stop()

    try:
        hist_odds    = load_historical_odds()
        hist_picks   = load_historical_picks()
        hist_winners = load_historical_winners()
    except Exception:
        hist_odds = hist_picks = hist_winners = pd.DataFrame()

    # Sidebar (returns filters dict)
    filters = render_sidebar(df)

    # Page header
    page = st.session_state.page

    if page == "Player Picker":
        st.markdown(f"""
        <div class="page-title">Player Picker</div>
        <div class="page-subtitle">Masters 2026 · Build your 3-man team · Min. 150 combined odds</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_picker(df, filters)

    elif page == "Player Profile":
        st.markdown(f"""
        <div class="page-title">Player Profile</div>
        <div class="page-subtitle">Detailed stats & performance radar</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_profile(df)

    elif page == "Historical Dashboard":
        st.markdown(f"""
        <div class="page-title">Historical Dashboard</div>
        <div class="page-subtitle">Trends, picks & winners across previous years</div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_historical(hist_odds, hist_picks, hist_winners)


if __name__ == "__main__":
    main()
