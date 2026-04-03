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
    --green:#4ade80; --green-dim:#166534; --green-glow:rgba(74,222,128,0.15);
    --bg:#0a0f0a; --surface:#111811; --surface2:#182018;
    --border:rgba(74,222,128,0.18); --text:#e8f0e8; --text-muted:#7a9a7a;
    --red:#f87171; --gold:#fbbf24;
}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stToggle label{color:#e8f0e8!important;font-family:'DM Mono',monospace!important;font-size:11px!important;}
[data-testid="stSidebar"] input[type="number"]{background:#182018!important;color:#e8f0e8!important;border:1px solid rgba(74,222,128,0.3)!important;border-radius:4px!important;}
[data-testid="stSidebar"] .stNumberInput input{color:#e8f0e8!important;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:var(--text)!important;}
[data-testid="metric-container"]{background:var(--surface2)!important;border:1px solid var(--border)!important;border-radius:8px!important;padding:12px!important;}
.stButton>button{background:transparent!important;border:1px solid var(--border)!important;color:var(--green)!important;font-family:'DM Mono',monospace!important;font-size:12px!important;letter-spacing:0.05em!important;border-radius:4px!important;transition:all 0.2s!important;}
.stButton>button:hover{background:var(--green-glow)!important;border-color:var(--green)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:8px!important;}
hr{border-color:var(--border)!important;}
.player-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px;transition:border-color 0.2s;}
.player-card:hover{border-color:var(--green);}
.player-card .name{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:var(--text);}
.player-card .sub{font-family:'DM Mono',monospace;font-size:11px;color:var(--text-muted);letter-spacing:0.06em;margin-top:2px;}
.player-card .odds{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:var(--green);}
.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;font-weight:500;}
.badge-safe{background:rgba(74,222,128,0.12);color:#4ade80;border:1px solid rgba(74,222,128,0.3);}
.badge-balanced{background:rgba(251,191,36,0.12);color:#fbbf24;border:1px solid rgba(251,191,36,0.3);}
.badge-high{background:rgba(248,113,113,0.12);color:#f87171;border:1px solid rgba(248,113,113,0.3);}
.team-panel{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:20px;}
.team-panel.valid{border-color:#4ade80;box-shadow:0 0 20px rgba(74,222,128,0.1);}
.team-panel.invalid{border-color:#f87171;box-shadow:0 0 20px rgba(248,113,113,0.05);}
.section-header{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:var(--text-muted);margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--border);}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(74,222,128,0.06);font-size:13px;}
.stat-row .label{color:var(--text-muted);font-family:'DM Mono',monospace;font-size:11px;}
.stat-row .value{color:var(--text);font-weight:500;}
.page-title{font-family:'Playfair Display',serif;font-size:38px;font-weight:900;line-height:1.1;letter-spacing:-0.01em;background:linear-gradient(135deg,#e8f0e8 0%,#4ade80 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.page-subtitle{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-muted);margin-top:4px;}
.bio-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:20px;margin-bottom:16px;}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}
.info-item{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px 14px;}
.info-item .ilabel{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-muted);margin-bottom:4px;}
.info-item .ivalue{font-family:'DM Mono',monospace;font-size:15px;font-weight:500;color:var(--text);}
.info-item .ivalue.highlight{color:var(--green);font-family:'Playfair Display',serif;font-size:20px;font-weight:900;}
.suggest-card{background:var(--surface2);border:1px solid rgba(74,222,128,0.12);border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.suggest-card .sname{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;}
.suggest-card .smeta{font-family:'DM Mono',monospace;font-size:10px;color:var(--text-muted);}
@media(max-width:768px){.mobile-team-top{display:block!important;}.desktop-team-only{display:none!important;}}
@media(min-width:769px){.mobile-team-top{display:none!important;}.desktop-team-only{display:block!important;}}
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ──

@st.cache_data
def get_available_images():
    if not os.path.isdir("images"):
        return set()
    return {os.path.splitext(f)[0] for f in os.listdir("images") if f.lower().endswith(".jpg")}

@st.cache_data
def load_players():
    df = pd.read_csv("consolidated_player_data_2026.csv")
    pct_cols = [c for c in df.columns if "percentage" in c.lower() or c.lower().endswith("_pct")]
    for col in pct_cols:
        if col in df.columns and df[col].dropna().max() <= 1.0:
            df[col] = df[col] * 100
    df = compute_value_scores(df)
    df["risk"] = df["odds"].apply(classify_risk)
    df["implied_prob"] = 1 / (df["odds"] + 1)
    return df

@st.cache_data
def load_csv_safe(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

# ── BUSINESS LOGIC ──

def minmax(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - mn) / (mx - mn)

def compute_value_scores(df):
    df = df.copy()
    for c in ["avg_round","cuts_made_percentage","masters_wins","rounds_under_par_percentage","best_finish_position"]:
        if c not in df.columns:
            df[c] = 0
    df["_n_avg_round"]   = 1 - minmax(df["avg_round"])
    df["_n_cuts"]        = minmax(df["cuts_made_percentage"])
    df["_n_wins"]        = minmax(df["masters_wins"])
    df["_n_rup"]         = minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"] = 1 - minmax(df["best_finish_position"])
    df["value_score"] = (
        0.30 * df["_n_avg_round"] + 0.20 * df["_n_cuts"] +
        0.20 * df["_n_wins"]      + 0.15 * df["_n_rup"] +
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

def combined_odds(players_df):
    return players_df["odds"].sum()

def team_strength(players_df):
    return players_df["value_score"].sum()

SORT_ASC = {
    "odds":True,"age":True,"avg_round":True,
    "value_score":False,"cuts_made_percentage":False,
    "masters_wins":False,"rounds_under_par_percentage":False,
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

def best_finish_display(val):
    try:
        v = int(float(val))
        return str(v) if v > 0 else "Rookie"
    except:
        return "Rookie"

def fmt_currency(val):
    try:
        return f"${float(val):,.0f}"
    except:
        return "—"

# ── SESSION STATE ──

def init_state():
    defaults = {
        "selected_ids":[], "page":"Player Picker", "profile_id":None,
        "filter_odds_range":None,"filter_age_range":None,
        "filter_countries":[],"filter_masters_winners_only":False,
        "filter_cuts_range":None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── SIDEBAR ──

def render_sidebar(df):
    with st.sidebar:
        st.markdown('<div class="page-title" style="font-size:24px;">⛳ Masters 2026</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Decision Support Tool</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
        pages = ["Player Picker","Player Profile","Score & Risk","Historical Dashboard"]
        icons = {"Player Picker":"⬜","Player Profile":"👤","Score & Risk":"📈","Historical Dashboard":"📊"}
        for p in pages:
            if st.button(f"{icons[p]}  {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()
        st.markdown("---")

        if st.session_state.page == "Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)

            odds_min_abs = int(df["odds"].min())
            odds_max_abs = int(df["odds"].max())
            if st.session_state.filter_odds_range is None:
                st.session_state.filter_odds_range = (odds_min_abs, odds_max_abs)
            st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;color:#7a9a7a;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Odds Range</div>', unsafe_allow_html=True)
            oc1, oc2 = st.columns(2)
            with oc1:
                odds_lo = st.number_input("Min", min_value=odds_min_abs, max_value=odds_max_abs,
                    value=st.session_state.filter_odds_range[0], step=5, key="odds_lo", label_visibility="visible")
            with oc2:
                odds_hi = st.number_input("Max", min_value=odds_min_abs, max_value=odds_max_abs,
                    value=st.session_state.filter_odds_range[1], step=5, key="odds_hi", label_visibility="visible")
            odds_range = (min(odds_lo, odds_hi), max(odds_lo, odds_hi))
            st.session_state.filter_odds_range = odds_range

            age_min_abs = int(df["age"].min())
            age_max_abs = int(df["age"].max())
            if st.session_state.filter_age_range is None:
                st.session_state.filter_age_range = (age_min_abs, age_max_abs)
            st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;color:#7a9a7a;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Age Range</div>', unsafe_allow_html=True)
            ac1, ac2 = st.columns(2)
            with ac1:
                age_lo = st.number_input("Min", min_value=age_min_abs, max_value=age_max_abs,
                    value=st.session_state.filter_age_range[0], step=1, key="age_lo", label_visibility="visible")
            with ac2:
                age_hi = st.number_input("Max", min_value=age_min_abs, max_value=age_max_abs,
                    value=st.session_state.filter_age_range[1], step=1, key="age_hi", label_visibility="visible")
            age_range = (min(age_lo, age_hi), max(age_lo, age_hi))
            st.session_state.filter_age_range = age_range

            countries = sorted(df["country"].dropna().unique().tolist())
            selected_countries = st.multiselect("Country", countries,
                default=st.session_state.filter_countries, key="country_select")
            st.session_state.filter_countries = selected_countries

            masters_winners_only = st.toggle("Masters winners only",
                value=st.session_state.filter_masters_winners_only, key="winners_toggle")
            st.session_state.filter_masters_winners_only = masters_winners_only

            cuts_min_abs = float(df["cuts_made_percentage"].min())
            cuts_max_abs = float(df["cuts_made_percentage"].max())
            if st.session_state.filter_cuts_range is None:
                st.session_state.filter_cuts_range = (cuts_min_abs, cuts_max_abs)
            st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;color:#7a9a7a;letter-spacing:0.1em;margin:8px 0 4px;text-transform:uppercase;">Cuts Made %</div>', unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                cuts_lo = st.number_input("Min", min_value=cuts_min_abs, max_value=cuts_max_abs,
                    value=st.session_state.filter_cuts_range[0], step=5.0, key="cuts_lo",
                    format="%.0f", label_visibility="visible")
            with cc2:
                cuts_hi = st.number_input("Max", min_value=cuts_min_abs, max_value=cuts_max_abs,
                    value=st.session_state.filter_cuts_range[1], step=5.0, key="cuts_hi",
                    format="%.0f", label_visibility="visible")
            cuts_range = (min(cuts_lo, cuts_hi), max(cuts_lo, cuts_hi))
            st.session_state.filter_cuts_range = cuts_range

            return {"odds_range":odds_range,"age_range":age_range,"countries":selected_countries,
                    "masters_winners_only":masters_winners_only,"cuts_range":cuts_range}
    return {}

# ── PLAYER PICKER ──

def render_player_picker(df, filters):
    fdf = df.copy()
    fdf = fdf[fdf["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"]:
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

            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"""
                <div class="player-card" style="{card_border}">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{row.get('country','—')} · Age {int(row['age'])} · {risk_badge_html(row['risk'])}</div>
                    <div style="display:flex;gap:24px;margin-top:10px;align-items:flex-end;">
                        <div><div class="sub">ODDS</div><div class="odds">{int(row['odds'])}/1</div></div>
                        <div><div class="sub">VALUE</div><div style="font-size:18px;font-family:'DM Mono';color:var(--text);">{row['value_score']:.3f}</div></div>
                        <div><div class="sub">CUTS MADE</div><div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{row['cuts_made_percentage']:.0f}%</div></div>
                        <div><div class="sub">AVG RND</div><div style="font-size:15px;font-family:'DM Mono';color:var(--text);">{avg_rnd_display}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button("👤", key=f"prof_{pid}", help="View profile"):
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
    c_odds = combined_odds(selected_df) if n > 0 else 0
    t_strength = team_strength(selected_df) if n > 0 else 0
    is_valid = (n == 3) and (c_odds >= 150)
    panel_cls = "valid" if is_valid else ("invalid" if n == 3 else "")

    st.markdown(f'<div class="team-panel {panel_cls}">', unsafe_allow_html=True)
    if n == 0:
        st.markdown('<div style="color:var(--text-muted);font-family:\'DM Mono\';font-size:12px;text-align:center;padding:20px 0;">Select 3 golfers to build your team</div>', unsafe_allow_html=True)
    else:
        for _, row in selected_df.iterrows():
            pid = row["id"]
            c1, c2, c3 = st.columns([5, 1, 1])
            with c1:
                st.markdown(f"""
                <div style="padding:8px 0;border-bottom:1px solid var(--border);">
                    <div style="font-family:'Playfair Display';font-size:14px;font-weight:700;">{row['first_name']} {row['last_name']}</div>
                    <div style="font-family:'DM Mono';font-size:10px;color:var(--text-muted);">{risk_badge_html(row['risk'])} &nbsp; {int(row['odds'])}/1 &nbsp; score:{row['value_score']:.3f}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("👤", key=f"panel_prof_{context}_{pid}", help="View profile"):
                    st.session_state.profile_id = pid
                    st.session_state.page = "Player Profile"
                    st.rerun()
            with c3:
                if st.button("✕", key=f"panel_rem_{context}_{pid}", help=f"Remove {row['first_name']}"):
                    st.session_state.selected_ids.remove(pid)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        odds_color = "#4ade80" if c_odds >= 150 else "#f87171"
        st.markdown(f"""
        <div class="stat-row"><span class="label">COMBINED ODDS</span><span class="value" style="color:{odds_color};font-family:'Playfair Display';font-size:20px;font-weight:900;">{int(c_odds)}</span></div>
        <div class="stat-row"><span class="label">TEAM STRENGTH</span><span class="value" style="font-family:'DM Mono';">{t_strength:.3f}</span></div>
        <div class="stat-row"><span class="label">SLOTS FILLED</span><span class="value" style="font-family:'DM Mono';">{n} / 3</span></div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if n == 3 and not is_valid:
            st.markdown('<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.3);border-radius:6px;padding:10px;font-family:\'DM Mono\';font-size:11px;color:#f87171;">⚠ Combined odds must be ≥ 150 for a valid entry.</div>', unsafe_allow_html=True)
        elif is_valid:
            st.markdown('<div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.3);border-radius:6px;padding:10px;font-family:\'DM Mono\';font-size:11px;color:#4ade80;">✓ Valid team — ready to submit.</div>', unsafe_allow_html=True)
            st.markdown("""<div style="margin-top:10px;text-align:center;">
                <a href="https://eoghanobrien-bit.github.io/masters-sweepstake/" target="_blank"
                   style="display:inline-block;padding:10px 20px;background:rgba(74,222,128,0.12);border:1px solid rgba(74,222,128,0.5);border-radius:6px;font-family:'DM Mono';font-size:12px;color:#4ade80;text-decoration:none;letter-spacing:0.06em;">
                    ⛳ Submit your team →
                </a></div>""", unsafe_allow_html=True)
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


# ── PLAYER PROFILE ──

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
            st.markdown(f'<div style="width:120px;height:120px;border-radius:50%;background:var(--surface2);border:2px solid var(--border);display:flex;align-items:center;justify-content:center;font-family:\'Playfair Display\';font-size:36px;color:var(--text-muted);">{initials}</div>', unsafe_allow_html=True)

    with top_mid:
        world_rank = f" &nbsp;·&nbsp; World Rank #{int(row['world_ranking'])}" if pd.notna(row.get('world_ranking')) else ""
        st.markdown(f"""
        <div style="padding-top:8px;">
            <div style="font-family:'Playfair Display';font-size:32px;font-weight:900;line-height:1.1;">{row['first_name']} {row['last_name']}</div>
            <div style="font-family:'DM Mono';font-size:11px;color:var(--text-muted);margin-top:6px;letter-spacing:0.08em;">{row.get('country','—')} &nbsp;·&nbsp; Age {int(row['age'])}{world_rank}</div>
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
    tab_overview, tab_masters, tab_radar = st.tabs(["📋 Overview", "🏆 Masters Record & Stats", "🎯 Radar"])
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
        if pd.notna(row.get("world_ranking")):
            grid_items.append(("WORLD RANKING", f"#{int(row['world_ranking'])}", True))
        if pd.notna(row.get("age")):
            grid_items.append(("AGE", str(int(row["age"])), False))
        if pd.notna(row.get("turned_pro")):
            grid_items.append(("TURNED PRO", str(int(row["turned_pro"])), False))
        if pd.notna(row.get("country")):
            grid_items.append(("COUNTRY", str(row["country"]), False))
        if pd.notna(row.get("college")) and str(row.get("college","")) not in ["","nan"]:
            grid_items.append(("COLLEGE", str(row["college"]), False))
        if grid_items:
            html = '<div class="info-grid">'
            for label, val, highlight in grid_items:
                cls = "highlight" if highlight else ""
                html += f'<div class="info-item"><div class="ilabel">{label}</div><div class="ivalue {cls}">{val}</div></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

        implied = row["implied_prob"] * 100
        st.markdown(f"""
        <div class="bio-card" style="margin-top:8px;">
            <div class="section-header" style="border:none;margin-bottom:6px;">ODDS CONTEXT</div>
            <div style="display:flex;gap:20px;flex-wrap:wrap;">
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">ODDS</div>
                     <div style="font-family:'Playfair Display';font-size:24px;font-weight:900;color:var(--green);">{int(row['odds'])}/1</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">IMPLIED PROB</div>
                     <div style="font-family:'DM Mono';font-size:20px;font-weight:500;">{implied:.1f}%</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">VALUE SCORE</div>
                     <div style="font-family:'DM Mono';font-size:20px;font-weight:500;">{row['value_score']:.3f}</div></div>
                <div><div style="font-family:'DM Mono';font-size:9px;letter-spacing:0.1em;color:var(--text-muted);">RISK TIER</div>
                     <div style="margin-top:4px;">{risk_badge_html(row['risk'])}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
        overview_text = str(row.get('overview', row.get('bio', '')))
        if overview_text not in ['', 'nan', 'None']:
            st.markdown(f'<div class="bio-card" style="line-height:1.7;font-size:14px;color:var(--text-muted);">{overview_text}</div>', unsafe_allow_html=True)
        else:
            st.info("No biography available for this player.")


def _render_profile_combined(row, df):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-header">Augusta Record</div>', unsafe_allow_html=True)
        masters_stats = [
            ("MASTERS WINS",         "masters_wins",                lambda v: str(int(v)),              True),
            ("APPEARANCES",          "masters_appearances",         lambda v: str(int(v)),              False),
            ("BEST FINISH",          "best_finish_position",        best_finish_display,                True),
            ("CUTS MADE",            "cuts_made_percentage",        lambda v: f"{v:.0f}%",              False),
            ("TOTAL ROUNDS",         "total_rounds_played",         lambda v: str(int(v)),              False),
            ("AVG ROUND SCORE",      "avg_round",                   lambda v: f"{v:.2f}" if v > 0 else "Rookie", False),
            ("LOWEST ROUND",         "lowest_round",                lambda v: str(int(v)) if v > 0 else "—", False),
            ("HIGHEST ROUND",        "highest_round",               lambda v: str(int(v)) if v > 0 else "—", False),
            ("ROUNDS UNDER PAR %",   "rounds_under_par_percentage", lambda v: f"{v:.0f}%",              False),
            ("AVG FINISH POSITION",  "avg_finish_position",         lambda v: f"{v:.1f}",               False),
            ("MASTERS EARNINGS",     "masters_earnings",            fmt_currency,                       False),
            ("TOTAL PRIZE MONEY",    "total_prize_money",           fmt_currency,                       False),
            ("CAREER EARNINGS",      "career_earnings",             fmt_currency,                       False),
        ]
        html = '<div class="info-grid">'
        found = False
        for label, col_name, fmt_fn, highlight in masters_stats:
            val = row.get(col_name)
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                try:
                    display = fmt_fn(val)
                    cls = "highlight" if highlight else ""
                    html += f'<div class="info-item"><div class="ilabel">{label}</div><div class="ivalue {cls}">{display}</div></div>'
                    found = True
                except Exception:
                    pass
        html += '</div>'
        if found:
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No Masters record data available.")

    with col2:
        st.markdown('<div class="section-header">Odds & Value</div>', unsafe_allow_html=True)
        badge_html = risk_badge_html(row['risk'])
        html = f"""<div class="info-grid">
        <div class="info-item"><div class="ilabel">ODDS</div><div class="ivalue highlight">{int(row['odds'])}/1</div></div>
        <div class="info-item"><div class="ilabel">IMPLIED PROBABILITY</div><div class="ivalue">{row['implied_prob']*100:.1f}%</div></div>
        <div class="info-item"><div class="ilabel">VALUE SCORE</div><div class="ivalue">{row['value_score']:.3f}</div></div>
        <div class="info-item"><div class="ilabel">RISK TIER</div><div class="ivalue" style="font-size:13px;">{badge_html}</div></div>
        </div>"""
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Odds vs Field</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df["odds"], nbinsx=25,
            marker_color="rgba(74,222,128,0.25)",
            marker_line_color="rgba(74,222,128,0.5)", marker_line_width=1))
        fig.add_vline(x=row["odds"], line_color="#4ade80", line_width=2, line_dash="dash",
            annotation_text=f"{row['first_name']} {row['last_name']} ({int(row['odds'])}/1)",
            annotation_font_color="#4ade80", annotation_font_size=10)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,17,0.4)",
            font=dict(family="DM Sans", color="#e8f0e8", size=11),
            xaxis=dict(title="Odds", gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
            yaxis=dict(title="# Players", gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)"),
            margin=dict(l=40,r=20,t=20,b=40), height=220, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def _render_profile_radar(row, df):
    norm_cols = [c for c in df.columns if c.endswith("_norm")]
    if not norm_cols:
        st.info("No normalised (_norm) columns found in player data.")
        return

    # Map norm col -> raw col for readable tooltips
    raw_col_map = {}
    for nc in norm_cols:
        raw_name = nc[:-5]
        raw_col_map[nc] = raw_name if raw_name in df.columns else nc

    player_options = ["Field Average"] + df.apply(lambda r: f"{r['first_name']} {r['last_name']}", axis=1).tolist()
    compare_label = st.selectbox("Compare against", player_options, index=0, key="radar_compare")

    labels = [c.replace("_norm","").replace("_"," ").title() for c in norm_cols]
    values = [float(row[c]) for c in norm_cols]

    def get_raw_display(r, nc):
        rc = raw_col_map[nc]
        v = r.get(rc, r[nc])
        if isinstance(v, float):
            return f"{v:.2f}"
        return str(v)

    raw_vals = [get_raw_display(row, nc) for nc in norm_cols]
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]
    raw_closed = raw_vals + [raw_vals[0]]

    if compare_label == "Field Average":
        compare_vals = [float(df[c].mean()) for c in norm_cols]
        compare_raw_vals = []
        for nc in norm_cols:
            rc = raw_col_map[nc]
            avg = df[rc].mean() if rc in df.columns else df[nc].mean()
            compare_raw_vals.append(f"{float(avg):.2f}")
        compare_name = "Field Average"
        compare_color = "#fbbf24"
        compare_fill = "rgba(251,191,36,0.06)"
    else:
        crow = df[df.apply(lambda r: f"{r['first_name']} {r['last_name']}" == compare_label, axis=1)].iloc[0]
        compare_vals = [float(crow[c]) for c in norm_cols]
        compare_raw_vals = [get_raw_display(crow, nc) for nc in norm_cols]
        compare_name = compare_label
        compare_color = "#f87171"
        compare_fill = "rgba(248,113,113,0.06)"

    compare_closed = compare_vals + [compare_vals[0]]
    compare_raw_closed = compare_raw_vals + [compare_raw_vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=compare_closed, theta=labels_closed, fill="toself",
        fillcolor=compare_fill, line=dict(color=compare_color, width=1.5, dash="dot"),
        name=compare_name,
        customdata=compare_raw_closed,
        hovertemplate="<b>%{theta}</b><br>%{customdata}<extra>" + compare_name + "</extra>",
    ))
    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=labels_closed, fill="toself",
        fillcolor="rgba(74,222,128,0.12)", line=dict(color="#4ade80", width=2),
        marker=dict(color="#4ade80", size=5),
        name=f"{row['first_name']} {row['last_name']}",
        customdata=raw_closed,
        hovertemplate="<b>%{theta}</b><br>%{customdata}<extra>" + f"{row['first_name']} {row['last_name']}" + "</extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(17,24,17,0)",
            radialaxis=dict(visible=True, range=[0,1], gridcolor="rgba(74,222,128,0.15)",
                linecolor="rgba(74,222,128,0.15)", tickfont=dict(color="#7a9a7a", size=9, family="DM Mono")),
            angularaxis=dict(gridcolor="rgba(74,222,128,0.12)", linecolor="rgba(74,222,128,0.12)",
                tickfont=dict(color="#e8f0e8", size=10, family="DM Sans"))),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60,r=60,t=40,b=40), height=480, showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8f0e8", size=10)),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── SCORE & RISK OVERVIEW ──

def render_score_risk_overview(df):
    st.markdown('<div class="section-header">Field Overview</div>', unsafe_allow_html=True)
    col_metrics = st.columns(4)
    with col_metrics[0]: st.metric("Total Players", len(df))
    with col_metrics[1]: st.metric("Safe (<25/1)", len(df[df["risk"]=="Safe"]))
    with col_metrics[2]: st.metric("Balanced (25–60/1)", len(df[df["risk"]=="Balanced"]))
    with col_metrics[3]: st.metric("High Risk (>60/1)", len(df[df["risk"]=="High Risk"]))

    st.markdown("---")
    RISK_COLORS = {"Safe":"#4ade80","Balanced":"#fbbf24","High Risk":"#f87171"}
    row1_l, row1_r = st.columns(2, gap="large")

    with row1_l:
        st.markdown("**Value Score vs Odds**")
        fig = go.Figure()
        for risk_tier, grp in df.groupby("risk"):
            fig.add_trace(go.Scatter(
                x=grp["odds"], y=grp["value_score"], mode="markers", name=risk_tier,
                marker=dict(color=RISK_COLORS.get(risk_tier,"#4ade80"), size=8, opacity=0.8,
                    line=dict(color="#0a0f0a",width=1)),
                text=grp["first_name"]+" "+grp["last_name"],
                hovertemplate="<b>%{text}</b><br>Odds: %{x}/1<br>Value: %{y:.3f}<extra></extra>",
            ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,17,0.4)",
            font=dict(family="DM Sans",color="#e8f0e8",size=11),
            xaxis=dict(title="Odds",gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            yaxis=dict(title="Value Score",gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            margin=dict(l=40,r=20,t=30,b=40), height=380,
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with row1_r:
        st.markdown("**Risk Tier Breakdown**")
        risk_counts = df["risk"].value_counts().reindex(["Safe","Balanced","High Risk"],fill_value=0).reset_index()
        risk_counts.columns = ["Risk","Count"]
        fig = go.Figure(go.Bar(x=risk_counts["Risk"], y=risk_counts["Count"],
            marker_color=["#4ade80","#fbbf24","#f87171"],
            text=risk_counts["Count"], textposition="outside",
            textfont=dict(color="#e8f0e8",size=12)))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,17,0.4)",
            font=dict(family="DM Sans",color="#e8f0e8",size=11),
            xaxis=dict(gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            yaxis=dict(gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            margin=dict(l=40,r=20,t=30,b=40), height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    row2_l, row2_r = st.columns(2, gap="large")

    with row2_l:
        st.markdown("**Cuts Made % vs Avg Round Score**")
        fig = go.Figure()
        for risk_tier, grp in df.groupby("risk"):
            nr = grp[grp["avg_round"] > 0]
            if not nr.empty:
                fig.add_trace(go.Scatter(
                    x=nr["cuts_made_percentage"], y=nr["avg_round"], mode="markers", name=risk_tier,
                    marker=dict(color=RISK_COLORS.get(risk_tier,"#4ade80"), size=8, opacity=0.8,
                        line=dict(color="#0a0f0a",width=1)),
                    text=nr["first_name"]+" "+nr["last_name"],
                    hovertemplate="<b>%{text}</b><br>Cuts Made: %{x:.0f}%<br>Avg Round: %{y:.2f}<extra></extra>",
                ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,17,0.4)",
            font=dict(family="DM Sans",color="#e8f0e8",size=11),
            xaxis=dict(title="Cuts Made %",gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            yaxis=dict(title="Avg Round Score",gridcolor="rgba(74,222,128,0.08)",linecolor="rgba(74,222,128,0.2)"),
            margin=dict(l=40,r=20,t=30,b=40), height=360,
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with row2_r:
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
    st.markdown("**How Score & Risk Are Calculated**")
    exp_l, exp_r = st.columns(2, gap="large")
    with exp_l:
        st.markdown("""<div class="bio-card" style="font-size:13px;line-height:1.8;">
<div class="section-header">VALUE SCORE FORMULA</div>
The Value Score is a weighted composite of five Masters performance metrics, each normalised 0→1 across the field:
<br><br>
<div style="font-family:'DM Mono';font-size:12px;color:#4ade80;padding:10px;background:rgba(74,222,128,0.05);border-radius:6px;border:1px solid rgba(74,222,128,0.15);">
Score = 0.30 × Avg Round Score<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.20 × Cuts Made %<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.20 × Masters Wins<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.15 × Rounds Under Par %<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + 0.15 × Best Finish Position
</div>
<br>
Higher score = stronger Augusta pedigree relative to the field. Rookies with no Masters history score 0 on most metrics.
</div>""", unsafe_allow_html=True)
    with exp_r:
        st.markdown("""<div class="bio-card" style="font-size:13px;line-height:1.8;">
<div class="section-header">RISK TIER CLASSIFICATION</div>
Risk is based on the player's pre-tournament betting odds:
<br><br>
<div style="font-family:'DM Mono';font-size:12px;padding:10px;background:rgba(74,222,128,0.05);border-radius:6px;border:1px solid rgba(74,222,128,0.15);">
<span style="color:#4ade80;">■ Safe</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Odds &lt; 25/1<br>
<span style="color:#fbbf24;">■ Balanced</span>&nbsp;&nbsp; Odds 25/1 – 60/1<br>
<span style="color:#f87171;">■ High Risk</span>&nbsp; Odds &gt; 60/1
</div>
<br>
The sweepstake requires a minimum combined team odds of 150, incentivising a mix of Safe anchors and High Risk outsiders.
<br><br>
<div class="section-header" style="margin-top:8px;">COMBINED TEAM ODDS</div>
Sum of each player's odds (e.g. 12 + 50 + 100 = 162). Must be ≥ 150 for a valid entry.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Full Field — Score & Risk Table**")
    tdf = df[["first_name","last_name","country","odds","value_score","risk",
              "cuts_made_percentage","avg_round","masters_wins","best_finish_position"]].copy()
    tdf["Player"] = tdf["first_name"]+" "+tdf["last_name"]
    tdf["Best Finish"] = tdf["best_finish_position"].apply(best_finish_display)
    tdf = tdf[["Player","country","odds","value_score","risk","cuts_made_percentage","avg_round","masters_wins","Best Finish"]]\
        .sort_values("value_score",ascending=False)
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


# ── HISTORICAL DASHBOARD ──

def _chart_layout(height=380, xaxis=None, yaxis=None, extra=None):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,17,0.4)",
        font=dict(family="DM Sans", color="#e8f0e8", size=11),
        margin=dict(l=40, r=20, t=40, b=40), height=height,
    )
    _x = dict(gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)")
    _y = dict(gridcolor="rgba(74,222,128,0.08)", linecolor="rgba(74,222,128,0.2)")
    if xaxis: _x.update(xaxis)
    if yaxis: _y.update(yaxis)
    layout["xaxis"] = _x
    layout["yaxis"] = _y
    if extra: layout.update(extra)
    return layout


def render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams):
    st.markdown('<div class="section-header">Historical Dashboard</div>', unsafe_allow_html=True)

    row1_l, row1_r = st.columns(2, gap="large")

    with row1_l:
        st.markdown("**Most Picked Golfers**")
        if not hist_picks.empty and "num_picks" in hist_picks.columns:
            picks_agg = (hist_picks.groupby(["first","last"],as_index=False)["num_picks"]
                         .sum().sort_values("num_picks",ascending=False).head(15))
            picks_agg["name"] = picks_agg["first"]+" "+picks_agg["last"]
            fig = go.Figure(go.Bar(x=picks_agg["num_picks"], y=picks_agg["name"], orientation="h",
                marker=dict(color=picks_agg["num_picks"],
                    colorscale=[[0,"#166534"],[1,"#4ade80"]], showscale=False)))
            fig.update_layout(**_chart_layout(380, yaxis={"autorange":"reversed"}))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No picks data available.")

    with row1_r:
        st.markdown("**Average Combined Odds by Year**")
        if not hist_odds.empty and "combined_odds" in hist_odds.columns and "year" in hist_odds.columns:
            hist_odds["combined_odds"] = pd.to_numeric(hist_odds["combined_odds"], errors="coerce")
            hist_odds["year"] = pd.to_numeric(hist_odds["year"], errors="coerce")
            odds_by_year = hist_odds.groupby("year",as_index=False)["combined_odds"].mean().sort_values("year")
            fig = go.Figure(go.Scatter(x=odds_by_year["year"], y=odds_by_year["combined_odds"],
                mode="lines+markers", line=dict(color="#4ade80",width=2.5),
                marker=dict(color="#4ade80",size=7,line=dict(color="#0a0f0a",width=2)),
                fill="tozeroy", fillcolor="rgba(74,222,128,0.07)"))
            fig.update_layout(**_chart_layout(380))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No odds data available.")

    st.markdown("---")
    row2_l, row2_r = st.columns(2, gap="large")

    with row2_l:
        st.markdown("**Combined Odds vs Finishing Position**")
        if not hist_odds.empty and "combined_odds" in hist_odds.columns and "position" in hist_odds.columns:
            sdf = hist_odds.dropna(subset=["combined_odds","position"]).copy()
            sdf["position"] = pd.to_numeric(sdf["position"], errors="coerce")
            sdf = sdf.dropna(subset=["position"])
            participant_col = next((c for c in ["participant","name","player"] if c in sdf.columns), None)
            fig = go.Figure(go.Scatter(
                x=sdf["combined_odds"], y=sdf["position"], mode="markers",
                marker=dict(color=sdf["combined_odds"],
                    colorscale=[[0,"#166534"],[1,"#4ade80"]], size=8, opacity=0.7,
                    line=dict(color="#0a0f0a",width=1)),
                text=sdf[participant_col] if participant_col else None,
                hovertemplate=("<b>%{text}</b><br>Odds: %{x}<br>Position: %{y}<extra></extra>" if participant_col
                               else "Odds: %{x}<br>Position: %{y}<extra></extra>"),
            ))
            fig.update_layout(**_chart_layout(340,
                xaxis={"title":"Combined Odds"},
                yaxis={"title":"Position","autorange":"reversed"}))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No odds/position data.")

    with row2_r:
        st.markdown("**Previous Masters Winners**")
        if not hist_winners.empty:
            show_cols = [c for c in ["year","full_name","participant"] if c in hist_winners.columns]
            st.dataframe(hist_winners[show_cols].sort_values("year",ascending=False).reset_index(drop=True),
                use_container_width=True, height=340,
                column_config={"year":st.column_config.NumberColumn("Year",format="%d"),
                               "full_name":st.column_config.TextColumn("Winner"),
                               "participant":st.column_config.TextColumn("Entered By")}, hide_index=True)
        else:
            st.info("No winners data.")

    if not hist_rounds.empty:
        st.markdown("---")
        st.markdown("**Round Score Distribution by Year**")
        score_col = next((c for c in ["score","round_score","total"] if c in hist_rounds.columns), None)
        year_col = "year" if "year" in hist_rounds.columns else None
        if score_col and year_col:
            hist_rounds[score_col] = pd.to_numeric(hist_rounds[score_col], errors="coerce")
            hist_rounds[year_col] = pd.to_numeric(hist_rounds[year_col], errors="coerce")
            fig = go.Figure()
            years = sorted(hist_rounds[year_col].dropna().unique())
            for i, yr in enumerate(years):
                shade = 0.3 + 0.7 * i / max(len(years)-1, 1)
                yr_data = hist_rounds[hist_rounds[year_col]==yr][score_col].dropna()
                fig.add_trace(go.Box(y=yr_data, name=str(int(yr)),
                    marker_color=f"rgba(74,222,128,{shade:.2f})",
                    line_color=f"rgba(74,222,128,{shade:.2f})",
                    fillcolor=f"rgba(74,222,128,{0.08+0.1*i/max(len(years)-1,1):.2f})"))
            fig.update_layout(**_chart_layout(320,
                xaxis={"title":"Year"},
                yaxis={"title":"Round Score"},
                extra={"showlegend":False}))
            st.plotly_chart(fig, use_container_width=True)

    if not hist_scores.empty:
        st.markdown("---")
        row3_l, row3_r = st.columns(2, gap="large")
        score_col = next((c for c in ["total_score","score","avg_score"] if c in hist_scores.columns), None)
        name_col  = next((c for c in ["full_name","player","name"] if c in hist_scores.columns), None)
        year_col  = "year" if "year" in hist_scores.columns else None

        with row3_l:
            st.markdown("**Top Players by Avg Score (All Years)**")
            if score_col and name_col:
                hist_scores[score_col] = pd.to_numeric(hist_scores[score_col], errors="coerce")
                agg = hist_scores.groupby(name_col,as_index=False)[score_col].mean().sort_values(score_col).head(12)
                fig = go.Figure(go.Bar(x=agg[score_col], y=agg[name_col], orientation="h",
                    marker=dict(color="#4ade80",opacity=0.8)))
                fig.update_layout(**_chart_layout(340,
                    xaxis={"title":"Avg Score"},
                    yaxis={"autorange":"reversed"}))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Expected columns not found in historical_scores.csv.")

        with row3_r:
            st.markdown("**Score Trends Over Years**")
            if score_col and year_col:
                hist_scores[year_col] = pd.to_numeric(hist_scores[year_col], errors="coerce")
                yearly_avg = hist_scores.groupby(year_col,as_index=False)[score_col].mean().sort_values(year_col)
                fig = go.Figure(go.Scatter(x=yearly_avg[year_col], y=yearly_avg[score_col],
                    mode="lines+markers", line=dict(color="#fbbf24",width=2.5),
                    marker=dict(color="#fbbf24",size=7,line=dict(color="#0a0f0a",width=2)),
                    fill="tozeroy", fillcolor="rgba(251,191,36,0.06)"))
                fig.update_layout(**_chart_layout(340,
                    xaxis={"title":"Year"},
                    yaxis={"title":"Avg Score"}))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Year/score columns not found in historical_scores.csv.")

    if not hist_teams.empty:
        st.markdown("---")
        st.markdown("**Team Score vs Position**")
        score_col       = next((c for c in ["team_score","total_score","combined_score"] if c in hist_teams.columns), None)
        pos_col         = next((c for c in ["position","finishing_position","rank"] if c in hist_teams.columns), None)
        participant_col = next((c for c in ["participant","name","player"] if c in hist_teams.columns), None)
        year_col        = "year" if "year" in hist_teams.columns else None

        if score_col and pos_col:
            tdf = hist_teams.copy()
            tdf[pos_col]   = pd.to_numeric(tdf[pos_col], errors="coerce")
            tdf[score_col] = pd.to_numeric(tdf[score_col], errors="coerce")
            tdf = tdf.dropna(subset=[score_col, pos_col])
            if year_col:
                tdf[year_col] = pd.to_numeric(tdf[year_col], errors="coerce")
            fig = go.Figure(go.Scatter(
                x=tdf[score_col], y=tdf[pos_col], mode="markers",
                marker=dict(
                    color=tdf[year_col].astype(float) if year_col else "#4ade80",
                    colorscale=[[0,"#166534"],[1,"#4ade80"]], size=9, opacity=0.75,
                    line=dict(color="#0a0f0a",width=1),
                    colorbar=dict(title="Year",tickfont=dict(color="#e8f0e8",size=9)) if year_col else None,
                    showscale=bool(year_col)),
                text=tdf[participant_col] if participant_col else None,
                hovertemplate=("<b>%{text}</b><br>Score: %{x}<br>Position: %{y}<extra></extra>" if participant_col
                               else "Score: %{x}<br>Position: %{y}<extra></extra>"),
            ))
            valid = tdf[[score_col,pos_col]].dropna()
            if len(valid) > 2:
                m, b = np.polyfit(valid[score_col], valid[pos_col], 1)
                xr = np.linspace(valid[score_col].min(), valid[score_col].max(), 50)
                fig.add_trace(go.Scatter(x=xr, y=m*xr+b, mode="lines",
                    line=dict(color="#f87171",width=1.5,dash="dash"), name="Trend"))
            fig.update_layout(**_chart_layout(360,
                xaxis={"title":"Team Combined Score"},
                yaxis={"title":"Finishing Position","autorange":"reversed"},
                extra={"legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10))}))
            st.plotly_chart(fig, use_container_width=True)

        if participant_col and pos_col:
            st.markdown("---")
            st.markdown("**Participant Performance Over the Years**")
            hist_teams[pos_col] = pd.to_numeric(hist_teams[pos_col], errors="coerce")
            part_stats = (hist_teams.groupby(participant_col)[pos_col]
                          .agg(["mean","min","count"])
                          .rename(columns={"mean":"Avg Position","min":"Best Position","count":"Years Entered"})
                          .sort_values("Avg Position").reset_index())
            part_stats["Avg Position"] = part_stats["Avg Position"].round(1)
            part_stats["Best Position"] = part_stats["Best Position"].fillna(0).astype(int)
            st.dataframe(part_stats, use_container_width=True, height=300, hide_index=True,
                column_config={participant_col:st.column_config.TextColumn("Participant"),
                               "Avg Position":st.column_config.NumberColumn("Avg Finish",format="%.1f"),
                               "Best Position":st.column_config.NumberColumn("Best Finish"),
                               "Years Entered":st.column_config.NumberColumn("Years Entered")})


# ── MAIN ──

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
        st.markdown('<div class="page-title">Player Picker</div><div class="page-subtitle">Masters 2026 · Build your 3-man team · Min. 150 combined odds</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_picker(df, filters)

    elif page == "Player Profile":
        st.markdown('<div class="page-title">Player Profile</div><div class="page-subtitle">Detailed stats · Augusta record · Performance radar</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_player_profile(df, available_images)

    elif page == "Score & Risk":
        st.markdown('<div class="page-title">Score & Risk</div><div class="page-subtitle">Field overview · Value vs odds · Risk analysis</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_score_risk_overview(df)

    elif page == "Historical Dashboard":
        st.markdown('<div class="page-title">Historical Dashboard</div><div class="page-subtitle">Trends, picks & winners across previous years</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_historical(hist_odds, hist_picks, hist_winners, hist_scores, hist_rounds, hist_teams)


if __name__ == "__main__":
    main()
