import streamlit as st
import pandas as pd
import json
import os
import altair as alt

json_dir = 'jsons'

def load_league_data():
    league_data = {}
    for league in os.listdir(json_dir):
        if league.endswith('.json'):
            with open(os.path.join(json_dir, league), 'r', encoding='utf-8') as file:
                data = json.load(file)
                league_name = league.replace('.json', '')
                league_data[league_name] = pd.DataFrame(data)
    return league_data

league_data = load_league_data()

st.set_page_config(layout="wide")
st.header("Player Comparison Dashboard")

with st.sidebar:
    st.header("Select League and Players")

    league_names = list(league_data.keys())
    selected_league = st.selectbox("Select League", league_names)

    df = league_data[selected_league]

    players = st.multiselect("Select Players", df.index)

if players:
    filtered_df = df[df.index.isin(players)]
    st.write(f"Comparing selected players in {selected_league} league:")

    # 2 kolon için Streamlit columns kullanımı
    num_cols = 2
    cols = st.columns(num_cols)

    # Her kolon için bir grafik oluştur
    for i, column in enumerate(filtered_df.columns):
        if column != 'Oyuncu Resmi': 
            data = filtered_df[column].reset_index()
            data.columns = ['Player', 'Value']
            data = data.sort_values(by='Value', ascending=False)

            # Her grafiği sırasıyla iki kolona yerleştir
            with cols[i % num_cols]:
                st.subheader(f"{column} Comparison")

                chart = alt.Chart(data).mark_bar().encode(
                    x=alt.X('Player:N', sort=None, axis=alt.Axis(labelAngle=0)),
                    y='Value:Q',
                    color='Value:O',
                ).properties(width=600, height=400)

                text = chart.mark_text(
                    align='center',
                    baseline='bottom',
                    dy=-5,
                    fontSize=16
                ).encode(
                    text='Value:O'
                )

                st.altair_chart(chart + text)
else:
    st.write("Please select at least one player to compare.")