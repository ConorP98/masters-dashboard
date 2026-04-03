import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load consolidated player data
@st.cache_data
def load_data():
    df = pd.read_csv("consolidated_player_data.csv")
    return df

df = load_data()

# Sidebar: select player
st.sidebar.title("Select Player")
player_name = st.sidebar.selectbox(
    "Player",
    df["display_name"].sort_values().unique()
)

# Fetch selected player row
row = df[df["display_name"] == player_name].iloc[0]

# --- PLAYER PROFILE ---
st.title(f"{row['display_name']}")

# Bio and Overview
st.markdown("## Bio")
col1, col2 = st.columns([1,2])

with col1:
    if pd.notna(row["image"]):
        st.image(row["image"], use_column_width=True)
    st.write(f"**Age:** {row['age']}")
    st.write(f"**Country:** {row['country']}")
    st.write(f"**Height:** {row['height']} cm")
    st.write(f"**Weight:** {row['weight']} kg")
    st.write(f"**Birthplace:** {row['birthplace']}")
    st.write(f"**Education:** {row['education']}")
    st.write(f"**Residence:** {row['residence']}")
    st.write(f"**Turned Pro:** {row['turned_pro']}")
    st.write(f"**Amateur:** {row['amateur']}")
    st.write(f"**Past Champion:** {row['past_champion']}")
    st.write(f"**Past Masters:** {row['past_masters']}")
    st.write(f"**Best Finish:** {row['best_finish']} ({row['best_finish_group']})")
    st.write(f"**Instagram:** {row['instagram']}")
    st.write(f"**Twitter:** {row['twitter']}")
    st.write(f"[Share Link]({row['share_url']})")

with col2:
    st.markdown("### Overview")
    if pd.notna(row["overview"]):
        st.write(row["overview"])
    else:
        st.write("No overview available.")

# --- SPIDER CHART / RADAR ---
st.markdown("## Performance Radar")

radar_metrics = [
    ("Wins", "wins_norm", lambda r: f"{r['wins']} Win{'s' if r['wins']!=1 else ''}"),
    ("Masters Wins", "masters_wins_norm", lambda r: f"{r['masters_wins']} Masters Win{'s' if r['masters_wins']!=1 else ''}"),
    ("Rounds Under Par", "rounds_under_par_percentage_norm", lambda r: f"{r['rounds_under_par']} rounds ({r['rounds_under_par_percentage']*100:.1f}%)"),
    ("Cuts Made", "cuts_made_percentage_norm", lambda r: f"{r['cuts_made']} Cuts ({r['cuts_made_percentage']*100:.1f}%)"),
    ("Avg Round", "avg_round_norm", lambda r: f"{r['avg_round']:.2f}"),
]

values_norm = [row[norm] for _, norm, _ in radar_metrics]
values_closed = values_norm + [values_norm[0]]
labels_closed = [label for label, _, _ in radar_metrics] + [radar_metrics[0][0]]
hover_text = [func(row) for _, _, func in radar_metrics] + [radar_metrics[0][2](row)]

fig_radar = go.Figure(go.Scatterpolar(
    r=values_closed,
    theta=labels_closed,
    fill="toself",
    fillcolor="rgba(74,222,128,0.12)",
    line=dict(color="#4ade80", width=2),
    marker=dict(color="#4ade80", size=5),
    text=hover_text,
    hoverinfo="text+theta"
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=40),
    height=400
)
st.plotly_chart(fig_radar, use_container_width=True)

# --- ADDITIONAL STATS TABLE ---
st.markdown("## Key Statistics")
stats_fields = [
    "tournaments_played",
    "cuts_made",
    "cuts_made_percentage",
    "rounds_played",
    "rounds_under_par",
    "rounds_under_par_percentage",
    "money_earned",
    "low_round",
    "high_round",
    "avg_round",
    "odds",
]

stats_data = {field: [row[field]] for field in stats_fields}

# Convert percentage decimals to % strings for display
for field in ["cuts_made_percentage", "rounds_under_par_percentage"]:
    stats_data[field] = [f"{row[field]*100:.1f}%" if pd.notna(row[field]) else "N/A"]

st.table(pd.DataFrame(stats_data).T.rename(columns={0:"Value"}))
