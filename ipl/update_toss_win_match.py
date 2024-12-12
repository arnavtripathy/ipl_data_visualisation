import pandas as pd

# Load the dataset
file_path = 'matches.csv'  # Replace with the path to your file
data = pd.read_csv(file_path)

# Add a 'loser' column based on the winner and teams playing
data['toss_win'] = data.apply(
    lambda row: True if row['winner'] == row['toss_winner'] else False, axis=1
)

# Save or view the updated DataFrame
data.to_csv('toss_matches.csv', index=False)
print(data.head())