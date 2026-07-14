import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# Set up the page layout
st.set_page_config(page_title="Chess Analytics", layout="wide")
st.title("♟️ Chess Performance Dashboard")

# 1. Connect and Cache the Data
@st.cache_data
def load_data():
    # Connect to the exact database your dbt models live in
    con = duckdb.connect('chess_dbt/dev.duckdb', read_only=True)
    
    # Query your Gold Layer Fact Table
    df = con.execute("SELECT * FROM main.fact_games").df()
    con.close()
    return df

df = load_data()

# 2. Build Top-Level Metric Cards
st.subheader("Lifetime Stats")
col1, col2, col3 = st.columns(3)

total_games = len(df)
# Adjust these based on how Copilot structured your 'result' or 'winner' column
wins = len(df[df['result'] == 'win']) 
win_rate = (wins / total_games) * 100 if total_games > 0 else 0

with col1:
    st.metric("Total Games Played", total_games)
with col2:
    st.metric("Total Wins", wins)
with col3:
    st.metric("Overall Win Rate", f"{win_rate:.1f}%")

# 3. Add a Plotly Visualization
st.markdown("---")
st.subheader("Rating Over Time")

# Simple line chart mapping your rating progression
fig = px.line(df, x='game_date', y='white_rating', title="White Rating Trajectory")
st.plotly_chart(fig, use_container_width=True)

# 4. Show the Raw Gold Data
with st.expander("View Underlying Fact Table"):
    st.dataframe(df)