# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from utilities import extract_id_and_city

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

matches_path = 'ipl/matches.csv'
stadium_data = pd.read_csv(matches_path)
winners_data = pd.read_csv(matches_path)


#Load auction data
auction_path = 'ipl/team_total_spent_per_year.csv'  # Replace with your file path
auction_data = pd.read_csv(auction_path)

# Filter out rows without coordinates
id_city_df = extract_id_and_city(stadium_data)



# Load player statistics data
player_stats_path = 'ipl/player_stats.csv'
player_stats = pd.read_csv(player_stats_path)

# Filter players with at least 500 balls faced
qualified_players_batting = player_stats[player_stats['balls_faced'] >= 500]

# Calculate top 10 batting averages for players with at least 30 matches
top_10_batting_strike_rate = qualified_players_batting.nlargest(10, 'batting_strike_rate')[['player', 'batting_strike_rate']]

# Filter players with at least 1000 balls bowled
qualified_players_bowling = player_stats[player_stats['balls_bowled'] >= 1000]

# Calculate top 10 bowling economies for players with at least 30 matches
top_10_bowling_economies = qualified_players_bowling.nsmallest(10, 'bowling_economy')[['player', 'bowling_economy']]

# Calculate top 10 highest runscorers of all time
top_10_runs = player_stats.nlargest(10,'runs')[['player','runs']]


# Calculate top 10 highest wicket takers of all time
top_10_wickets = player_stats.nlargest(10,'wickets')[['player','wickets']]

# Extract team-wise number of matches won
team_wins = winners_data['winner'].value_counts().reset_index()
team_wins.columns = ['team', 'matches_won']

# Extract team-wise number of matches won
losers_path = 'ipl/updated_matches.csv'
losers_data = pd.read_csv(losers_path)
team_losses = losers_data['loser'].value_counts().reset_index()
team_losses.columns = ['team', 'matches_lost']

