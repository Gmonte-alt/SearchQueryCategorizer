# Below is a Python script that reads all the CSV files specified in the csv_files dictionary and concatenates them into a single TSV (tab-separated values) file:
# preprocess_NER_keyword_csv_to_tsv.py

import pandas as pd

# Dictionary specifying CSV files
csv_files = {
    'data/keyword_data_training-kw_only_transposed_V2.csv': 'Group1'#, data/Table_GeographicData-Table-GeoGroup1_cleaned.csv
    # 'data/Table_CommoditiesData-Table-comGroup2_cleaned.csv': 'Group2',
    # 'data/Table_MarketIndexData-Table-mktxGroup3_cleaned.csv': 'Group3',
    # 'data/Table_WorldCurrencyData-Table-curGroup4_cleaned.csv': 'Group4',
    # 'data/Table_CurrencyIndexData-Table-curGroup5_cleaned.csv': 'Group5',
    # 'data/tickers_listGroup6_cleaned.csv': 'Group6',
    # 'data/tickers_listGroup7_cleaned.csv': 'Group7',
    # 'data/tickers_listGroup8_cleaned.csv': 'Group8',
}

# Initialize an empty list to store DataFrames
dfs = []

# Read each CSV file and append its DataFrame to the list
for csv_file, identifier in csv_files.items():
    df = pd.read_csv(csv_file)
    df['Identifier'] = identifier  # Add Identifier column
    dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs)

# Save the combined DataFrame to a TSV file
combined_df.to_csv('data/preprocess_NER_tsv_combined_data.tsv', sep='\t', index=False)

print("Combined data saved to data/preprocess_NER_tsv_combined_data.tsv")
