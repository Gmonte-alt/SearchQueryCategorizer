# file name: ff_sq_all-conv-import.py 
# version: V000-000-001

import pandas as pd

# Load the CSV file
file_path = 'data/search_query_conversion_actions.csv'  # Update this path with the actual file path

# Try to read the CSV file with different delimiters if necessary
try:
    df = pd.read_csv(file_path)
except pd.errors.ParserError:
    df = pd.read_csv(file_path, delimiter=';')
    # Add more delimiters if needed, e.g., '\t' for tab

# Inspect the first few rows and data types to ensure it is read correctly
print(df.head())
print(df.dtypes)

# Ensure "All conv." is treated as a float
df['All conv.'] = pd.to_numeric(df['All conv.'], errors='coerce')

# Filter out search terms that contain the exact phrases
phrases_to_exclude = ['furnished finder', 'furnished finders', 'furnishedfinder']
for phrase in phrases_to_exclude:
    df = df[~df['Search term'].str.contains(phrase, case=False, na=False)]

# Separate DataFrames for different conversion actions
purchase_df = df[df['Conversion action'] == 'Furnished Finder - GA4 (web) FF Purchase']
lead_df = df[df['Conversion action'] == 'Furnished Finder - GA4 (web) FF Lead']

# Aggregate "All conv." values by "Search term" for purchases
purchase_aggregated_df = purchase_df.groupby('Search term', as_index=False).agg({
    'All conv.': 'sum',
}).rename(columns={'All conv.': 'ff_purchases'})

# Aggregate "All conv." values by "Search term" for leads
lead_aggregated_df = lead_df.groupby('Search term', as_index=False).agg({
    'All conv.': 'sum',
}).rename(columns={'All conv.': 'ff_leads'})

# Merge the two aggregated DataFrames on "Search term"
merged_df = pd.merge(purchase_aggregated_df, lead_aggregated_df, on='Search term', how='outer')

# Fill NaN values with 0 for both columns
merged_df['ff_purchases'] = merged_df['ff_purchases'].fillna(0)
merged_df['ff_leads'] = merged_df['ff_leads'].fillna(0)

# Create a new column for the division of ff_purchases by ff_leads, handling division by zero
merged_df['ff_purchase_to_lead_ratio'] = merged_df.apply(
    lambda row: row['ff_purchases'] / row['ff_leads'] if row['ff_leads'] != 0 else float('NaN'),
    axis=1
)

# Sort the merged dataframe by "ff_purchases" from highest to lowest
merged_df = merged_df.sort_values(by='ff_purchases', ascending=False)

# Save the result to a new CSV file
output_file_path = 'output/filtered_aggregated_output.csv'
merged_df.to_csv(output_file_path, index=False)

print(f"Filtered, aggregated, and sorted data has been saved to {output_file_path}")