# Initialize Dash app with Bootstrap theme
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        # Main Header
        html.Div(
            html.H1(
                "IPL Visualizations",
                className="text-center",
                style={"color": "#4A90E2", "font-size": "36px", "font-weight": "bold"},
            ),
            style={
                "background-color": "#f5f7fa",
                "padding": "20px",
                "margin-bottom": "20px",
                "border-radius": "10px",
                "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            },
        ),
        
        # Row 1: Match Locations and Player Performance Metrics
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Match Locations Hotspot",
                            className="text-center",
                            style={"color": "#4A90E2"},
                        ),
                        dcc.Graph(id="world-map", style={"height": "300px"}),  # Map component
                    ],
                    style={
                        "width": "48%",
                        "background-color": "#ffffff",
                        "padding": "20px",
                        "margin": "10px",
                        "border-radius": "10px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "height": "450px",
                    },
                ),
                html.Div(
                    [
                        html.H2(
                            "Player Performance Metrics",
                            className="text-center",
                            style={"color": "#4A90E2"},
                        ),
                        dcc.Tabs(
                            id="metric-tabs",
                            value="batting_strike_rate",
                            children=[
                                dcc.Tab(label="Batting Strike Rate", value="batting_strike_rate"),
                                dcc.Tab(label="Bowling Economy", value="bowling_economy"),
                                dcc.Tab(label="Total Runs", value="runs"),
                                dcc.Tab(label="Total Wickets", value="wickets"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        dcc.Graph(id="bar-graph", style={"height": "300px"}),  # Bar graph component
                    ],
                    style={
                        "width": "48%",
                        "background-color": "#ffffff",
                        "padding": "20px",
                        "margin": "10px",
                        "border-radius": "10px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
            style={"width": "100%", "margin-bottom": "20px", "text-align": "center"},
        ),
        
        # Row 2: Team Performance and Spending Trends
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Team Performance Overview",
                            className="text-center",
                            style={"color": "#4A90E2"},
                        ),
                        dcc.Tabs(
                            id="team-performance-tabs",
                            value="wins",
                            children=[
                                dcc.Tab(label="Wins", value="wins"),
                                dcc.Tab(label="Losses", value="losses"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        dcc.Graph(id="team-performance-bar", style={"height": "300px"}),  # Team Performance Graph
                    ],
                    style={
                        "width": "48%",
                        "background-color": "#ffffff",
                        "padding": "20px",
                        "margin": "10px",
                        "border-radius": "10px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                        html.H2(
                            "Team Spending Trends",
                            className="text-center",
                            style={"color": "#4A90E2"},
                        ),
                        dcc.Graph(id="line-graph", style={"height": "300px"}),  # Line graph component
                    ],
                    style={
                        "width": "48%",
                        "background-color": "#ffffff",
                        "padding": "20px",
                        "margin": "10px",
                        "border-radius": "10px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
            style={"width": "100%", "margin-bottom": "20px", "text-align": "center"},
        ),
    ],
    style={
        "font-family": "Arial, sans-serif",
        "background-color": "#f5f7fa",
        "padding": "20px",
        "text-align": "center",
    },
)

# Callback to update the map
@app.callback(
    Output("world-map", "figure"),
    Input("world-map", "id"),  # Dummy input to initialize the graph
)
def update_map(_):
    # Create the map
    fig = px.scatter_mapbox(
        id_city_df,
        lat="lat",
        lon="lon",
        size="match_count",
        hover_name="city",
        title="Map of IPL Venues",
        hover_data={"match_count": True, "lat": False, "lon": False},
        color_discrete_sequence=["blue"],
        zoom=3,
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        height=360,
        margin={"r": 0, "t": 2, "l": 0, "b": 0},
    )
    return fig

# Callback to update the bar graph based on selected metric
@app.callback(
    Output("bar-graph", "figure"),
    Input("metric-tabs", "value"),
)
def update_bar_graph(selected_metric):
    if selected_metric == "batting_strike_rate":
        df = top_10_batting_strike_rate
        y_label = "Batting Strike Rate"
        color = "batting_strike_rate"
        title = "Top 10 Players by Batting Strike Rate"
    elif selected_metric == "runs":
        df = top_10_runs
        y_label = "Runs scored"
        color = "runs"
        title = "Top 10 Players with highest Runs"
    elif selected_metric == "wickets":
        df = top_10_wickets
        y_label = "Wickets taken"
        color = "wickets"
        title = "Top 10 Players with highest Wickets"
    elif selected_metric == "bowling_economy":
        df = top_10_bowling_economies
        y_label = "Bowling Economy"
        color = "bowling_economy"
        title = "Top 10 Players by Bowling Economy"

    # Create the bar graph
    fig = px.bar(
        df,
        x="player",
        y=selected_metric,
        title=title,
        labels={selected_metric: y_label, "player": "Player"},
        color=color,
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        xaxis_title="Player",
        yaxis_title=y_label,
    )
    return fig


# Callback to update the team wins or losses bar graph
@app.callback(
    Output("team-performance-bar", "figure"),
    Input("team-performance-tabs", "value"),
)
def update_team_performance_bar(selected_tab):
    if selected_tab == "wins":
        df = team_wins
        y_label = "Matches Won"
        color = "matches_won"
        title = "Number of Matches Won by Each Team"
    elif selected_tab == "losses":
        df = team_losses
        y_label = "Matches Lost"
        color = "matches_lost"
        title = "Number of Matches Lost by Each Team"

    # Create the bar graph
    fig = px.bar(
        df,
        x="team",
        y=color,
        title=title,
        labels={color: y_label, "team": "Team"},
        color=color,
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        xaxis_title="Team",
        yaxis_title=y_label,
    )
    return fig

@app.callback(
    Output("line-graph", "figure"),
    Input("line-graph", "id"),  # Dummy input to initialize the graph
)
def update_line_graph(_):
    fig = px.line(
        auction_data,
        x="year",
        y="amount",
        color="team",
        title="Total Amount Spent by Teams Over the Years in INR from 2013-2022",
        labels={"amount": "Amount Spent", "year": "Year", "team": "Team"},
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        xaxis_title="Year",
        yaxis_title="Amount Spent",
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)