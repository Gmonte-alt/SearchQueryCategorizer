# sq_keyword_company_name_finder.py 
# data/tickers_list_companyGroup7_cleanedV001-000-001.csv

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

def is_valid_word(word):
    """Check if a word is valid."""
    if len(word) <= 1:  # Exclude single-character words
        return False
    if re.match(r'^\d+$', word):  # Exclude numerical values
        return False
    excluded_words = {'news', 'corporation', 'inc', 'incorporated', 'stock', 'to', 'global', 'price', 'share',
                      'growth', 'manufactur', 'trading', 'the', 'value', 'target', 'and', 'preferred', 'portfolio',
                      'equities', 'in', 'world', 'best', 'market', 'housing', 'government', 'income', 'of',
                      'investments', 'equity', 'holdings', 'on', 'money'}
    if word.lower() in excluded_words:  # Exclude specific words
        return False
    return True

def check_context(search_query_words, company_words, index):
    """Check the context of the matched word."""
    if index > 0 and index < len(search_query_words) - 1:
        prev_search_word = search_query_words[index - 1]
        prev_company_word = company_words[index - 1]
        next_search_word = search_query_words[index + 1]
        if index < len(company_words) - 1:
            next_company_word = company_words[index + 1]
            if prev_search_word.lower() != prev_company_word.lower() or next_search_word.lower() != next_company_word.lower():
                return False
    elif index == 0 and len(search_query_words) > 1:
        next_search_word = search_query_words[index + 1]
        if index < len(company_words) - 1:
            next_company_word = company_words[index + 1]
            if next_search_word.lower() != next_company_word.lower():
                return False
    elif index == len(search_query_words) - 1 and len(search_query_words) > 1:
        prev_search_word = search_query_words[index - 1]
        prev_company_word = company_words[index - 1]
        if prev_search_word.lower() != prev_company_word.lower():
            return False
    return True

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
                for i, search_word in enumerate(search_query_words):
                    for j, company_word in enumerate(company_words):
                        if search_word.lower() == company_word.lower() and check_context(search_query_words, company_words, i):
                            print(f"Search Query: {search_query}")
                            print(f"Matched Company Name: {company_name}")
                            print()
                            break


if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)

