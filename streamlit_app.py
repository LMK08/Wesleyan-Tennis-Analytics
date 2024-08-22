#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data
server_df = pd.read_csv(os.path.join('data', 'server_df.csv'))
returner_df = pd.read_csv(os.path.join('data', 'returner_df.csv'))
s1_df = pd.read_csv(os.path.join('data', 'S+1_df.csv'))
singles_matches_df = pd.read_csv(os.path.join('data', 'singles_matches_df.csv'))

# Rename the column 'Unnamed: 0' to 'Player'
server_df.rename(columns={'Unnamed: 0': 'Player'}, inplace=True)

# Streamlit application layout
st.title("Tennis Statistics Dashboard")

# Dropdown for selecting Player 1
player1 = st.selectbox(
    "Select Player 1",
    server_df['Player'].unique(),
    index=0
)

# Dropdown for selecting Player 2 (Optional)
player2 = st.selectbox(
    "Select Player 2 (Optional)",
    ["None"] + list(server_df['Player'].unique()),
    index=0
)

# Multiselect for server metrics
server_metrics = st.multiselect(
    "Select Server Metrics",
    server_df.columns,
    default=server_df.columns[1]  # Assuming first column is 'Player'
)

# Multiselect for returner metrics
returner_metrics = st.multiselect(
    "Select Returner Metrics",
    returner_df.columns,
    default=returner_df.columns[1]  # Assuming first column is 'Player'
)

# Multiselect for S+1 metrics
s1_metrics = st.multiselect(
    "Select S+1 Metrics",
    s1_df.columns,
    default=s1_df.columns[1]  # Assuming first column is 'Player Name'
)

# Filter data based on the selected players
filtered_server_df1 = server_df[server_df['Player'] == player1]
filtered_returner_df1 = returner_df[returner_df['Player'] == player1]
filtered_s1_df1 = s1_df[s1_df['Player Name'] == player1]

if player2 != "None":
    filtered_server_df2 = server_df[server_df['Player'] == player2]
    filtered_returner_df2 = returner_df[returner_df['Player'] == player2]
    filtered_s1_df2 = s1_df[s1_df['Player Name'] == player2]
else:
    filtered_server_df2 = filtered_returner_df2 = filtered_s1_df2 = None

# Server Metrics Visualization
if not filtered_server_df1.empty:
    if filtered_server_df2 is not None and not filtered_server_df2.empty:
        server_fig = px.bar(
            pd.concat([
                filtered_server_df1.melt(id_vars=['Player'], value_vars=server_metrics),
                filtered_server_df2.melt(id_vars=['Player'], value_vars=server_metrics)
            ]),
            x='variable',
            y='value',
            color='Player',
            barmode='group',
            title=f'Comparison of Server Metrics: {player1} vs {player2}'
        )
    else:
        server_fig = px.bar(
            filtered_server_df1.melt(id_vars=['Player'], value_vars=server_metrics),
            x='variable',
            y='value',
            barmode='group',
            title=f'Server Metrics for {player1}'
        )
    st.plotly_chart(server_fig)

# Returner Metrics Visualization
if not filtered_returner_df1.empty:
    if filtered_returner_df2 is not None and not filtered_returner_df2.empty:
        returner_fig = px.bar(
            pd.concat([
                filtered_returner_df1.melt(id_vars=['Player'], value_vars=returner_metrics),
                filtered_returner_df2.melt(id_vars=['Player'], value_vars=returner_metrics)
            ]),
            x='variable',
            y='value',
            color='Player',
            barmode='group',
            title=f'Comparison of Returner Metrics: {player1} vs {player2}'
        )
    else:
        returner_fig = px.bar(
            filtered_returner_df1.melt(id_vars=['Player'], value_vars=returner_metrics),
            x='variable',
            y='value',
            barmode='group',
            title=f'Returner Metrics for {player1}'
        )
    st.plotly_chart(returner_fig)

# S+1 Metrics Visualization
if not filtered_s1_df1.empty:
    if filtered_s1_df2 is not None and not filtered_s1_df2.empty:
        s1_fig = px.bar(
            pd.concat([
                filtered_s1_df1.melt(id_vars=['Player Name'], value_vars=s1_metrics),
                filtered_s1_df2.melt(id_vars=['Player Name'], value_vars=s1_metrics)
            ]),
            x='variable',
            y='value',
            color='Player Name',
            barmode='group',
            title=f'Comparison of S+1 Metrics: {player1} vs {player2}'
        )
    else:
        s1_fig = px.bar(
            filtered_s1_df1.melt(id_vars=['Player Name'], value_vars=s1_metrics),
            x='variable',
            y='value',
            barmode='group',
            title=f'S+1 Metrics for {player1}'
        )
    st.plotly_chart(s1_fig)


# In[ ]:




