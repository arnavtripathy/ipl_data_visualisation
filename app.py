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

# App layout
app.layout = html.Div(
    [
        # Main Header
        html.Div(
            html.H1("IPL Visualizations", className="text-center my-4", style={"color": "#ffffff", "font-size": "36px"}),
            style={
                "background-color": "#1a1a1a",
                "padding": "20px",
                "border-radius": "10px",
                "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",
                "margin": "10px",
            },
        ),
        
        # Map Container with Header
        html.Div(
            [
                html.H2("Match Locations Hotspot", className="text-center mb-2", style={"color": "#ffffff"}),
                dcc.Graph(id="world-map", style={"height": "50vh"}),  # Map component
            ],
            style={
                "position": "absolute",
                "top": "10%",
                "left": "5%",
                "width": "40%",
                "height": "40%",
                "border": "2px solid #ffffff",
                "border-radius": "10px",
                "padding": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "box-shadow": "2px 2px 10px rgba(0,0,0,0.5)",
            },
        ),
        
        # Player Performance Metrics Container
        html.Div(
            [
                html.H2("Player Performance Metrics", className="text-center mb-2", style={"color": "#ffffff"}),
                dcc.Tabs(
                    id="metric-tabs",
                    value="batting_strike_rate",
                    children=[
                        dcc.Tab(label="Top 10 Batting Strike Rate", value="batting_strike_rate"),
                        dcc.Tab(label="Top 10 Bowling Economies", value="bowling_economy"),
                        dcc.Tab(label="Top 10 Highest Run Scorers", value="runs"),
                        dcc.Tab(label="Top 10 Highest Wicket Takers", value="wickets"),
                    ],
                ),
                dcc.Graph(id="bar-graph", style={"height": "50vh"}),  # Bar graph component
            ],
            style={
                "position": "absolute",
                "top": "10%",
                "right": "5%",
                "width": "40%",
                "height": "40%",
                "border": "2px solid #ffffff",
                "border-radius": "10px",
                "padding": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "box-shadow": "2px 2px 10px rgba(0,0,0,0.5)",
            },
        ),
        
        # Team Wins and Losses Bar Graph Container with Tabs
        html.Div(
            [
                html.H2("Team Performance Overview", className="text-center mb-2", style={"color": "#ffffff"}),
                dcc.Tabs(
                    id="team-performance-tabs",
                    value="wins",
                    children=[
                        dcc.Tab(label="Team Wins", value="wins"),
                        dcc.Tab(label="Team Losses", value="losses"),
                    ],
                ),
                dcc.Graph(id="team-performance-bar", style={"height": "40vh"}),  # Team Performance Graph
            ],
            style={
                "position": "absolute",
                "bottom": "5%",
                "left": "5%",
                "width": "40%",
                "height": "40%",
                "border": "2px solid #ffffff",
                "border-radius": "10px",
                "padding": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "box-shadow": "2px 2px 10px rgba(0,0,0,0.5)",
            },
        ),

        # Line Graph Container for Spending Trends
        html.Div(
            [
                html.H2("Team Spending Trends", className="text-center mb-2", style={"color": "#ffffff"}),
                dcc.Graph(id="line-graph", style={"height": "40vh"}),  # Line graph component
            ],
            style={
                "position": "absolute",
                "bottom": "5%",
                "right": "5%",
                "width": "40%",
                "height": "40%",
                "border": "2px solid #ffffff",
                "border-radius": "10px",
                "padding": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "box-shadow": "2px 2px 10px rgba(0,0,0,0.5)",
            },
        ),
    ],
    style={
        "height": "150vh",
        "position": "relative",
        "background-color": "#000000",
        "background-image": "url('/assets/ipl_trophy.jpg')",  # Replace with your image URL
        "background-size": "cover",
        "background-position": "center",
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
        zoom=4,
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
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

# Callback to update the team wins bar graph
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
        title="Total Amount Spent by Teams Over the Years",
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