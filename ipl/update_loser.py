import pandas as pd

# Load the dataset
file_path = 'matches.csv'  # Replace with the path to your file
data = pd.read_csv(file_path)

# Add a 'loser' column based on the winner and teams playing
data['loser'] = data.apply(
    lambda row: row['team2'] if row['winner'] == row['team1'] else row['team1'], axis=1
)

# Save or view the updated DataFrame
data.to_csv('updated_matches.csv', index=False)
print(data.head())