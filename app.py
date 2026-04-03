import streamlit as st
import pandas as pd
import plotly.express as px

# --- Helper Functions ---
def combined_odds(df):
    return df['combined_odds'].sum()

def team_strength(df):
    # Example: sum of scores or some metric
    return df['strength'].sum()

def risk_badge_html(risk):
    colors = {'High':'red','Medium':'orange','Low':'green'}
    return f"<span style='color:{colors.get(risk,'black')}'>{risk}</span>"

# --- Render Functions ---
def render_team_panel(df):
    st.subheader("Selected Team")
    if st.session_state.selected_ids:
        team_df = df[df.id.isin(st.session_state.selected_ids)]
        for _, row in team_df.iterrows():
            st.markdown(
                f"{row['first_name']} {row['last_name']} · Cuts Made: {row['cuts_made_percentage']:.1f}% · Rounds Under Par: {row['rounds_under_par_percentage']:.1f}% · {risk_badge_html(row['risk'])}",
                unsafe_allow_html=True
            )

        total_strength = team_strength(team_df)
        total_odds = combined_odds(team_df)

        st.write(f"Team Strength: {total_strength:.3f}")
        st.write(f"Combined Odds: {int(total_odds)}/1")

        # Minimum rules
        min_players_ok = len(team_df) == 3
        min_odds_ok = total_odds >= 150

        if min_players_ok and min_odds_ok:
            st.success("✅ Team meets all rules")
        else:
            if not min_players_ok:
                st.warning("⚠️ Team must have exactly 3 players")
            if not min_odds_ok:
                st.warning(f"⚠️ Team combined odds must be at least 150/1 (current: {int(total_odds)}/1)")

        # Deselect all button
        if st.button("Clear All"):
            st.session_state.selected_ids = []
            st.experimental_rerun()
    else:
        st.info("Add 3 players to form your team. Minimum combined odds must be 150/1.")

def render_player_picker(df):
    st.subheader("Player Picker")
    selected_name = st.selectbox("Select a player", [""] + df['full_name'].tolist())
    if selected_name:
        player_id = df[df['full_name'] == selected_name].iloc[0]['id']
        if player_id not in st.session_state.selected_ids:
            st.session_state.selected_ids.append(player_id)
        st.experimental_rerun()

def render_player_profile(df_players):
    st.subheader("Player Profile")
    # Use the first selected player if any, else default to first in DF
    selected_id = st.selectbox(
        "Select a player to view profile",
        options=df_players['id'].tolist(),
        format_func=lambda x: df_players[df_players['id']==x]['full_name'].values[0]
    )
    player = df_players[df_players['id'] == selected_id].iloc[0]
    st.markdown(f"### {player['full_name']}")
    st.write(f"Cuts Made %: {player['cuts_made_percentage']:.1f}%")
    st.write(f"Rounds Under Par %: {player['rounds_under_par_percentage']:.1f}%")
    st.write(f"Risk: {player['risk']}")

def render_historical(hist_odds, hist_picks, hist_winners):
    st.markdown("<h2 class='page-title'>Historical Masters Data</h2>", unsafe_allow_html=True)

    # Fix column case: ensure lowercase matches the DF
    hist_odds = hist_odds.rename(columns=str.lower)
    hist_picks = hist_picks.rename(columns=str.lower)
    hist_winners = hist_winners.rename(columns=str.lower)

    st.markdown("### Odds Trends")
    if 'combined_odds' in hist_odds.columns:
        fig = px.line(hist_odds, x="year", y="combined_odds", color="participant")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Historical odds data not available")

    st.markdown("### Top Picks")
    st.dataframe(hist_picks)
    st.markdown("### Winners")
    st.dataframe(hist_winners)

# --- Load Data ---
@st.cache_data
def load_data():
    # Replace with actual loading logic
    df_players = pd.read_csv("players.csv")
    df_players['full_name'] = df_players['first_name'] + " " + df_players['last_name']

    hist_odds = pd.read_csv("hist_odds.csv")
    hist_picks = pd.read_csv("hist_picks.csv")
    hist_winners = pd.read_csv("hist_winners.csv")

    return df_players, hist_odds, hist_picks, hist_winners

df_players, hist_odds, hist_picks, hist_winners = load_data()

# --- Session State ---
if 'selected_ids' not in st.session_state:
    st.session_state.selected_ids = []
if 'page' not in st.session_state:
    st.session_state.page = "Player Picker"

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Player Picker", "Player Profile", "Team Panel", "Historical Dashboard"])
st.session_state.page = page

# --- Main App ---
if st.session_state.page == "Player Picker":
    render_player_picker(df_players)
elif st.session_state.page == "Player Profile":
    render_player_profile(df_players)
elif st.session_state.page == "Team Panel":
    render_team_panel(df_players)
elif st.session_state.page == "Historical Dashboard":
    render_historical(hist_odds, hist_picks, hist_winners)
