#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
server_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/server_df.csv')
returner_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/returner_df.csv')
s1_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/S+1_df.csv')
singles_matches_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/singles_matches_df.csv')

app = dash.Dash(__name__)

# Extract unique players and opponents
players = singles_matches_df['2 - Player Name'].unique()
opponents = singles_matches_df['3 - Opponent Name'].unique()
matches = singles_matches_df['1 - Event'].unique()

app.layout = html.Div([
    html.H1("Tennis Statistics Dashboard"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': player, 'value': player} for player in players],
        value=players[0],
        placeholder="Select a Player"
    ),
    dcc.Dropdown(
        id='opponent-dropdown',
        options=[{'label': opponent, 'value': opponent} for opponent in opponents],
        value=opponents[0],
        placeholder="Select an Opponent"
    ),
    dcc.Dropdown(
        id='match-dropdown',
        options=[{'label': match, 'value': match} for match in matches],
        value=matches[0],
        placeholder="Select a Match"
    ),
    dcc.Graph(id='server-graph'),
    dcc.Graph(id='returner-graph'),
    dcc.Graph(id='s1-graph')
])

@app.callback(
    [Output('server-graph', 'figure'),
     Output('returner-graph', 'figure'),
     Output('s1-graph', 'figure')],
    [Input('player-dropdown', 'value'),
     Input('opponent-dropdown', 'value'),
     Input('match-dropdown', 'value')]
)
def update_graphs(selected_player, selected_opponent, selected_match):
    # Filter data based on selections
    filtered_server_df = server_df[server_df['Unnamed: 0'] == selected_player]
    filtered_returner_df = returner_df[returner_df['Unnamed: 0'] == selected_player]
    filtered_s1_df = s1_df[s1_df['Player'] == selected_player]

    filtered_matches_df = singles_matches_df[
        (singles_matches_df['2 - Player Name'] == selected_player) &
        (singles_matches_df['3 - Opponent Name'] == selected_opponent) &
        (singles_matches_df['1 - Event'] == selected_match)
    ]

    # Create figures
    server_fig = px.bar(filtered_server_df, x='total points', y='serve points', title='Server Statistics')
    returner_fig = px.bar(filtered_returner_df, x='total points', y='return points', title='Returner Statistics')
    s1_fig = px.bar(filtered_s1_df, x='Total Serve +1 Actions', y='Serve +1 Winners', title='Serve +1 Statistics')

    return server_fig, returner_fig, s1_fig

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




