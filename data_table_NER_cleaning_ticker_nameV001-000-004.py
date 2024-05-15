# data_table_NER_cleaning_ticker_nameV001-000-0003.py
# data/tickers_list_companyGroup7_cleaned.csv
# Current version V001-000-003
# A python script that can craw a csv file of keywords and clean the keyword data according 
# to a list of processes to complete, in order:

# 1. lower-case all letters
# 2. replace periods in between words with spaces
# 3. remove special characters
# 4. remove duplicates

# -- note Updated for removing .com from the company name and remove double spaces.
#       updated the code to not remove the "&"
# columns to name 'company', 'name', 'Identifier'
# In this modified version, I've removed the loop for processing individual CSV files 
# and replaced it with a function (process_csv) that accepts a list of CSV files, corresponding 
# columns to grab, and identifiers. This function reads each CSV file, cleans the 
# specified columns, concatenates the resulting dataframes, and saves the combined and cleaned
# data into a single CSV file.

import pandas as pd

# Function to clean keywords
def clean_keywords(keyword):
    # Lower-case all letters
    keyword = keyword.lower()
    # Remove ".com" from company names
    if ".com" in keyword:
        keyword = keyword.replace(".com", "")
    # Replace periods with spaces
    keyword = keyword.replace('.', '')
    # Remove special characters: quotation marks, commas, and others, except '&'
    keyword = ''.join(char for char in keyword if char.isalnum() or char.isspace() or char == '&')
    # Replace double spaces with single spaces
    keyword = ' '.join(keyword.split())
    return keyword

# Function to process CSV files
def process_csv(csv_files, columns_to_grab, identifiers):
    # Initialize an empty list to store DataFrames
    dfs = []

    # Process each CSV file and its columns
    for csv_file, cols_to_grab, identifier in zip(csv_files, columns_to_grab, identifiers):
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        print("Column names in DataFrame:")
        print(df.columns)
        print("Columns to grab:", cols_to_grab)

        # Clean each column separately
        cleaned_columns = {}
        for col in cols_to_grab:
            print("Processing column:", col)
            cleaned_columns[col] = df[col].astype(str).apply(clean_keywords)
    
        # Create a DataFrame with the cleaned keywords and identifier
        cleaned_df = pd.DataFrame(cleaned_columns)
        
        # Flatten the columns_to_grab list if it's a list of tuples
        if isinstance(cols_to_grab[0], tuple):
            cols_to_grab = [col for cols in cols_to_grab for col in cols]

        # Reorder the columns according to a specific order
        cleaned_df = cleaned_df[cols_to_grab]

        # Create a list of identifiers with the same length as the DataFrame
        identifiers_list = [identifier] * len(cleaned_df)

        # Assign the list of identifiers to the 'Identifier' column
        cleaned_df['Identifier'] = identifiers_list
        
        # Append the DataFrame to the list
        dfs.append(cleaned_df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    return combined_df

# Dictionary specifying columns to grab for each CSV file and their identifier
csv_data = [
    ('data/tickers_list.csv', ['company', 'name'], 'Group7'),   # Specify columns for tickers_list.csv and their identifier
    ('data/Table_MarketIndexData-Table-mktxV2.csv', ['company', 'name'], 'Group7')
]

# Process each CSV file and its columns
combined_data = process_csv(*zip(*csv_data))  # Unpack the zip of csv_data
combined_csv_file = 'data/ticker_mktIndex_combined_data.csv'
combined_data.to_csv(combined_csv_file, index=False)
print(f"Combined data saved to {combined_csv_file}")
