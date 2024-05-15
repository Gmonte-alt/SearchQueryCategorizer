# Next version of keyword_data_transpose.py. This time with Dictionary to upload multiple csv files

import pandas as pd

# Function to process a single CSV file
def process_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Initialize an empty list to store the rows
    rows = []
    
    # Iterate over each row
    for index, row in df.iterrows():
        # Split the cleaned keyword into individual words
        words = str(row['Cleaned Keyword']).split()
        # Initialize a flag to track the first word
        first_word = True
        # Initialize the tag to None
        tag = None
        # Iterate over each word
        for word in words:
            # Determine the tag based on the 'Identifier' column
            identifier = row['Identifier']
            if identifier == 'Group1':
                tag = 'geo'
            elif identifier == 'Group2' or identifier == 'Group8':
                tag = 'act'
            elif identifier == 'Group3' or identifier == 'Group6' or identifier == 'Group7':
                tag = 'org'
            elif identifier == 'Group4' or identifier == 'Group5':
                tag = 'cur'
            # Assign "B-" tag to the first word that is not a period
            if word != '.' and first_word:
                rows.append([word, 'B-' + tag])
                first_word = False
            # Assign "I-" tag to subsequent words that are not periods
            elif word != '.':
                rows.append([word, 'I-' + tag])
        # Add a period after each item
        rows.append(['.', 'O'])
    
    # Create a DataFrame from the list of rows
    result = pd.DataFrame(rows, columns=['word', 'bio_tag'])
    
    return result

# Dictionary specifying CSV files
csv_files = {
    'data/Table_GeographicData-Table-GeoGroup1_cleaned.csv': 'Group1',
    'data/Table_CommoditiesData-Table-comGroup2_cleaned.csv': 'Group2',
    'data/Table_MarketIndexData-Table-mktxGroup3_cleaned.csv': 'Group3',
    'data/Table_WorldCurrencyData-Table-curGroup4_cleaned.csv': 'Group4',
    'data/Table_CurrencyIndexData-Table-curGroup5_cleaned.csv': 'Group5',
    'data/tickers_listGroup6_cleaned.csv': 'Group6',
    'data/tickers_listGroup7_cleaned.csv': 'Group7',
    'data/tickers_listGroup8_cleaned.csv': 'Group8',
    # Add more CSV files and their corresponding identifiers as needed
}

# Initialize an empty DataFrame to store the results
final_result = pd.DataFrame(columns=['word', 'bio_tag'])

# Process each CSV file and concatenate the results
for csv_file, identifier in csv_files.items():
    result = process_csv(csv_file)
    final_result = pd.concat([final_result, result], ignore_index=True)

# Save the final result to a new CSV file
final_result.to_csv('data/keyword_data_training-kw_only_transposed_V2.csv', index=False)

print("Keywords transposed successfully with tags added!")

