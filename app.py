import streamlit as st
import pandas as pd
import os

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
# STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --surface: #ffffff;
  --surface2: #f5f5f5;
  --text: #111111;
  --text-muted: #555555;
  --green: #4ade80;
  --red: #f87171;
  --border: #e5e7eb;
}
.player-card {
  padding:10px;
  border:1px solid var(--border);
  border-radius:6px;
  margin-bottom:10px;
}
.name { font-weight:700; font-size:16px; }
.sub { font-size:12px; color:var(--text-muted); }
.badge { padding:2px 6px; border-radius:4px; font-size:10px; font-weight:700;}
.badge-safe { background:#4ade80;color:white;}
.badge-balanced { background:#facc15;color:white;}
.badge-high { background:#f87171;color:white;}
.team-panel { padding:10px; border:1px solid var(--border); border-radius:6px; margin-bottom:20px;}
.team-panel.valid { border-color:var(--green);}
.team-panel.invalid { border-color:var(--red);}
.stat-row { display:flex; justify-content:space-between; padding:2px 0;}
.label { font-weight:600; color:var(--text-muted);}
.value { font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_players():
    df = pd.read_csv("historical_player_data.csv")  # your actual CSV
    df = compute_value_scores(df)
    df["risk"] = df["odds"].apply(classify_risk)
    df["implied_prob"] = 1 / (df["odds"] + 1)
    return df

# ─────────────────────────────────────────────
# BUSINESS LOGIC
# ─────────────────────────────────────────────
def minmax(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5]*len(series), index=series.index)
    return (series - mn) / (mx - mn)

def compute_value_scores(df):
    df = df.copy()
    cols_needed = ["avg_round","cuts_made_percentage","masters_wins","rounds_under_par_percentage","best_finish_position"]
    for c in cols_needed:
        if c not in df.columns:
            df[c] = 0
    df["_n_avg_round"]   = 1 - minmax(df["avg_round"])
    df["_n_cuts"]        = minmax(df["cuts_made_percentage"])
    df["_n_wins"]        = minmax(df["masters_wins"])
    df["_n_rup"]         = minmax(df["rounds_under_par_percentage"])
    df["_n_best_finish"] = 1 - minmax(df["best_finish_position"])
    df["value_score"] = (0.3*df["_n_avg_round"] + 0.2*df["_n_cuts"] + 0.2*df["_n_wins"] + 0.15*df["_n_rup"] + 0.15*df["_n_best_finish"])
    df.drop(columns=[c for c in df.columns if c.startswith("_n_")], inplace=True)
    return df

def classify_risk(odds):
    if odds < 25:
        return "Safe"
    elif odds <= 60:
        return "Balanced"
    return "High Risk"

def risk_badge_html(risk):
    cls = {"Safe":"badge-safe","Balanced":"badge-balanced","High Risk":"badge-high"}.get(risk,"badge-safe")
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
        st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
        pages = ["Player Picker","Player Profile"]
        for p in pages:
            icon = {"Player Picker":"⬜","Player Profile":"👤"}[p]
            if st.button(f"{icon} {p}", key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()
        st.markdown("---")
        if st.session_state.page=="Player Picker":
            st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
            odds_min, odds_max = int(df["odds"].min()), int(df["odds"].max())
            odds_range = st.slider("Odds range", odds_min, odds_max, (odds_min, odds_max))
            age_min, age_max = int(df["age"].min()), int(df["age"].max())
            age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))
            countries = sorted(df["country"].dropna().unique().tolist())
            selected_countries = st.multiselect("Country", countries)
            masters_winners_only = st.toggle("Masters winners only", value=False)
            cuts_min, cuts_max = float(df["cuts_made_percentage"].min()), float(df["cuts_made_percentage"].max())
            cuts_range = st.slider("Cuts made %", cuts_min, cuts_max, (cuts_min, cuts_max))
            return {
                "odds_range": odds_range,
                "age_range": age_range,
                "countries": selected_countries,
                "masters_winners_only": masters_winners_only,
                "cuts_range": cuts_range
            }
    return {}

# ─────────────────────────────────────────────
# PLAYER PICKER PAGE
# ─────────────────────────────────────────────
def render_player_picker(df, filters):
    fdf = df[df["odds"].between(*filters["odds_range"])]
    fdf = fdf[fdf["age"].between(*filters["age_range"])]
    if filters["countries"]:
        fdf = fdf[fdf["country"].isin(filters["countries"])]
    if filters["masters_winners_only"]:
        fdf = fdf[df["masters_wins"]>0]
    fdf = fdf[fdf["cuts_made_percentage"].between(*filters["cuts_range"])]

    left_col,right_col = st.columns([2,1], gap="large")
    with left_col:
        st.markdown('<div class="section-header">Player Pool</div>', unsafe_allow_html=True)
        st.caption(f"{len(fdf)} players · {len(st.session_state.selected_ids)}/3 selected")
        sort_col = st.selectbox("Sort by", ["odds","value_score","age","cuts_made_percentage","masters_wins"], label_visibility="collapsed")
        fdf = fdf.sort_values(sort_col, ascending=(sort_col=="odds"))
        for _, row in fdf.iterrows():
            pid=row["id"]
            is_selected = pid in st.session_state.selected_ids
            col_a,col_b = st.columns([4,1])
            with col_a:
                st.markdown(f"""
                <div class="player-card">
                    <div class="name">{row['first_name']} {row['last_name']}</div>
                    <div class="sub">{row.get('country','—')} · Age {int(row['age'])} · {risk_badge_html(row['risk'])}</div>
                    <div style="display:flex;gap:12px;margin-top:8px;">
                        <div><div class="sub">ODDS</div><div>{int(row['odds'])}/1</div></div>
                        <div><div class="sub">VALUE</div><div>{row['value_score']:.3f}</div></div>
                        <div><div class="sub">CUTS MADE</div><div>{row['cuts_made_percentage']:.0f}%</div></div>
                        <div><div class="sub">AVG RND</div><div>{row['avg_round']:.1f}</div></div>
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
                    disabled = len(st.session_state.selected_ids)>=3
                    if st.button("+ Add", key=f"add_{pid}", disabled=disabled):
                        st.session_state.selected_ids.append(pid)
                        st.rerun()
    with right_col:
        render_team_panel(df)

def render_team_panel(df):
    st.markdown('<div class="section-header">Your Team</div>', unsafe_allow_html=True)
    selected_df = df[df["id"].isin(st.session_state.selected_ids)]
    n = len(st.session_state.selected_ids)
    c_odds = combined_odds(selected_df) if n>0 else 0
    t_strength = team_strength(selected_df) if n>0 else 0
    is_valid = (n==3) and (c_odds>=150)
    panel_cls = "valid" if is_valid else ("invalid" if n==3 else "")
    st.markdown(f'<div class="team-panel {panel_cls}">', unsafe_allow_html=True)
    if n==0:
        st.markdown('<div style="text-align:center;padding:20px;color:var(--text-muted);">Select 3 golfers to build your team</div>', unsafe_allow_html=True)
    else:
        for _,row in selected_df.iterrows():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--border);">
                <div>
                    <div style="font-weight:700;">{row['first_name']} {row['last_name']}</div>
                    <div style="font-size:10px;color:var(--text-muted);">{risk_badge_html(row['risk'])} · score: {row['value_score']:.3f}</div>
                </div>
                <div style="font-weight:900;color:var(--green);">{int(row['odds'])}/1</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-row"><span class="label">COMBINED ODDS</span><span class="value" style="color:{'#4ade80' if c_odds>=150 else '#f87171'};">{int(c_odds)}</span></div>
        <div class="stat-row"><span class="label">TEAM STRENGTH</span><span class="value">{t_strength:.3f}</span></div>
        <div class="stat-row"><span class="label">SLOTS FILLED</span><span class="value">{n} / 3</span></div>
        """, unsafe_allow_html=True)
        if n==3 and not is_valid:
            st.markdown("""<div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.3);border-radius:6px;padding:10px;color:#f87171;">⚠ Combined odds must be ≥ 150 for a valid entry.</div>""", unsafe_allow_html=True)
        elif is_valid:
            st.markdown("""<div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.3);border-radius:6px;padding:10px;color:#4ade80;">✓ Valid team — ready to submit.</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if n>0:
        if st.button("Clear team", use_container_width=True):
            st.session_state.selected_ids = []
            st.rerun()

# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────
def render_player_profile(df):
    player_options = df.apply(lambda r: f"{r['first_name']} {r['last_name']}", axis=1).tolist()
    player_ids = df["id"].tolist()
    default_idx = player_ids.index(st.session_state.profile_id) if st.session_state.profile_id in player_ids else 0
    chosen_label = st.selectbox("Select player", player_options, index=default_idx)
    row = df.iloc[player_options.index(chosen_label)]
    st.session_state.profile_id = row["id"]

    left, right = st.columns([1,2], gap="large")
    with left:
        img_path = f"images/{row['first_name']} {row['last_name']}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, width=180)
        else:
            initials = f"{row['first_name'][0]}{row['last_name'][0]}"
            st.markdown(f"<div style='width:120px;height:120px;border-radius:50%;background:var(--surface2);display:flex;align-items:center;justify-content:center;font-size:36px;color:var(--text-muted);'>{initials}</div>", unsafe_allow_html=True)

        stats = [
            ("Odds", f"{int(row['odds'])}/1"),
            ("Value Score", f"{row['value_score']:.3f}"),
            ("Masters Wins", f"{int(row.get('masters_wins',0))}"),
            ("Cuts Made", f"{row.get('cuts_made_percentage',0):.0f}%"),
            ("Avg Round", f"{row.get('avg_round',0):.2f}"),
            ("Rounds Under Par %", f"{row.get('rounds_under_par_percentage',0):.1f}%"),
            ("Best Finish Pos", f"{row.get('best_finish_position','-')}"),
            ("Money Earned", f"${row.get('money_earned',0):,.0f}"),
            ("Implied Prob", f"{row['implied_prob']*100:.1f}%")
        ]
        for label,val in stats:
            st.markdown(f"<div class='stat-row'><span class='label'>{label}</span><span class='value'>{val}</span></div>", unsafe_allow_html=True)

        if row["id"] not in st.session_state.selected_ids:
            if len(st.session_state.selected_ids)<3:
                if st.button("+ Add to team", use_container_width=True):
                    st.session_state.selected_ids.append(row["id"])
                    st.rerun()
        else:
            if st.button("✕ Remove from team", use_container_width=True):
                st.session_state.selected_ids.remove(row["id"])
                st.rerun()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
players_df = load_players()
filters = render_sidebar(players_df)

if st.session_state.page=="Player Picker":
    render_player_picker(players_df, filters)
elif st.session_state.page=="Player Profile":
    render_player_profile(players_df)
