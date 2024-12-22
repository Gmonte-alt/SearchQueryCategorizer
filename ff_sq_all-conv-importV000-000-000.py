# file name: ff_sq_all-conv-import.py 
# version: V000-000-000

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

# Filter rows where "Conversion action" contains "Furnished Finder - GA4 (web) FF Purchase"
filtered_df = df[df['Conversion action'] == 'Furnished Finder - GA4 (web) FF Purchase']

# Filter out search terms that contain the exact phrases
phrases_to_exclude = ['furnished finder', 'furnished finders', 'furnishedfinder']
for phrase in phrases_to_exclude:
    filtered_df = filtered_df[~filtered_df['Search term'].str.contains(phrase, case=False, na=False)]

# Check for missing values and handle them (optional)
print(filtered_df.isnull().sum())

# Aggregate "All conv." values by "Search term"
aggregated_df = filtered_df.groupby('Search term', as_index=False).agg({
    'All conv.': 'sum',
    # Include other columns you need in the output. Here are some examples:
    # 'Clicks': 'sum',
    # 'Impr.': 'sum',
    # 'CTR': 'mean',
    # 'Avg. CPC': 'mean',
    # 'Cost': 'sum',
    # 'Conv. rate': 'mean',
    # 'Conversions': 'sum',
    # 'Cost / conv.': 'mean'
})

# Sort the aggregated dataframe by "All conv." from highest to lowest
aggregated_df = aggregated_df.sort_values(by='All conv.', ascending=False)

# Save the result to a new CSV file
output_file_path = 'output/filtered_aggregated_output.csv'
aggregated_df.to_csv(output_file_path, index=False)

print(f"Filtered, aggregated, and sorted data has been saved to {output_file_path}")
