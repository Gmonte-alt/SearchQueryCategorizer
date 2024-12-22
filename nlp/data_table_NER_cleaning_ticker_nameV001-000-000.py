# data_table_NER_cleaning_ticker_name.py
# A python script that can craw a csv file of keywords and clean the keyword data according 
# to a list of processes to complete, in order:

# 1. lower-case all letters
# 2. replace periods in between words with spaces
# 3. remove special characters
# 4. remove duplicates

# incorporate multiple csv files, each with different column labels

# specify which columns to grab from each csv file. Also, I'll need 
# to grab different columns from the same csv file and process them all as one column.

#  incorporate an identifier so that I may identify that group of csv file plus column

# a special case where in one csv file plus column combination there are a list of words I want to remove that trail the keyword. The list of words is "corporation", "and company", "company", "inc", "group plc", "companies", "limited", "group", "holdings inc", and "partners lp". Can you update the python script to incorporate a separate function where I can use the 'Identifier' column to filter and submit this combination of csv file & column group into the function to remove words that are in that list? Also, could you also incorporate removing any trailing spaces, after those words are removed?

import pandas as pd
import os

# Function to clean keywords
# Function to clean keywords
def clean_keywords(keyword):
    # Lower-case all letters
    keyword = keyword.lower()
    # Replace periods with spaces
    keyword = keyword.replace('.', '')
    # Remove special characters: quotation marks, commas, and others
    keyword = ''.join(char for char in keyword if char.isalnum() or char.isspace())
    return keyword


# Function to remove specific words from keywords and trailing spaces
def remove_specific_words(keyword):
    # specific_words = ["corporation", "and company", "company", "incorporated", "group plc", "companies", "limited", "group", "holdings inc", "partners lp", "corp", "holding", "inc"]
    # for word in specific_words:
    #     keyword = keyword.replace(word, '')
    return keyword.strip()  # Remove trailing spaces

# Function to process CSV files
def process_csv(csv_file, columns_to_grab, identifier):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Clean each column separately
    cleaned_columns = {}
    for col in columns_to_grab:
        cleaned_columns[col] = df[col].astype(str).apply(clean_keywords)
        if identifier == 'Group7':  # Adjust as needed
            cleaned_columns[col] = cleaned_columns[col].apply(remove_specific_words)
    
    # Create a DataFrame with the cleaned keywords and identifier
    cleaned_df = pd.DataFrame(cleaned_columns)
    cleaned_df['Identifier'] = identifier
    
    # Save the cleaned data to a new CSV file
    cleaned_csv_file = os.path.splitext(csv_file)[0] + '_company' + identifier + '_cleaned.csv'
    cleaned_df.to_csv(cleaned_csv_file, index=False)
    print(f"Cleaned data saved to {cleaned_csv_file}")

# Dictionary specifying columns to grab for each CSV file and their identifier
csv_data = [
    ('data/tickers_list.csv', ['company', 'name'], 'Group7'),   # Specify columns for tickers_list.csv and their identifier
]

# Process each CSV file and its columns
for csv_file, columns_to_grab, identifier in csv_data:
    process_csv(csv_file, columns_to_grab, identifier)
