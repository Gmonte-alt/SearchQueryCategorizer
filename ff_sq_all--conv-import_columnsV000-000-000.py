# file name: ff_sq_all--conv-import_columns.py
# version: V000-000-000
# Note: this is a replica of the ff_sq_all-conv-import.py file, except the input file is has the conversion action names set as columns rather than rows

import pandas as pd

# Load the CSV file
file_path = 'data/Search terms - Account Structure all conversions.csv'  # Update this path with the actual file path

# Read the CSV file starting from the 3rd row
try:
    df = pd.read_csv(file_path, skiprows=2)
except pd.errors.ParserError:
    df = pd.read_csv(file_path, delimiter=';', skiprows=2)
    # Add more delimiters if needed, e.g., '\t' for tab

# Inspect the first few rows and data types to ensure it is read correctly
print(df.head())
print(df.dtypes)

# Ensure relevant columns are treated as floats
conversion_columns = [
    'Furnished Finder - GA4 (web) FF Lead_All conv.',
    'Furnished Finder - GA4 (web) FF Purchase_All conv.',
    'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.',
    'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.',
    'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.'
]

for col in conversion_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    else:
        print(f"Column {col} not found in DataFrame")

# Filter out search terms that contain the exact phrases
phrases_to_exclude = [
    'furnished finder', 'furnished finders', 'furnishedfinder', 'furnished findings', 'furniture finder',
    'furnished finger', 'furniture finder', 'furnishing finder', 'finder furnished', 'furnace finder',
    'finding furnished'
]
for phrase in phrases_to_exclude:
    df = df[~df['Search term'].str.contains(phrase, case=False, na=False)]

# Aggregate "All conv." values by "Search term" for purchases
purchase_aggregated_df = df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF Purchase_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF Purchase_All conv.': 'ff_purchases'})

# Aggregate "All conv." values by "Search term" for leads
lead_aggregated_df = df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF Lead_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF Lead_All conv.': 'ff_leads'})

# Aggregate "All conv." values by "Search term" for BRSubmit
BRSubmit_aggregated_df = df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.': 'ff_BRSubmit'})

# Aggregate "All conv." values by "Search term" for DMSubmit
DMSubmit_aggregated_df = df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.': 'ff_DMSubmit'})

# Aggregate "All conv." values by "Search term" for PhoneGet
PhoneGet_aggregated_df = df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.': 'ff_PhoneGet'})

# Merge the aggregated DataFrames on "Search term"
merged_df = purchase_aggregated_df
for df_to_merge in [lead_aggregated_df, BRSubmit_aggregated_df, DMSubmit_aggregated_df, PhoneGet_aggregated_df]:
    merged_df = pd.merge(merged_df, df_to_merge, on='Search term', how='outer')

# Fill NaN values with 0 for all columns except 'Search term'
for col in merged_df.columns:
    if col != 'Search term':
        merged_df[col] = merged_df[col].fillna(0)

# Create a new column for the division of ff_purchases by ff_leads, handling division by zero
merged_df['ff_purchase_to_lead_ratio'] = merged_df.apply(
    lambda row: row['ff_purchases'] / row['ff_leads'] if row['ff_leads'] != 0 else float('NaN'),
    axis=1
)

# Create a new column for the division of ff_leads by ff_BRSubmit, handling division by zero
merged_df['ff_lead_to_BRSubmit_ratio'] = merged_df.apply(
    lambda row: row['ff_leads'] / row['ff_BRSubmit'] if row['ff_BRSubmit'] != 0 else float('NaN'),
    axis=1
)

# Sort the merged dataframe by "ff_purchases" from highest to lowest
merged_df = merged_df.sort_values(by='ff_purchases', ascending=False)

# Save the result to a new CSV file
output_file_path = 'output/NEW_filtered_aggregated_output.csv'
merged_df.to_csv(output_file_path, index=False)

print(f"Filtered, aggregated, and sorted data has been saved to {output_file_path}")
