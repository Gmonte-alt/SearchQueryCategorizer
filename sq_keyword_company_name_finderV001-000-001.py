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


def process_search_queries(search_query_file, company_file):
    """Process search queries and find associated company names."""
    company_data = load_company_data(company_file)
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search Query'].strip()  # Assuming the search query column is labeled 'Search Query'
            words = search_query.split()
            found_companies = set()
            for word in words:
                if is_valid_word(word):
                    for company_name, name in company_data.items():
                        if word.lower() in company_name.lower().split():
                            found_companies.add((company_name, name))
                            break  # Exit inner loop if a match is found
            if found_companies:
                for company_name, name in found_companies:
                    print(f"Search Query: {search_query}, Company Name: {company_name}, Ticker: {name}")
            else:
                print(f"No company found for search query: {search_query}")

if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)
