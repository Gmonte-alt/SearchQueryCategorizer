# Python file:  sq_keyword_company_name_finder.py 
# Input file:   data/tickers_list_companyGroup7_cleanedV001-000-001.csv
# Version file: V001-000-005 #    Update with next iteration

# Version change notes:
# 
#         Included a "Number of Combinations:" which could result in a value of 1 or greater
#         The expectation is that this value will be used as a filtering method

import csv
import re

def load_company_data(company_file):
    """Load company data from a CSV file."""
    company_data = {}
    with open(company_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = row['company'].strip()  # Assuming the company column is labeled 'company'
            name = row['name'].strip()  # Assuming the name column is labeled 'name'
            company_data[company_name] = name
    return company_data

def check_context(search_query_words, company_words, index, j_index):
    """Check the context of the matched word."""
    search_query_len = len(search_query_words)
    company_words_len = len(company_words)
    
    # Check if the matched word is at the beginning or end of the search query
    if index == 0 or index == search_query_len - 1:
        return False
    
    # Ensure that the index is within the bounds of the company_words list
    if j_index + 1 >= company_words_len:
        return False

    # Check the context of the matched word in the search query and company name
    prev_search_word = search_query_words[index - 1]
    next_search_word = search_query_words[index + 1]
    prev_company_word = company_words[j_index - 1]
    next_company_word = company_words[j_index + 1]

    # Check if either the previous or next words in both the search query and company name match
    if (prev_search_word.lower() == prev_company_word.lower() or
        next_search_word.lower() == next_company_word.lower()):
        return True
    
    return False

def process_search_queries(search_query_file, company_file):
    """Process search queries and find associated company names."""
    company_names = load_company_data(company_file)
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search Query'].strip()
            search_query_words = search_query.split()
            for company_name in company_names:
                company_words = company_name.split()
                match_count = 0  # Initialize match count
                for i, search_word in enumerate(search_query_words):
                    for j, company_word in enumerate(company_words):
                        if search_word.lower() == company_word.lower() and check_context(search_query_words, company_words, i, j):
                            match_count += 1  # Increment match count
                            print(f"Search Query: {search_query}")
                            print(f"Matched Company Name: {company_name}")
                            print(f"Number of Combinations: {match_count}")
                            print()
                            break

if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)

