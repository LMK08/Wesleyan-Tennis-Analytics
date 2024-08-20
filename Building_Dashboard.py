#!/usr/bin/env python
# coding: utf-8

# In[13]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# In[14]:


# Load data
server_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/server_df.csv')
returner_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/returner_df.csv')
s1_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/S+1_df.csv')
singles_matches_df = pd.read_csv('/Users/lkimball/Desktop/Wesleyan_Tennis_Analytics/singles_matches_df.csv')


# In[15]:


singles_matches_df


# In[16]:


server_df


# In[17]:


# Rename the column 'Unnamed: 0' to 'Player'
server_df.rename(columns={'Unnamed: 0': 'Player'}, inplace=True)


# In[18]:




# Initialize the Dash app
app = dash.Dash(__name__)

# Extract columns from each DataFrame
server_columns = list(server_df.columns)
returner_columns = list(returner_df.columns)
s1_columns = list(s1_df.columns)

# Assuming you have already renamed the column:
# server_df.rename(columns={'Unnamed: 0': 'Player'}, inplace=True)

# Update the dropdowns to reference the new column name
app.layout = html.Div([
    html.H1("Tennis Statistics Dashboard"),
    
    # Dropdown for selecting Player 1
    dcc.Dropdown(
        id='player1-dropdown',
        options=[{'label': player, 'value': player} for player in server_df['Player'].unique()],
        value=server_df['Player'].unique()[0],  # Default to the first player
        placeholder="Select Player 1"
    ),
    
    # Dropdown for selecting Player 2
    dcc.Dropdown(
        id='player2-dropdown',
        options=[{'label': player, 'value': player} for player in server_df['Player'].unique()],
        value=None,  # No default value
        placeholder="Select Player 2 (Optional)"
    ),
    
    # Dropdown for server metrics
    html.Div([
        html.Label("Server Metrics"),
        dcc.Dropdown(
            id='server-metric-dropdown',
            options=[{'label': metric, 'value': metric} for metric in server_columns],
            multi=True,
            value=[server_columns[0]],  # Default to the first metric
            placeholder="Select server metrics"
        ),
        dcc.Graph(id='server-graph'),
    ]),
    
    # Dropdown for returner metrics
    html.Div([
        html.Label("Returner Metrics"),
        dcc.Dropdown(
            id='returner-metric-dropdown',
            options=[{'label': metric, 'value': metric} for metric in returner_columns],
            multi=True,
            value=[returner_columns[0]],  # Default to the first metric
            placeholder="Select returner metrics"
        ),
        dcc.Graph(id='returner-graph'),
    ]),
    
    # Dropdown for S+1 metrics
    html.Div([
        html.Label("S+1 Metrics"),
        dcc.Dropdown(
            id='s1-metric-dropdown',
            options=[{'label': metric, 'value': metric} for metric in s1_columns],
            multi=True,
            value=[s1_columns[0]],  # Default to the first metric
            placeholder="Select S+1 metrics"
        ),
        dcc.Graph(id='s1-graph'),
    ]),
])


@app.callback(
    [Output('server-graph', 'figure'),
     Output('returner-graph', 'figure'),
     Output('s1-graph', 'figure')],
    [Input('player1-dropdown', 'value'),
     Input('player2-dropdown', 'value'),
     Input('server-metric-dropdown', 'value'),
     Input('returner-metric-dropdown', 'value'),
     Input('s1-metric-dropdown', 'value')]
)
def update_graphs(selected_player1, selected_player2, selected_server_metrics, selected_returner_metrics, selected_s1_metrics):
    # Filter data based on the selected players
    filtered_server_df1 = server_df[server_df['Player'] == selected_player1]
    filtered_returner_df1 = returner_df[returner_df['Player'] == selected_player1]
    filtered_s1_df1 = s1_df[s1_df['Player Name'] == selected_player1]
    
    # Check if Player 2 is selected
    if selected_player2:
        filtered_server_df2 = server_df[server_df['Player'] == selected_player2]
        filtered_returner_df2 = returner_df[returner_df['Player'] == selected_player2]
        filtered_s1_df2 = s1_df[s1_df['Player Name'] == selected_player2]
    else:
        filtered_server_df2 = filtered_returner_df2 = filtered_s1_df2 = None

    # Server Metrics Visualization
    if not filtered_server_df1.empty:
        if filtered_server_df2 is not None and not filtered_server_df2.empty:
            server_fig = px.bar(
                pd.concat([
                    filtered_server_df1.melt(id_vars=['Player'], value_vars=selected_server_metrics),
                    filtered_server_df2.melt(id_vars=['Player'], value_vars=selected_server_metrics)
                ]),
                x='variable',
                y='value',
                color='Player',
                barmode='group',
                title=f'Comparison of Server Metrics: {selected_player1} vs {selected_player2}'
            )
        else:
            server_fig = px.bar(
                filtered_server_df1.melt(id_vars=['Player'], value_vars=selected_server_metrics),
                x='variable',
                y='value',
                barmode='group',
                title=f'Server Metrics for {selected_player1}'
            )
    else:
        server_fig = {}

    # Returner Metrics Visualization
    if not filtered_returner_df1.empty:
        if filtered_returner_df2 is not None and not filtered_returner_df2.empty:
            returner_fig = px.bar(
                pd.concat([
                    filtered_returner_df1.melt(id_vars=['Player'], value_vars=selected_returner_metrics),
                    filtered_returner_df2.melt(id_vars=['Player'], value_vars=selected_returner_metrics)
                ]),
                x='variable',
                y='value',
                color='Player',
                barmode='group',
                title=f'Comparison of Returner Metrics: {selected_player1} vs {selected_player2}'
            )
        else:
            returner_fig = px.bar(
                filtered_returner_df1.melt(id_vars=['Player'], value_vars=selected_returner_metrics),
                x='variable',
                y='value',
                barmode='group',
                title=f'Returner Metrics for {selected_player1}'
            )
    else:
        returner_fig = {}

    # S+1 Metrics Visualization
    if not filtered_s1_df1.empty:
        if filtered_s1_df2 is not None and not filtered_s1_df2.empty:
            s1_fig = px.bar(
                pd.concat([
                    filtered_s1_df1.melt(id_vars=['Player Name'], value_vars=selected_s1_metrics),
                    filtered_s1_df2.melt(id_vars=['Player Name'], value_vars=selected_s1_metrics)
                ]),
                x='variable',
                y='value',
                color='Player Name',
                barmode='group',
                title=f'Comparison of S+1 Metrics: {selected_player1} vs {selected_player2}'
            )
        else:
            s1_fig = px.bar(
                filtered_s1_df1.melt(id_vars=['Player Name'], value_vars=selected_s1_metrics),
                x='variable',
                y='value',
                barmode='group',
                title=f'S+1 Metrics for {selected_player1}'
            )
    else:
        s1_fig = {}

    return server_fig, returner_fig, s1_fig


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:





# In[ ]:





# In[ ]:




