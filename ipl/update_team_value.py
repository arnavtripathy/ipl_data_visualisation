import pandas as pd

# Load the dataset
file_path = 'auction_data.csv'  # Replace with your file path
auction_data = pd.read_csv(file_path)

# Group by year and team, and sum the amount spent

auction_data['Year'] = auction_data['Year'].astype(int)
total_spent = auction_data.groupby(['Year', 'Team'])['Amount'].sum().reset_index()

# Save the result to a CSV file
output_path = 'team_total_spent_per_year.csv'
total_spent.to_csv(output_path, index=False)

print(f"Processed data has been saved to {output_path}")