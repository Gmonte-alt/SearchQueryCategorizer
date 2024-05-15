# sq_keyword_company_name_finder.py 
# data/tickers_list_companyGroup7_cleanedV001-000-001.csv

import csv

def load_company_names(company_file):
    """Load company names from a CSV file."""
    company_names = set()
    with open(company_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = row['company'].strip()  # Assuming the company column is labeled 'company'
            company_names.add(company_name)
    return company_names

def find_company_names_in_query(search_query, company_names):
    """Find company names in a search query."""
    if "nvidia" in search_query.lower():
        return {"NVIDIA"}
    return set()

def process_search_queries(search_query_file, company_file):
    """Process search queries and find associated company names."""
    company_names = load_company_names(company_file)
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search Query'].strip()  # Assuming the search query column is labeled 'Search Query'
            if "nvidia" in search_query.lower():
                found_companies = find_company_names_in_query(search_query, company_names)
                print(f"Search Query: {search_query}")
                if found_companies:
                    print(f"Found Companies: {', '.join(found_companies)}")
                else:
                    print("No associated company found.")
                print()

if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)
