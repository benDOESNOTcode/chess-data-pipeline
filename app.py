import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chess Analytics", layout="wide")
st.title("♟️ Personal Chess Dashboard")

# 1. Connect to DuckDB and load the Gold Layer
@st.cache_data
def load_data():
    conn = duckdb.connect('chess.db')
    # Query the dbt fact table directly
    df = conn.execute("SELECT * FROM fact_games").df()
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data found in the database. Run your dbt models!")
else:
    # 2. Data Transformation: Extract the date from the PGN string
    # PGNs contain metadata like [Date "2026.07.14"]
    df['game_date'] = df['pgn'].str.extract(r'\[Date "(.*?)"\]')
    df['game_date'] = pd.to_datetime(df['game_date'], format='%Y.%m.%d', errors='coerce')
    
    # Sort chronologically so our line chart flows left to right
    df = df.sort_values('game_date').reset_index(drop=True)

    # 3. Build the UI Layout
    st.subheader("Gold Layer: Fact Table")
    st.dataframe(df[['game_date', 'game_type', 'white_player_name', 'white_rating', 'black_player_name', 'black_rating', 'winner']].head(10))
    st.divider()

    # 4. Plotly Visualization
    st.subheader("Rating Progression (White)")
    
    # Drop rows where game_date couldn't be parsed just for the chart
    chart_df = df.dropna(subset=['game_date', 'white_rating'])
    
    fig = px.line(
        chart_df, 
        x='game_date', 
        y='white_rating', 
        markers=True,
        title="White Rating Over Time",
        labels={'game_date': 'Date', 'white_rating': 'Rating'}
    )
    
    st.plotly_chart(fig, use_container_width=True)