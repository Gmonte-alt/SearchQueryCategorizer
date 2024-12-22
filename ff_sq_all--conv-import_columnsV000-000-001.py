# file name: ff_sq_all--conv-import_columns.py
# version: V000-000-001
# Note: this next version incorporates the performance data for all search queries
#       The results look good, but I am seeing some slight increase on purchases for a few search queries

import pandas as pd

# Load the main CSV file
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

# Load the second CSV file
second_file_path = 'data/Search terms - Account Structure Performance.csv' # 'data/second_file.csv'  # Update this path with the actual file path

# Read the second CSV file starting from the 3rd row
try:
    df2 = pd.read_csv(second_file_path, skiprows=2)
except pd.errors.ParserError:
    df2 = pd.read_csv(second_file_path, delimiter=';', skiprows=2)
    # Add more delimiters if needed, e.g., '\t' for tab

# Inspect the first few rows and data types of the second CSV to ensure it is read correctly
print(df2.head())
print(df2.dtypes)

# Select relevant columns from the second CSV
df2 = df2[['Search term', 'Keyword ID', 'Ad group ID', 'Campaign ID', 'Clicks', 'Impr.', 'Cost']]

# Convert "Clicks" column to numeric
df2['Clicks'] = pd.to_numeric(df2['Clicks'], errors='coerce')
df2['Impr.'] = pd.to_numeric(df2['Impr.'], errors='coerce')
df2['Cost'] = pd.to_numeric(df2['Cost'], errors='coerce')

# Filter rows where "Clicks" < 1 and save these to a new CSV file
filtered_df2 = df2[df2['Clicks'] < 1]
filtered_output_file_path = 'output/zero-clicks-search-query.csv'
filtered_df2.to_csv(filtered_output_file_path, index=False)

print(f"Filtered rows with Clicks < 1 have been saved to {filtered_output_file_path}")

# Exclude rows where "Clicks" < 1 for the merge
df2 = df2[df2['Clicks'] >= 1]

# Merge the first DataFrame with the second DataFrame using an outer merge on multiple fields
merge_columns = ['Search term', 'Keyword ID', 'Ad group ID', 'Campaign ID']
merged_initial_df = pd.merge(df, df2, on=merge_columns, how='outer')

# Ensure relevant columns are treated as floats in the merged_initial_df
conversion_columns = [
    'Furnished Finder - GA4 (web) FF Lead_All conv.',
    'Furnished Finder - GA4 (web) FF Purchase_All conv.',
    'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.',
    'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.',
    'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.',
    'Clicks',
    'Impr.',
    'Cost'
]

for col in conversion_columns:
    if col in merged_initial_df.columns:
        merged_initial_df[col] = pd.to_numeric(merged_initial_df[col], errors='coerce')
    else:
        print(f"Column {col} not found in DataFrame")

# Filter out search terms that contain the exact phrases
phrases_to_exclude = [
    'furnished finder', 'furnished finders', 'furnishedfinder', 'furnished findings', 'furniture finder',
    'furnished finger', 'furniture finder', 'furnishing finder', 'finder furnished', 'furnace finder',
    'finding furnished', 'furnishfinder', 'find furnished'
]
for phrase in phrases_to_exclude:
    merged_initial_df = merged_initial_df[~merged_initial_df['Search term'].str.contains(phrase, case=False, na=False)]

# Aggregate "All conv." values by "Search term" for purchases
purchase_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF Purchase_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF Purchase_All conv.': 'ff_purchases'})

# Aggregate "All conv." values by "Search term" for leads
lead_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF Lead_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF Lead_All conv.': 'ff_leads'})

# Aggregate "All conv." values by "Search term" for BRSubmit
BRSubmit_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-BRSubmit_All conv.': 'ff_BRSubmit'})

# Aggregate "All conv." values by "Search term" for DMSubmit
DMSubmit_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-DMSubmit_All conv.': 'ff_DMSubmit'})

# Aggregate "All conv." values by "Search term" for PhoneGet
PhoneGet_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.': 'sum'
}).rename(columns={'Furnished Finder - GA4 (web) FF-PhoneGet_All conv.': 'ff_PhoneGet'})

# Aggregate performance metrics from the second CSV file
performance_aggregated_df = merged_initial_df.groupby('Search term', as_index=False).agg({
    'Clicks': 'sum',
    'Impr.': 'sum',
    'Cost': 'sum'
})

# Merge the aggregated DataFrames on "Search term"
merged_df = purchase_aggregated_df
for df_to_merge in [lead_aggregated_df, BRSubmit_aggregated_df, DMSubmit_aggregated_df, PhoneGet_aggregated_df, performance_aggregated_df]:
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

# Create a new column for the division of Cost by ff_purchases, handling division by zero
merged_df['ff_Cost_to_purchase_ratio'] = merged_df.apply(
    lambda row: row['Cost'] / row['ff_purchases'] if row['ff_purchases'] != 0 else float('NaN'),
    axis=1
)

# Create a new column for the division of ff_leads by ff_BRSubmit, handling division by zero
merged_df['ff_lead_to_BRSubmit_ratio'] = merged_df.apply(
    lambda row: row['ff_leads'] / row['ff_BRSubmit'] if row['ff_BRSubmit'] != 0 else float('NaN'),
    axis=1
)

# Sort the merged dataframe by "ff_purchases" from highest to lowest
merged_df = merged_df.sort_values(by='ff_purchases', ascending=False)

# Save the final merged result to a new CSV file
final_output_file_path = 'output/FINAL_merged_output.csv'
merged_df.to_csv(final_output_file_path, index=False)

print(f"Final merged data has been saved to {final_output_file_path}")
