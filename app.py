import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

st.set_page_config(
    page_title="Masters 2026 · Decision Support",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --green:#FEF102;--green-dim:#0e4f38;--green-glow:rgba(254,241,2,0.12);
    --bg:#166D4D;--surface:#0e4f38;--surface2:#1a5e42;
    --border:rgba(254,241,2,0.35);--text:#ffffff;--text-muted:#b8d4c8;
    --red:#f87171;--gold:#FEF102;
}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:#ffffff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:#ffffff!important;}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label,[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stToggle label{color:#ffffff!important;font-family:'DM Mono',monospace!important;font-size:11px!important;}
[data-testid="stSidebar"] input[type="number"]{background:#1a5e42!important;color:#ffffff!important;border:1px solid rgba(254,241,2,0.4)!important;border-radius:4px!important;}
/* ── Selectbox / dropdown dark fix ── */
div[data-baseweb="select"] > div{background:#1a5e42!important;color:#ffffff!important;border-color:rgba(254,241,2,0.4)!important;}
div[data-baseweb="select"] span,div[data-baseweb="select"] div,div[data-baseweb="select"] input{color:#ffffff!important;background:transparent!important;}
div[data-baseweb="popover"] *,div[data-baseweb="menu"] *{background:#1a5e42!important;color:#ffffff!important;}
div[data-baseweb="menu"] li:hover,div[data-baseweb="popover"] li:hover{background:#0e4f38!important;}
div[data-baseweb="tag"]{background:#0e4f38!important;color:#FEF102!important;}
ul[data-baseweb="menu"]{background:#1a5e42!important;}
/* Radio */
[data-testid="stRadio"] label,[data-testid="stRadio"] *{color:#ffffff!important;}
p,li,span,div,td,th,label{color:#ffffff;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#ffffff!important;}
/* Metric cards */
[data-testid="metric-container"]{background:#1a5e42!important;border:1px solid var(--border)!important;border-radius:8px!important;padding:16px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#FEF102!important;font-size:2rem!important;font-weight:700!important;}
[data-testid="metric-container"] [data-testid="stMetricLabel"]{color:#ffffff!important;font-size:0.85rem!important;}
/* All buttons uniform */
.stButton>button{
    background:transparent!important;border:1px solid var(--border)!important;
    color:var(--green)!important;font-family:'DM Mono',monospace!important;
    font-size:12px!important;letter-spacing:0.05em!important;border-radius:4px!important;
    transition:all 0.2s!important;padding:4px 10px!important;
}
.stButton>button:hover{background:var(--green-glow)!important;border-color:var(--green)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:8px!important;}
hr{border-color:var(--border)!important;}
.player-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:4px;transition:border-color 0.2s;}
.player-card:hover{border-color:var(--green);}
.player-card .name{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:#ffffff;}
.player-card .sub{font-family:'DM Mono',monospace;font-size:11px;color:#b8d4c8;letter-spacing:0.06em;margin-top:2px;}
.player-card .odds{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:var(--green);}
.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;font-weight:500;}
.badge-safe{background:rgba(254,241,2,0.15);color:#FEF102;border:1px solid rgba(254,241,2,0.4);}
.badge-balanced{background:rgba(251,191,36,0.12);color:#fbbf24;border:1px solid rgba(251,191,36,0.3);}
.badge-high{background:rgba(248,113,113,0.12);color:#f87171;border:1px solid rgba(248,113,113,0.3);}
.team-panel{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:20px;}
.team-panel.valid{border-color:#FEF102;box-shadow:0 0 20px rgba(254,241,2,0.15);}
.team-panel.invalid{border-color:#f87171;box-shadow:0 0 20px rgba(248,113,113,0.08);}
.section-header{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:#b8d4c8;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--border);}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(254,241,2,0.08);font-size:13px;}
.stat-row .label{color:#b8d4c8;font-family:'DM Mono',monospace;font-size:11px;}
.stat-row .value{color:#ffffff;font-weight:500;}
.page-title{font-family:'Playfair Display',serif;font-size:38px;font-weight:900;line-height:1.1;letter-spacing:-0.01em;background:linear-gradient(135deg,#ffffff 0%,#FEF102 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.page-subtitle{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:#b8d4c8;margin-top:4px;}
.bio-card{background:#1a5e42;border:1px solid var(--border);border-radius:10px;padding:20px;margin-bottom:16px;}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}
.info-item{background:#1a5e42;border:1px solid var(--border);border-radius:8px;padding:12px 14px;}
.info-item .ilabel{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:#b8d4c8;margin-bottom:4px;}
.info-item .ivalue{font-family:'DM Mono',monospace;font-size:15px;font-weight:500;color:#ffffff;}
.info-item .ivalue.highlight{color:var(--green);font-family:'Playfair Display',serif;font-size:20px;font-weight:900;}
.suggest-card{background:var(--surface2);border:1px solid rgba(254,241,2,0.15);border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.suggest-card .sname{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;color:#ffffff;}
.suggest-card .smeta{font-family:'DM Mono',monospace;font-size:10px;color:#b8d4c8;}
.progress-wrap{background:#1a5e42;border:1px solid var(--border);border-radius:8px;padding:14px 16px;margin-bottom:12px;}
.progress-label{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#b8d4c8;margin-bottom:6px;display:flex;justify-content:space-between;}
.progress-track{background:#0e4f38;border-radius:4px;height:12px;overflow:hidden;border:1px solid rgba(254,241,2,0.2);}
.progress-bar{height:100%;border-radius:4px;transition:width 0.4s ease;}
@media(max-width:768px){.mobile-team-top{display:block!important;}.desktop-team-only{display:none!important;}}
@media(min-width:769px){.mobile-team-top{display:none!important;}.desktop-team-only{display:block!important;}}
</style>
""", unsafe_allow_html=True)

EXCLUDED_PLAYERS = [("phil", "mickelson")]

# ─────────────────────────── helpers ─────────────────────────────────────────

@st.cache_data
def get_available_images():
    if not os.path.isdir("images"):
        return set()
    return {os.path.splitext(f)[0] for f in os.listdir("images") if f.lower().endswith(".jpg")}


def lbs_to_kg(val):
    try:
        v = float(str(val).lower().replace("lbs","").replace("kg","").replace("lb","").strip())
        if v > 100:
            v = round(v * 0.453592)
        return f"{int(v)} kg"
    except Exception:
        return str(val)


def _col(df, *candidates):
    """Return first matching column name (case-insensitive), or None."""
    lc = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lc:
            return lc[cand.lower()]
    return None


@st.cache_data
def load_players():
    df = pd.read_csv("consolidated_player_data_2026.csv")
    # Normalise column names to lowercase
    df.columns = [c.strip().lower() for c in df.columns]
    # Fix percentages stored as decimals
    pct_cols = [c for c in df.columns if "percentage" in c or c.endswith("_pct")]
    for col in pct_cols:
        s = pd.to_numeric(df[col], errors="coerce")
        if s.dropna().max() <= 1.0:
            df[col] = s * 100
    # Exclude withdrawn/ineligible
    mask = pd.Series([True] * len(df), index=df.index)
    for fn, ln in EXCLUDED_PLAYERS:
        fc = _col(df, "first_name", "first")
        lc = _col(df, "last_name", "last")
        if fc and lc:
            mask &= ~((df[fc].str.lower() == fn) & (df[lc].str.lower() == ln))
    df = df[mask].copy().reset_index(drop=True)
    df = compute_value_scores(df)
    df["risk"] = df["odds"].apply(classify_risk)
    df["implied_prob"] = 1 / (df["odds"] + 1)
    return df


@st.cache_data
def load_csv_safe(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def minmax(series):
    s = pd.to_numeric(series, errors="coerce").fillna(0)
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series([0.5] * len(s), index=s.index)
    return (s - mn) / (mx - mn)


def compute_value_scores(df):
    df = df.copy()
    needed = ["avg_round", "cuts_made_percentage", "masters_wins",
              "rounds_under_par_percentage", "best_finish_position"]
    for c in needed:
        if c not in df.columns:
            df[c] = 0
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["_n_avg_round"]   = 1 - minmax(df["avg_round"])
    df["_n_cuts"]        = minmax(df["cuts_made_percentage"])
    df["_n_wins"]        = minmax(df["masters_wins"])
    df["_n_rup"]         = minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"] = 1 - minmax(df["best_finish_position"])
    df["value_score"] = (
        0.30 * df["_n_avg_round"]   +
        0.20 * df["_n_cuts"]        +
        0.20 * df["_n_wins"]        +
        0.15 * df["_n_rup"]         +
        0.15 * df["_n_best_finish"]
    )
    df.drop(columns=[c for c in df.columns if c.startswith("_n_")], inplace=True)
    return df


def classify_risk(odds):
    if odds < 25:    return "Safe"
    elif odds <= 60: return "Balanced"
    return "High Risk"


def risk_badge_html(risk):
    cls = {"Safe":"badge-safe","Balanced":"badge-balanced","High Risk":"badge-high"}.get(risk,"badge-safe")
    return f'<span class="badge {cls}">{risk}</span>'


def best_finish_display(val):
    try:
        v = int(float(val))
        return str(v) if v > 0 else "Rookie"
    except Exception:
        return "Rookie"


def fmt_currency(val):
    try:
        return f"${float(val):,.0f}"
    except Exception:
        return "—"


SORT_ASC = {
    "odds": True, "age": True, "avg_round": True,
    "value_score": False, "cuts_made_percentage": False,
    "masters_wins": False, "rounds_under_par_percentage": False,
}


def suggest_completions(df, selected_ids, top_n=5):
    selected_df = df[df["id"].isin(selected_ids)]
    n = len(selected_ids)
    current_odds = selected_df["odds"].sum() if n > 0 else 0
    slots_remaining = 3 - n
    candidates = df[~df["id"].isin(selected_ids)].copy()
    if slots_remaining == 1:
        candidates = candidates[candidates["odds"] >= max(0, 150 - current_odds)]
    elif slots_remaining == 2:
        needed_total = max(0, 150 - current_odds)
        candidates = candidates[candidates["odds"] >= needed_total * 0.3]
    return candidates.sort_values("odds", ascending=True).head(top_n)


def _chart_layout(height=380, xaxis=None, yaxis=None, extra=None):
    layout = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(14,79,56,0.5)",
        font=dict(family="DM Sans", color="#ffffff", size=11),
        margin=dict(l=40, r=20, t=40, b=40), height=height)
    _x = dict(gridcolor="rgba(254,241,2,0.08)", linecolor="rgba(254,241,2,0.2)")
    _y = dict(gridcolor="rgba(254,241,2,0.08)", linecolor="rgba(254,241,2,0.2)")
    if xaxis: _x.update(xaxis)
    if yaxis: _y.update(yaxis)
    layout["xaxis"] = _x
    layout["yaxis"] = _y
    if extra: layout.update(extra)
    return layout


def init_state():
    defaults = {"selected_ids":[], "page":"Player Picker", "profile_id":None,
                "filter_odds_range":None, "filter_age_range":None,
                "filter_countries":[], "filter_masters_winners_only":False, "filter_cuts_range":None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ─────────────────────────── SIDEBAR ─────────────────────────────────────────

def render_sidebar(df):
    with st.sidebar:
        # Logo + title
        st.markdown("## ⛳ Masters 2026")
        st.caption("Decision Support Tool")
        st.markdown("---")
        st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
        pages = ["Player Picker","Player Profile","Score & Risk","Historical Dashboard"]
        icons = {"Player Picker":"🏌️","Player Profile":"👤","Score & Risk":"📈","Historical Dashboard":"📊"}
        for p in pages:
            if st.button(f"{icons[p]}  {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()
        st.markdown("---")
        if st.session_state.page == "Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
            odds_min_abs, odds_max_abs = int(df["odds"].min()), int(df["odds"].max())
            if st.session_state.filter_odds_range is None:
                st.session_state.filter_odds_range = (odds_min_abs, odds_max_abs)
            st.markdown('<div style="font-size:10px;color:#ffffff;font-family:DM Mono,monospace;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Odds Range</div>', unsafe_allow_html=True)
            oc1, oc2 = st.columns(2)
            with oc1: odds_lo = st.number_input("Min", min_value=odds_min_abs, max_value=odds_max_abs, value=st.session_state.filter_odds_range[0], step=5, key="odds_lo")
            with oc2: odds_hi = st.number_input("Max", min_value=odds_min_abs, max_value=odds_max_abs, value=st.session_state.filter_odds_range[1], step=5, key="odds_hi")
            odds_range = (min(odds_lo,odds_hi), max(odds_lo,odds_hi))
            st.session_state.filter_odds_range = odds_range

            age_min_abs, age_max_abs = int(df["age"].min()), int(df["age"].max())
            if st.session_state.filter_age_range is None:
                st.session_state.filter_age_range = (age_min_abs, age_max_abs)
            st.markdown('<div style="font-size:10px;color:#ffffff;font-family:DM Mono,monospace;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Age Range</div>', unsafe_allow_html=True)
            ac1, ac2 = st.columns(2)
            with ac1: age_lo = st.number_input("Min", min_value=age_min_abs, max_value=age_max_abs, value=st.session_state.filter_age_range[0], step=1, key="age_lo")
            with ac2: age_hi = st.number_input("Max", min_value=age_min_abs, max_value=age_max_abs, value=st.session_state.filter_age_range[1], step=1, key="age_hi")
            age_range = (min(age_lo,age_hi), max(age_lo,age_hi))
            st.session_state.filter_age_range = age_range

            countries = sorted(df["country"].dropna().unique().tolist()) if "country" in df.columns else []
            selected_countries = st.multiselect("Country", countries, default=st.session_state.filter_countries, key="country_select")
            st.session_state.filter_countries = selected_countries

            masters_winners_only = st.toggle("Masters winners only", value=st.session_state.filter_masters_winners_only, key="winners_toggle")
            st.session_state.filter_masters_winners_only = masters_winners_only

            cuts_min_abs = float(df["cuts_made_percentage"].min())
            cuts_max_abs = float(df["cuts_made_percentage"].max())
            if st.session_state.filter_cuts_range is None:
                st.session_state.filter_cuts_range = (cuts_min_abs, cuts_max_abs)
            st.markdown('<div style="font-size:10px;color:#ffffff;font-family:DM Mono,monospace;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Cuts Made %</div>', unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1: cuts_lo = st.number_input("Min", min_value=cuts_min_abs, max_value=cuts_max_abs, value=st.session_state.filter_cuts_range[0], step=5.0, key="cuts_lo", format="%.0f")
            with cc2: cuts_hi = st.number_input("Max", min_value=cuts_min_abs, max_value=cuts_max_abs, value=st.session_state.filter_cuts_range[1], step=5.0, key="cuts_hi", format="%.0f")
            cuts_range = (min(cuts_lo,cuts_hi), max(cuts_lo,cuts_hi))
            st.session_state.filter_cuts_range = cuts_range
            return {"odds_range":odds_range, "age_range":age_range, "countries":selected_countries,
                    "masters_winners_only":masters_winners_only, "cuts_range":cuts_range}
    return {}


# ─────────────────────────── PLAYER PICKER ───────────────────────────────────

def render_player_picker(df, filters):
    fdf = df.copy()
    fdf = fdf[fdf["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"] and "country" in fdf.columns:
        fdf = fdf[fdf["country"].isin(filters["countries"])]
    if filters["masters_winners_only"]:
        fdf = fdf[fdf["masters_wins"] > 0]
    fdf = fdf[fdf["cuts_made_percentage"].between(*filters["cuts_range"])]

    st.markdown('<div class="mobile-team-top">', unsafe_allow_html=True)
    render_team_panel(df, context="mobile")
    st.markdown('</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1], gap="large")
    with left_col:
        st.markdown('<div class="section-header">Player Pool</div>', unsafe_allow_html=True)
        st.caption(f"{len(fdf)} players · {len(st.session_state.selected_ids)}/3 selected")
        sort_col = st.selectbox("Sort by", list(SORT_ASC.keys()),
            format_func=lambda x: x.replace("_"," ").title(), label_visibility="collapsed")
        if sort_col == "avg_round":
            rookies = fdf[fdf["avg_round"] == 0]
            non_rookies = fdf[fdf["avg_round"] != 0].sort_values("avg_round", ascending=True)
            fdf = pd.concat([non_rookies, rookies])
        else:
            fdf = fdf.sort_values(sort_col, ascending=SORT_ASC.get(sort_col, True))

        for _, row in fdf.iterrows():
            pid = row["id"]
            is_selected = pid in st.session_state.selected_ids
            card_border = "border-color: var(--green);" if is_selected else ""
            avg_rnd_display = "Rookie" if row["avg_round"] == 0 else f"{row['avg_round']:.1f}"
            country = row.get("country","—") if "country" in row.index else "—"
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"""<div class="player-card" style="{card_border}">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{country} · Age {int(row['age'])} · {risk_badge_html(row['risk'])}</div>
                    <div style="display:flex;gap:24px;margin-top:10px;align-items:flex-end;">
                        <div><div class="sub">ODDS</div><div class="odds">{int(row['odds'])}/1</div></div>
                        <div><div class="sub">VALUE</div><div style="font-size:18px;font-family:'DM Mono';color:#ffffff;">{row['value_score']:.3f}</div></div>
                        <div><div class="sub">CUTS MADE</div><div style="font-size:15px;font-family:'DM Mono';color:#ffffff;">{row['cuts_made_percentage']:.0f}%</div></div>
                        <div><div class="sub">AVG RND</div><div style="font-size:15px;font-family:'DM Mono';color:#ffffff;">{avg_rnd_display}</div></div>
                    </div></div>""", unsafe_allow_html=True)
            with col_b:
                if st.button("Profile", key=f"prof_{pid}"):
                    st.session_state.profile_id = pid
                    st.session_state.page = "Player Profile"
                    st.rerun()
                if is_selected:
                    if st.button("✕ Remove", key=f"rem_{pid}"):
                        st.session_state.selected_ids.remove(pid)
                        st.rerun()
                else:
                    disabled = len(st.session_state.selected_ids) >= 3
                    if st.button("+ Add", key=f"add_{pid}", disabled=disabled):
                        st.session_state.selected_ids.append(pid)
                        st.rerun()

    with right_col:
        st.markdown('<div class="desktop-team-only">', unsafe_allow_html=True)
        render_team_panel(df, context="desktop")
        st.markdown('</div>', unsafe_allow_html=True)


def render_team_panel(df, context="main"):
    st.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)
    selected_df = df[df["id"].isin(st.session_state.selected_ids)]
    n = len(st.session_state.selected_ids)
    c_odds = selected_df["odds"].sum() if n > 0 else 0
    t_strength = selected_df["value_score"].sum() if n > 0 else 0
    is_valid = (n == 3) and (c_odds >= 150)

    pct = min(c_odds / 150 * 100, 100)
    bar_color = "#FEF102" if c_odds >= 150 else "#f87171"
    st.markdown(f"""<div class="progress-wrap">
        <div class="progress-label">
            <span>COMBINED ODDS TOWARD 150</span>
            <span style="color:{bar_color};font-weight:700;">{int(c_odds)} / 150</span>
        </div>
        <div class="progress-track">
            <div class="progress-bar" style="width:{pct:.1f}%;background:{bar_color};"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    panel_cls = "valid" if is_valid else ("invalid" if n == 3 else "")
    st.markdown(f'<div class="team-panel {panel_cls}">', unsafe_allow_html=True)
    if n == 0:
        st.markdown('<div style="color:#a0b8a0;font-family:\'DM Mono\';font-size:12px;text-align:center;padding:20px 0;">Select 3 golfers to build your team</div>', unsafe_allow_html=True)
    else:
        for _, row in selected_df.iterrows():
            pid = row["id"]
            c1, c2, c3 = st.columns([5, 1, 1])
            with c1:
                st.markdown(f"""<div style="padding:8px 0;border-bottom:1px solid var(--border);">
                    <div style="font-family:'Playfair Display';font-size:14px;font-weight:700;color:#ffffff;">{row['first_name']} {row['last_name']}</div>
                    <div style="font-family:'DM Mono';font-size:10px;color:#a0b8a0;">{risk_badge_html(row['risk'])} &nbsp; {int(row['odds'])}/1 &nbsp; score:{row['value_score']:.3f}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("Profile", key=f"panel_prof_{context}_{pid}"):
                    st.session_state.profile_id = pid
                    st.session_state.page = "Player Profile"
                    st.rerun()
            with c3:
                if st.button("✕", key=f"panel_rem_{context}_{pid}"):
                    st.session_state.selected_ids.remove(pid)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-row"><span class="label">TEAM STRENGTH</span><span class="value" style="font-family:'DM Mono';">{t_strength:.3f}</span></div>
        <div class="stat-row"><span class="label">SLOTS FILLED</span><span class="value" style="font-family:'DM Mono';">{n} / 3</span></div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if n == 3 and not is_valid:
            st.markdown('<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.3);border-radius:6px;padding:10px;font-family:\'DM Mono\';font-size:11px;color:#f87171;">⚠ Combined odds must be ≥ 150 for a valid entry.</div>', unsafe_allow_html=True)
        elif is_valid:
            st.markdown('<div style="background:rgba(254,241,2,0.08);border:1px solid rgba(254,241,2,0.35);border-radius:6px;padding:10px;font-family:\'DM Mono\';font-size:11px;color:#4ade80;">✓ Valid team — ready to submit.</div>', unsafe_allow_html=True)
            st.markdown("""<div style="margin-top:10px;text-align:center;">
                <a href="https://eoghanobrien-bit.github.io/masters-sweepstake/" target="_blank"
                   style="display:inline-block;padding:10px 20px;background:rgba(254,241,2,0.12);border:1px solid rgba(254,241,2,0.5);border-radius:6px;font-family:'DM Mono';font-size:12px;color:#4ade80;text-decoration:none;letter-spacing:0.06em;">
                    ⛳ Submit your team →</a></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if 0 < n < 3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Suggested Additions</div>', unsafe_allow_html=True)
        suggestions = suggest_completions(df, st.session_state.selected_ids)
        if suggestions.empty:
            st.caption("No valid completions found.")
        else:
            for _, srow in suggestions.iterrows():
                spid = srow["id"]
                sc1, sc2 = st.columns([4, 1])
                with sc1:
                    st.markdown(f"""<div class="suggest-card">
                        <div class="sname">{srow['first_name']} {srow['last_name']}</div>
                        <div class="smeta">{int(srow['odds'])}/1 · score {srow['value_score']:.3f} · {risk_badge_html(srow['risk'])}</div>
                    </div>""", unsafe_allow_html=True)
                with sc2:
                    if st.button("+ Add", key=f"sug_{context}_{spid}"):
                        st.session_state.selected_ids.append(spid)
                        st.rerun()

    if n > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear team", use_container_width=True, key=f"clear_{context}"):
            st.session_state.selected_ids = []
            st.rerun()


# ─────────────────────────── PLAYER PROFILE ──────────────────────────────────

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

    top_left, top_mid, top_right = st.columns([1, 2, 1], gap="large")
    with top_left:
        img_key = f"{row['first_name']} {row['last_name']}"
        if img_key in available_images:
            st.image(f"images/{img_key}.jpg", width=180)
        else:
            initials = f"{row['first_name'][0]}{row['last_name'][0]}"
            st.markdown(f'<div style="width:120px;height:120px;border-radius:50%;background:#1e2a1e;border:2px solid var(--border);display:flex;align-items:center;justify-content:center;font-family:\'Playfair Display\';font-size:36px;color:#a0b8a0;">{initials}</div>', unsafe_allow_html=True)
    with top_mid:
        world_rank = f" &nbsp;·&nbsp; World Rank #{int(row['world_ranking'])}" if "world_ranking" in row.index and pd.notna(row.get("world_ranking")) else ""
        country = row.get("country","—") if "country" in row.index else "—"
        st.markdown(f"""<div style="padding-top:8px;">
            <div style="font-family:'Playfair Display';font-size:32px;font-weight:900;line-height:1.1;color:#ffffff;">{row['first_name']} {row['last_name']}</div>
            <div style="font-family:'DM Mono';font-size:11px;color:#a0b8a0;margin-top:6px;letter-spacing:0.08em;">{country} &nbsp;·&nbsp; Age {int(row['age'])}{world_rank}</div>
            <div style="margin-top:10px;">{risk_badge_html(row['risk'])} <span style="font-family:'Playfair Display';font-size:28px;font-weight:900;color:var(--green);margin-left:16px;">{int(row['odds'])}/1</span></div>
        </div>""", unsafe_allow_html=True)
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
    tab_overview, tab_masters, tab_radar = st.tabs(["📋 Overview","🏆 Masters Record & Stats","🎯 Radar"])
    with tab_overview:
        _render_profile_overview(row, df)
    with tab_masters:
        _render_profile_combined(row, df)
    with tab_radar:
        _render_profile_radar(row, df)


def _render_profile_overview(row, df):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-header">Player Overview</div>', unsafe_allow_html=True)
        grid_items = []
        for field, label, highlight in [
            ("world_ranking","WORLD RANKING",True),
            ("age","AGE",False),
            ("turned_pro","TURNED PRO",False),
            ("country","COUNTRY",False),
            ("college","COLLEGE",False),
            ("height","HEIGHT",False),
            ("residence","RESIDENCE",False),
        ]:
            if field not in row.index: continue
            v = row.get(field)
            if v is None or str(v) in ["","nan","None","NaN"]: continue
            if field == "world_ranking":
                grid_items.append((label, f"#{int(float(v))}", highlight))
            elif field == "age":
                grid_items.append((label, str(int(float(v))), highlight))
            elif field == "turned_pro":
                grid_items.append((label, str(int(float(v))), highlight))
            else:
                grid_items.append((label, str(v), highlight))

        # Weight (lbs → kg)
        if "weight" in row.index:
            wt = row.get("weight")
            if wt is not None and str(wt) not in ["","nan","None","NaN"]:
                grid_items.append(("WEIGHT", lbs_to_kg(wt), False))

        if grid_items:
            html = '<div class="info-grid">'
            for label, val, highlight in grid_items:
                cls = "highlight" if highlight else ""
                html += f'<div class="info-item"><div class="ilabel">{label}</div><div class="ivalue {cls}">{val}</div></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

        # Instagram
        if "instagram" in row.index:
            insta = row.get("instagram")
            if insta and str(insta) not in ["","nan","None","NaN"]:
                handle = str(insta).replace("@","").strip()
                st.markdown(f"""<div class="bio-card" style="padding:12px 14px;margin-top:0;">
                    <a href="https://instagram.com/{handle}" target="_blank" rel="noopener noreferrer"
                       style="display:flex;align-items:center;gap:10px;text-decoration:none;color:#ffffff;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="2" y="2" width="20" height="20" rx="5" ry="5" stroke="url(#ig_g)" stroke-width="2"/>
                      <circle cx="12" cy="12" r="5" stroke="url(#ig_g)" stroke-width="2"/>
                      <circle cx="17.5" cy="6.5" r="1.5" fill="#e1306c"/>
                      <defs><linearGradient id="ig_g" x1="2" y1="22" x2="22" y2="2" gradientUnits="userSpaceOnUse">
                        <stop offset="0%" stop-color="#f09433"/><stop offset="25%" stop-color="#e6683c"/>
                        <stop offset="50%" stop-color="#dc2743"/><stop offset="75%" stop-color="#cc2366"/>
                        <stop offset="100%" stop-color="#bc1888"/>
                      </linearGradient></defs>
                    </svg>
                    <span style="font-family:'DM Mono';font-size:12px;color:#ffffff;">@{handle}</span>
                    </a></div>""", unsafe_allow_html=True)

        implied = row["implied_prob"] * 100
        st.markdown(f"""<div class="bio-card" style="margin-top:8px;">
            <div class="section-header" style="border:none;margin-bottom:6px;">ODDS CONTEXT</div>
            <div style="display:flex;gap:20px;flex-wrap:wrap;">
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:#a0b8a0;">ODDS</div>
                     <div style="font-family:'Playfair Display';font-size:24px;font-weight:900;color:var(--green);">{int(row['odds'])}/1</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:#a0b8a0;">IMPLIED PROB</div>
                     <div style="font-family:'DM Mono';font-size:20px;font-weight:500;color:#ffffff;">{implied:.1f}%</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:#a0b8a0;">VALUE SCORE</div>
                     <div style="font-family:'DM Mono';font-size:20px;font-weight:500;color:#ffffff;">{row['value_score']:.3f}</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:#a0b8a0;">RISK TIER</div>
                     <div style="margin-top:4px;">{risk_badge_html(row['risk'])}</div></div>
            </div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
        overview_text = ""
        for field in ["overview","bio","biography","about"]:
            if field in row.index:
                v = str(row.get(field,""))
                if v not in ["","nan","None","NaN"]:
                    overview_text = v
                    break
        if overview_text:
            st.markdown(f'<div class="bio-card" style="line-height:1.7;font-size:14px;color:#ffffff;">{overview_text}</div>', unsafe_allow_html=True)
        else:
            st.info("No biography available for this player.")


def _safe_stat(row, col_name):
    """Return (value, True) if column exists and is non-null/zero-like, else (None, False)."""
    if col_name not in row.index:
        return None, False
    v = row[col_name]
    if v is None or (isinstance(v, float) and np.isnan(v)) or str(v) in ["","nan","None","NaN"]:
        return None, False
    return v, True


def _render_profile_combined(row, df):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-header">Augusta Record</div>', unsafe_allow_html=True)

        # Define all stats to show: (display_label, column_name, formatter, highlight)
        stats_spec = [
            ("MASTERS WINS",        "masters_wins",                lambda v: str(int(float(v))),                               True),
            ("APPEARANCES",         "masters_appearances",         lambda v: str(int(float(v))),                               False),
            ("BEST FINISH",         "best_finish_position",        best_finish_display,                                        True),
            ("TOURNAMENTS PLAYED",  "tournaments_played",          lambda v: str(int(float(v))),                               False),
	    ("CUTS MADE",           "cuts_made",                   lambda v: str(int(float(v))),                               False),
            ("CUTS MADE %",         "cuts_made_percentage",        lambda v: f"{float(v):.0f}%",                               False),            
            ("ROUNDS PLAYED",       "rounds_played",               lambda v: str(int(float(v))),                               False),
            ("TOTAL ROUNDS",        "total_rounds_played",         lambda v: str(int(float(v))),                               False),
            ("ROUNDS UNDER PAR",    "rounds_under_par",            lambda v: str(int(float(v))),                               False),
            ("ROUNDS UNDER PAR %",  "rounds_under_par_percentage", lambda v: f"{float(v):.0f}%",                               False),
            ("AVG ROUND SCORE",     "avg_round",                   lambda v: f"{float(v):.2f}" if float(v) > 0 else "Rookie",  False),
            ("LOW ROUND",           "low_round",                   lambda v: str(int(float(v))) if float(v) > 0 else "—",      False),
            ("LOWEST ROUND",        "lowest_round",                lambda v: str(int(float(v))) if float(v) > 0 else "—",      False),
            ("HIGH ROUND",          "high_round",                  lambda v: str(int(float(v))) if float(v) > 0 else "—",      False),
            ("HIGHEST ROUND",       "highest_round",               lambda v: str(int(float(v))) if float(v) > 0 else "—",      False),
            ("AVG FINISH POS",      "avg_finish_position",         lambda v: f"{float(v):.1f}",                                False),
            ("MONEY EARNED",        "money_earned",                lambda v: f"${float(v):,.0f}" if float(v) >= 0 else "—",           False),
        ]

        html = '<div class="info-grid">'
        found = 0
        for label, col_name, fmt_fn, highlight in stats_spec:
            v, ok = _safe_stat(row, col_name)
            if not ok:
                continue
            try:
                display = fmt_fn(v)
                cls = "highlight" if highlight else ""
                html += f'<div class="info-item"><div class="ilabel">{label}</div><div class="ivalue {cls}">{display}</div></div>'
                found += 1
            except Exception:
                pass
        html += '</div>'

        if found > 0:
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No Masters record data available for this player.")
            # Debug helper — show which cols are present
            st.caption(f"Available columns in dataset: {', '.join(sorted(df.columns.tolist()))}")

    with col2:
        st.markdown('<div class="section-header">Odds vs Field</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df["odds"], nbinsx=25,
            marker_color="rgba(254,241,2,0.18)",
            marker_line_color="rgba(254,241,2,0.5)", marker_line_width=1))
        fig.add_vline(x=row["odds"], line_color="#FEF102", line_width=2, line_dash="dash",
            annotation_text=f"{row['first_name']} {row['last_name']} ({int(row['odds'])}/1)",
            annotation_font_color="#FEF102", annotation_font_size=10)
        fig.update_layout(**_chart_layout(220, xaxis={"title":"Odds"}, yaxis={"title":"# Players"}))
        st.plotly_chart(fig, use_container_width=True)


def _render_profile_radar(row, df):
    # Collect _norm columns that have valid (non-constant) data across the field
    norm_cols = []
    for c in df.columns:
        if not c.endswith("_norm"):
            continue
        s = pd.to_numeric(df[c], errors="coerce")
        # Skip if all NaN or all the same value (no discrimination)
        if s.notna().sum() < 2:
            continue
        # Clamp to [0,1] — if a _norm col was accidentally stored as 0–100, rescale it
        s_clean = s.dropna()
        if s_clean.max() > 1.0:
            df[c] = s / s.max()  # rescale in-place for this session
        norm_cols.append(c)

    if not norm_cols:
        st.info("No normalised (_norm) columns found in player data.")
        return

    # Map norm col → raw col for tooltip display only
    raw_col_map = {}
    for nc in norm_cols:
        raw = nc[:-5]  # strip _norm
        raw_col_map[nc] = raw if raw in df.columns else None

    player_options = ["Field Average"] + df.apply(lambda r: f"{r['first_name']} {r['last_name']}", axis=1).tolist()
    compare_label = st.selectbox("Compare against", player_options, index=0, key="radar_compare")

    labels = [c.replace("_norm","").replace("_"," ").title() for c in norm_cols]

    def safe_norm(r, nc):
        """Always read from the _norm column; clamp to [0,1]."""
        try:
            v = float(r[nc])
            if np.isnan(v): return 0.0
            return max(0.0, min(1.0, v))
        except Exception:
            return 0.0

    def fmt_tooltip(rc, v):
        """Format raw value for hover tooltip."""
        try:
            fv = float(v)
            if rc and ("percentage" in rc or rc.endswith("_pct")):
                return f"{fv:.1f}%"
            if rc and ("earning" in rc or "prize" in rc or "money" in rc):
                return f"${fv:,.0f}"
            return f"{fv:.2f}"
        except Exception:
            return str(v) if v is not None else "—"

    def player_vals(r):
        vals, raws = [], []
        for nc in norm_cols:
            # Shape: strictly from _norm column
            vals.append(safe_norm(r, nc))
            # Tooltip: from raw column if it exists
            rc = raw_col_map[nc]
            if rc and rc in r.index:
                raws.append(fmt_tooltip(rc, r[rc]))
            else:
                raws.append(fmt_tooltip(None, r[nc]))
        return vals, raws

    p_vals, p_raws = player_vals(row)

    if compare_label == "Field Average":
        c_vals, c_raws = [], []
        for nc in norm_cols:
            avg_norm = pd.to_numeric(df[nc], errors="coerce").mean()
            c_vals.append(max(0.0, min(1.0, avg_norm)) if pd.notna(avg_norm) else 0.0)
            rc = raw_col_map[nc]
            if rc and rc in df.columns:
                avg_raw = pd.to_numeric(df[rc], errors="coerce").mean()
                c_raws.append(fmt_tooltip(rc, avg_raw) if pd.notna(avg_raw) else "—")
            else:
                c_raws.append(fmt_tooltip(None, avg_norm))
        c_name, c_color, c_fill = "Field Average", "#fbbf24", "rgba(251,191,36,0.08)"
    else:
        match = df[df.apply(lambda r: f"{r['first_name']} {r['last_name']}" == compare_label, axis=1)]
        if match.empty:
            st.warning("Player not found.")
            return
        c_vals, c_raws = player_vals(match.iloc[0])
        c_name, c_color, c_fill = compare_label, "#f87171", "rgba(248,113,113,0.08)"

    def close(lst): return lst + [lst[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=close(c_vals), theta=close(labels), fill="toself",
        fillcolor=c_fill, line=dict(color=c_color, width=1.5, dash="dot"), name=c_name,
        customdata=close(c_raws),
        hovertemplate="<b>%{theta}</b><br>%{customdata}<extra>" + c_name + "</extra>"))
    fig.add_trace(go.Scatterpolar(r=close(p_vals), theta=close(labels), fill="toself",
        fillcolor="rgba(254,241,2,0.12)", line=dict(color="#FEF102", width=2),
        marker=dict(color="#FEF102", size=5),
        name=f"{row['first_name']} {row['last_name']}",
        customdata=close(p_raws),
        hovertemplate="<b>%{theta}</b><br>%{customdata}<extra>" + f"{row['first_name']} {row['last_name']}" + "</extra>"))
    fig.update_layout(
        polar=dict(bgcolor="rgba(14,79,56,0)",
            radialaxis=dict(visible=True, range=[0,1],
                gridcolor="rgba(254,241,2,0.18)", linecolor="rgba(254,241,2,0.18)",
                tickfont=dict(color="#b8d4c8", size=9, family="DM Mono")),
            angularaxis=dict(gridcolor="rgba(254,241,2,0.12)", linecolor="rgba(254,241,2,0.12)",
                tickfont=dict(color="#ffffff", size=10, family="DM Sans"))),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60,r=60,t=40,b=40), height=480, showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff", size=10)))
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────── SCORE & RISK ────────────────────────────────────

def render_score_risk_overview(df):
    st.markdown("**How Score & Risk Are Calculated**")
    exp_l, exp_r = st.columns(2, gap="large")
    with exp_l:
        st.markdown("""<div class="bio-card" style="font-size:13px;line-height:1.8;">
<div class="section-header">VALUE SCORE FORMULA</div>
The Value Score is a weighted composite of five Masters performance metrics, each normalised 0→1 across the field:
<br><br>
<div style="font-family:'DM Mono';font-size:12px;color:#4ade80;padding:10px;background:rgba(74,222,128,0.05);border-radius:6px;border:1px solid rgba(254,241,2,0.18);">
Score = 0.30 × Avg Round Score<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.20 × Cuts Made %<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.20 × Masters Wins<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.15 × Rounds Under Par %<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.15 × Best Finish Position
</div><br>
Higher score = stronger Augusta pedigree relative to the field. Rookies score 0 on most metrics.
</div>""", unsafe_allow_html=True)
    with exp_r:
        st.markdown("""<div class="bio-card" style="font-size:13px;line-height:1.8;">
<div class="section-header">RISK TIER CLASSIFICATION</div>
Risk is based on the player's pre-tournament betting odds:
<br><br>
<div style="font-family:'DM Mono';font-size:12px;padding:10px;background:rgba(74,222,128,0.05);border-radius:6px;border:1px solid rgba(254,241,2,0.18);">
<span style="color:#4ade80;">■ Safe</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Odds &lt; 25/1<br>
<span style="color:#fbbf24;">■ Balanced</span>&nbsp;&nbsp; Odds 25/1 – 60/1<br>
<span style="color:#f87171;">■ High Risk</span>&nbsp; Odds &gt; 60/1
</div><br>
The sweepstake requires a minimum combined team odds of 150, incentivising a mix of Safe anchors and High Risk outsiders.
<br><br>
<div class="section-header" style="margin-top:8px;">COMBINED TEAM ODDS</div>
Sum of each player's odds (e.g. 12 + 50 + 100 = 162). Must be ≥ 150 for a valid entry.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Field Overview</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Players", len(df))
    with m2: st.metric("Safe (<25/1)", len(df[df["risk"]=="Safe"]))
    with m3: st.metric("Balanced (25–60/1)", len(df[df["risk"]=="Balanced"]))
    with m4: st.metric("High Risk (>60/1)", len(df[df["risk"]=="High Risk"]))

    st.markdown("---")
    RISK_COLORS = {"Safe":"#FEF102","Balanced":"#fbbf24","High Risk":"#f87171"}
    r1l, r1r = st.columns(2, gap="large")
    with r1l:
        st.markdown("**Value Score vs Odds**")
        fig = go.Figure()
        for rt, grp in df.groupby("risk"):
            fig.add_trace(go.Scatter(x=grp["odds"], y=grp["value_score"], mode="markers", name=rt,
                marker=dict(color=RISK_COLORS.get(rt,"#FEF102"), size=8, opacity=0.8, line=dict(color="#0a0f0a",width=1)),
                text=grp["first_name"]+" "+grp["last_name"],
                hovertemplate="<b>%{text}</b><br>Odds: %{x}/1<br>Value: %{y:.3f}<extra></extra>"))
        fig.update_layout(**_chart_layout(380, xaxis={"title":"Odds"}, yaxis={"title":"Value Score"},
            extra={"legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11,color="#ffffff"))}))
        st.plotly_chart(fig, use_container_width=True)
    with r1r:
        st.markdown("**Risk Tier Breakdown**")
        rc = df["risk"].value_counts().reindex(["Safe","Balanced","High Risk"],fill_value=0).reset_index()
        rc.columns = ["Risk","Count"]
        fig = go.Figure(go.Bar(x=rc["Risk"], y=rc["Count"],
            marker_color=["#FEF102","#fbbf24","#f87171"],
            text=rc["Count"], textposition="outside", textfont=dict(color="#ffffff",size=12)))
        fig.update_layout(**_chart_layout(380))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    r2l, r2r = st.columns(2, gap="large")
    with r2l:
        st.markdown("**Cuts Made % vs Avg Round Score**")
        fig = go.Figure()
        for rt, grp in df.groupby("risk"):
            nr = grp[grp["avg_round"] > 0]
            if not nr.empty:
                fig.add_trace(go.Scatter(x=nr["cuts_made_percentage"], y=nr["avg_round"], mode="markers", name=rt,
                    marker=dict(color=RISK_COLORS.get(rt,"#FEF102"), size=8, opacity=0.8, line=dict(color="#0a0f0a",width=1)),
                    text=nr["first_name"]+" "+nr["last_name"],
                    hovertemplate="<b>%{text}</b><br>Cuts Made: %{x:.0f}%<br>Avg Round: %{y:.2f}<extra></extra>"))
        fig.update_layout(**_chart_layout(360, xaxis={"title":"Cuts Made %"}, yaxis={"title":"Avg Round Score"},
            extra={"legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11,color="#ffffff"))}))
        st.plotly_chart(fig, use_container_width=True)
    with r2r:
        st.markdown("**Top 20 by Value Score**")
        top20 = df.nlargest(20,"value_score")[["first_name","last_name","odds","value_score","risk"]].copy()
        top20["Player"] = top20["first_name"]+" "+top20["last_name"]
        top20["Odds"] = top20["odds"].apply(lambda x: f"{int(x)}/1")
        top20 = top20[["Player","Odds","value_score","risk"]].rename(columns={"value_score":"Value Score","risk":"Risk"})
        st.dataframe(top20.reset_index(drop=True), use_container_width=True, height=360,
            column_config={"Player":st.column_config.TextColumn("Player"),
                           "Odds":st.column_config.TextColumn("Odds"),
                           "Value Score":st.column_config.NumberColumn("Value Score",format="%.3f"),
                           "Risk":st.column_config.TextColumn("Risk")}, hide_index=True)

    st.markdown("---")
    st.markdown("**Full Field — Score & Risk Table**")
    tdf = df[["first_name","last_name","country","odds","value_score","risk",
              "cuts_made_percentage","avg_round","masters_wins","best_finish_position"]].copy() if "country" in df.columns else \
          df[["first_name","last_name","odds","value_score","risk",
              "cuts_made_percentage","avg_round","masters_wins","best_finish_position"]].copy()
    tdf["Player"] = tdf["first_name"]+" "+tdf["last_name"]
    tdf["Best Finish"] = tdf["best_finish_position"].apply(best_finish_display)
    show_cols = ["Player","odds","value_score","risk","cuts_made_percentage","avg_round","masters_wins","Best Finish"]
    if "country" in tdf.columns: show_cols.insert(1,"country")
    tdf = tdf[show_cols].sort_values("value_score",ascending=False)
    st.dataframe(tdf.reset_index(drop=True), use_container_width=True, height=500,
        column_config={"Player":st.column_config.TextColumn("Player"),
                       "country":st.column_config.TextColumn("Country"),
                       "odds":st.column_config.NumberColumn("Odds",format="%d/1"),
                       "value_score":st.column_config.NumberColumn("Value Score",format="%.3f"),
                       "risk":st.column_config.TextColumn("Risk"),
                       "cuts_made_percentage":st.column_config.NumberColumn("Cuts Made %",format="%.0f%%"),
                       "avg_round":st.column_config.NumberColumn("Avg Round",format="%.2f"),
                       "masters_wins":st.column_config.NumberColumn("Wins",format="%d"),
                       "Best Finish":st.column_config.TextColumn("Best Finish")}, hide_index=True)


# ─────────────────────────── HISTORICAL ──────────────────────────────────────

def render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams):

    # ── Normalise hist_picks ─────────────────────────────────────────────────
    if not hist_picks.empty:
        # Derive full name
        if "full_name" in hist_picks.columns:
            hist_picks["_name"] = hist_picks["full_name"].astype(str)
        elif "first_name" in hist_picks.columns and "last_name" in hist_picks.columns:
            hist_picks["_name"] = hist_picks["first_name"].astype(str)+" "+hist_picks["last_name"].astype(str)
        elif "first" in hist_picks.columns and "last" in hist_picks.columns:
            hist_picks["_name"] = hist_picks["first"].astype(str)+" "+hist_picks["last"].astype(str)
        elif "name" in hist_picks.columns:
            hist_picks["_name"] = hist_picks["name"].astype(str)
        else:
            hist_picks["_name"] = "Unknown"
        if "year" in hist_picks.columns:
            hist_picks["year"] = pd.to_numeric(hist_picks["year"], errors="coerce")

    # ── Most Picked Golfers ──────────────────────────────────────────────────
    st.markdown("**Most Picked Golfers (All Time)**")
    if not hist_picks.empty and "_name" in hist_picks.columns:
        picks_col = next((c for c in ["num_picks","picks","count"] if c in hist_picks.columns), None)
        if picks_col:
            hist_picks[picks_col] = pd.to_numeric(hist_picks[picks_col], errors="coerce")
            agg = hist_picks.groupby("_name",as_index=False)[picks_col].sum()
            agg = agg.sort_values(picks_col,ascending=False).head(15)
            x_vals = agg[picks_col].tolist()
        else:
            agg = hist_picks["_name"].value_counts().reset_index()
            agg.columns = ["_name","_cnt"]
            agg = agg.head(15)
            x_vals = agg["_cnt"].tolist()
        fig = go.Figure(go.Bar(x=x_vals, y=agg["_name"].tolist(), orientation="h",
            marker=dict(color=x_vals, colorscale=[[0,"#0e4f38"],[1,"#FEF102"]], showscale=False),
            hovertemplate="<b>%{y}</b><br>Picks: %{x}<extra></extra>"))
        fig.update_layout(**_chart_layout(420, yaxis={"autorange":"reversed"}))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No picks data available.")

    st.markdown("---")

    # ── Most Selected Player by Year — radio + scatter ───────────────────────
    st.markdown("**Most Selected Player by Year**")
    if not hist_picks.empty and "year" in hist_picks.columns:
        years_avail = sorted(hist_picks["year"].dropna().unique().astype(int).tolist())
        sel_year = st.radio("Year", [str(y) for y in years_avail], horizontal=True, key="top_player_year")
        yr_int = int(sel_year)
        pdf = hist_picks[hist_picks["year"] == yr_int].copy()

        if not pdf.empty:
            # Count picks per player for this year
            picks_col2 = next((c for c in ["num_picks","picks","count"] if c in pdf.columns), None)
            if picks_col2:
                pdf[picks_col2] = pd.to_numeric(pdf[picks_col2], errors="coerce").fillna(0)
                pdf2 = pdf.groupby("_name",as_index=False)[picks_col2].sum().rename(columns={"_name":"Player",picks_col2:"Picks"})
            else:
                pdf2 = pdf["_name"].value_counts().reset_index()
                pdf2.columns = ["Player","Picks"]

            pdf2["Picks"] = pd.to_numeric(pdf2["Picks"], errors="coerce").fillna(0)

            # Get odds for that year — try multiple sources
            odds_for_year = pd.Series(dtype=float)

            # Source 1: hist_odds participant→golfer/odds columns
            if not hist_odds.empty:
                ho = hist_odds.copy()
                if "year" in ho.columns:
                    ho = ho[pd.to_numeric(ho["year"], errors="coerce") == yr_int]
                golfer_cols = [c for c in ho.columns if c.startswith("golfer_")]
                odds_num_cols = sorted([c for c in ho.columns if c.startswith("odds") and c != "combined_odds"])
                if golfer_cols and odds_num_cols:
                    pairs = list(zip(golfer_cols, odds_num_cols))
                    rows_o = []
                    for _, r in ho.iterrows():
                        for gc, oc in pairs:
                            gname = str(r.get(gc, "")).strip()
                            oraw  = r.get(oc, np.nan)
                            if gname and gname not in ["", "nan", "None", "NaN"]:
                                rows_o.append({"Player": gname, "odds_val": pd.to_numeric(oraw, errors="coerce")})
                    if rows_o:
                        odds_for_year = pd.DataFrame(rows_o).groupby("Player")["odds_val"].mean()
                elif "_name" in ho.columns and "odds" in ho.columns:
                    odds_for_year = pd.to_numeric(ho.set_index("_name")["odds"], errors="coerce")

            # Source 2: fallback — look for an odds column directly in hist_picks
            if odds_for_year.empty or odds_for_year.isna().all():
                odds_col_p = next((c for c in pdf.columns if "odds" in c and "combined" not in c), None)
                if odds_col_p:
                    pdf["_odds_tmp"] = pd.to_numeric(pdf[odds_col_p], errors="coerce")
                    odds_for_year = pdf.groupby("_name")["_odds_tmp"].mean()

            pdf2["Odds"] = pdf2["Player"].map(odds_for_year) if len(odds_for_year) > 0 else np.nan

            # Scatter: num picks vs odds
            has_odds = "Odds" in pdf2.columns and pdf2["Odds"].notna().any()
            if has_odds:
                fig = go.Figure(go.Scatter(
                    x=pdf2["Odds"], y=pdf2["Picks"],
                    mode="markers+text",
                    text=pdf2["Player"],
                    textposition="top center",
                    textfont=dict(size=9, color="#a0b8a0"),
                    marker=dict(color=pdf2["Picks"],
                                colorscale=[[0,"#0e4f38"],[0.5,"#FEF102"],[1,"#fbbf24"]],
                                size=12, showscale=True,
                                colorbar=dict(title="Picks", tickfont=dict(color="#ffffff"),
                                              titlefont=dict(color="#ffffff")),
                                line=dict(color="#0a0f0a",width=1)),
                    hovertemplate="<b>%{text}</b><br>Odds: %{x}/1<br>Picks: %{y}<extra></extra>",
                ))
                fig.update_layout(**_chart_layout(420,
                    xaxis={"title":"Odds (lower = favourite)"},
                    yaxis={"title":"Times Picked"}))
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback: bar chart of picks
                pdf2s = pdf2.sort_values("Picks",ascending=False).head(15)
                fig = go.Figure(go.Bar(x=pdf2s["Picks"].tolist(), y=pdf2s["Player"].tolist(),
                    orientation="h", marker_color="#FEF102",
                    hovertemplate="<b>%{y}</b><br>Picks: %{x}<extra></extra>"))
                fig.update_layout(**_chart_layout(380, yaxis={"autorange":"reversed"}))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No picks data for {sel_year}.")
    else:
        st.info("No year column in picks data.")

    st.markdown("---")

    # ── Picks by Contestant (from historical_odds.csv) ───────────────────────
    st.markdown("**Picks by Contestant**")
    if not hist_odds.empty and "participant" in hist_odds.columns:
        ho = hist_odds.copy()
        if "year" in ho.columns:
            ho["year"] = pd.to_numeric(ho["year"], errors="coerce")
            years_c = sorted(ho["year"].dropna().unique().astype(int).tolist())
            sel_year_c = st.radio("Year", [str(y) for y in years_c], horizontal=True, key="contestant_year")
            ho = ho[ho["year"] == int(sel_year_c)]

        contestants = sorted(ho["participant"].dropna().astype(str).unique().tolist())
        if contestants:
            sel_p = st.selectbox("Contestant", contestants, key="contestant_sel")
            p_row = ho[ho["participant"] == sel_p]
            if not p_row.empty:
                p_row = p_row.iloc[0]
                # Build a clean 3-row table: one row per golfer
                rows_out = []
                for i in [1,2,3]:
                    gc = f"golfer_{i}" if f"golfer_{i}" in ho.columns else None
                    oc = f"odds{i}" if f"odds{i}" in ho.columns else None
                    if gc and oc:
                        gname = str(p_row.get(gc,"")).strip()
                        odds_v = p_row.get(oc, "")
                        if gname and gname not in ["","nan","None"]:
                            try: odds_disp = f"{int(float(odds_v))}/1"
                            except: odds_disp = str(odds_v)
                            rows_out.append({"Pick": f"Golfer {i}", "Player": gname, "Odds": odds_disp})
                # Combined odds
                combined = p_row.get("combined_odds","")
                try: combined_disp = f"{int(float(combined))}/1"
                except: combined_disp = str(combined)

                if rows_out:
                    out_df = pd.DataFrame(rows_out)
                    st.dataframe(out_df, use_container_width=True, height=175, hide_index=True,
                        column_config={"Pick":st.column_config.TextColumn("Pick"),
                                       "Player":st.column_config.TextColumn("Player"),
                                       "Odds":st.column_config.TextColumn("Odds")})
                    st.markdown(f"""<div class="bio-card" style="padding:12px 16px;margin-top:8px;">
                        <div class="section-header" style="border:none;margin-bottom:2px;">COMBINED ODDS</div>
                        <div style="font-family:'Playfair Display';font-size:24px;font-weight:900;color:var(--green);">{combined_disp}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.info("No golfer picks found for this participant.")
        else:
            st.info("No participants found for selected year.")
    elif hist_picks.empty:
        st.info("No historical_odds.csv data available.")
    else:
        st.info("historical_odds.csv does not have a 'participant' column.")

    st.markdown("---")

    # ── Teams per Year: Made Cut / Missed Cut ────────────────────────────────
    st.markdown("**Teams Entered per Year — Cut Status**")
    if not hist_teams.empty and "year" in hist_teams.columns:
        ht = hist_teams.copy()
        ht["year"] = pd.to_numeric(ht["year"], errors="coerce")

        if "made_cut" in ht.columns and "missed_cut" in ht.columns:
            ht["made_cut"]   = pd.to_numeric(ht["made_cut"],   errors="coerce").fillna(0)
            ht["missed_cut"] = pd.to_numeric(ht["missed_cut"], errors="coerce").fillna(0)
            agg = ht.groupby("year",as_index=False)[["made_cut","missed_cut"]].sum().sort_values("year")
            agg["total"] = agg["made_cut"] + agg["missed_cut"]
            yr_labels = agg["year"].astype(int).astype(str).tolist()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Made Cut", x=yr_labels, y=agg["made_cut"],
                marker_color="#FEF102",
                text=agg["made_cut"].astype(int), textposition="inside",
                textfont=dict(color="#0a0f0a",size=11,family="DM Mono")))
            fig.add_trace(go.Bar(name="Missed Cut", x=yr_labels, y=agg["missed_cut"],
                marker_color="#f87171",
                text=agg["missed_cut"].astype(int), textposition="inside",
                textfont=dict(color="#ffffff",size=11,family="DM Mono")))
            # Total labels on top
            fig.add_trace(go.Scatter(x=yr_labels, y=agg["total"], mode="text",
                text=agg["total"].astype(int).astype(str),
                textposition="top center",
                textfont=dict(color="#a0b8a0",size=10,family="DM Mono"),
                showlegend=False, hoverinfo="skip"))
            fig.update_layout(**_chart_layout(340, xaxis={"title":"Year"}, yaxis={"title":"Teams"},
                extra={"barmode":"stack",
                       "legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#ffffff",size=11))}))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Expected 'made_cut' and 'missed_cut' columns. Found: {list(ht.columns)}")
    else:
        st.info("No teams data or no 'year' column in historical_teams.csv.")

    st.markdown("---")

    # ── Previous Masters Winners ─────────────────────────────────────────────
    st.markdown("**Previous Masters Winners**")
    if not hist_winners.empty:
        rename_map = {}
        for c in hist_winners.columns:
            cl = c.lower()
            if any(x in cl for x in ["participant","entered_by","sweepstake","entry"]):
                rename_map[c] = "Sweepstakes Winner"
            elif any(x in cl for x in ["full_name","player","golfer","masters_winner","winner"]):
                rename_map[c] = "Masters Winner"
            elif "year" in cl:
                rename_map[c] = "Year"
        show = hist_winners.rename(columns=rename_map)
        show_cols = [c for c in ["Year","Masters Winner","Sweepstakes Winner"] if c in show.columns]
        if not show_cols:
            show_cols = list(show.columns)
        if "Year" in show.columns:
            show = show.sort_values("Year", ascending=False)
        st.dataframe(show[show_cols].reset_index(drop=True), use_container_width=True, height=340,
            column_config={"Year":st.column_config.NumberColumn("Year",format="%d"),
                           "Masters Winner":st.column_config.TextColumn("Masters Winner"),
                           "Sweepstakes Winner":st.column_config.TextColumn("Sweepstakes Winner")},
            hide_index=True)
    else:
        st.info("No winners data.")


# ─────────────────────────── MAIN ────────────────────────────────────────────

def main():
    try:
        df = load_players()
    except FileNotFoundError:
        st.error("❌ `consolidated_player_data_2026.csv` not found.")
        st.stop()

    available_images = get_available_images()
    hist_odds    = load_csv_safe("historical_odds.csv")
    hist_picks   = load_csv_safe("historical_picks.csv")
    hist_winners = load_csv_safe("historical_previous_winners.csv")
    hist_scores  = load_csv_safe("historical_scores.csv")
    hist_rounds  = load_csv_safe("historical_rounds.csv")
    hist_teams   = load_csv_safe("historical_teams.csv")

    filters = render_sidebar(df)
    page = st.session_state.page

    if page == "Player Picker":
        st.title("⛳ Player Picker")
        st.caption("Masters 2026 · Build your 3-man team · Min. 150 combined odds")
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_picker(df, filters)
    elif page == "Player Profile":
        st.title("👤 Player Profile")
        st.caption("Detailed stats · Augusta record · Performance radar")
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_profile(df, available_images)
    elif page == "Score & Risk":
        st.title("📈 Score & Risk")
        st.caption("Field overview · Value vs odds · Risk analysis")
        st.markdown("<br>", unsafe_allow_html=True)
        render_score_risk_overview(df)
    elif page == "Historical Dashboard":
        st.title("📊 Historical Dashboard")
        st.caption("Trends, picks & winners across previous years")
        st.markdown("<br>", unsafe_allow_html=True)
        render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams)


if __name__ == "__main__":
    main()
