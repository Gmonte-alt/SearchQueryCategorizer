# Python file:  sq_keyword_company_name_finder.py 
# Input file:   data/tickers_list_companyGroup7_cleanedV001-000-001.csv
# Version file: V001-000-007 #    Update with next iteration

# Version change notes:
# 
#         In the prior version, V001-000-007, I identified key data points from the search query to 
#         company name matches inside the check_context function. I have yet to identify match strengths.
#         In this next version we're going to move outside of the check context and begin developing
#         methods to identify match rates, i.e. percentage match. 
#         In order to accomplish this, we'll need to: 
#         1) window each search query + Matched Company Name,
#         2) surface the highest "Number of Combinations" value to the top, 
#         3) surface "Number of Combinations: 1" relative "Position in Company Name: ", 
#         4) surface the "Number of Combinations: 1" "Position in Search Query" 
#
#         --note: We introduced a new function, "output_highest_match" & changed the 
#               "process_search_queries" function. Next is to incorporate a tuple to send into "output_highest_match". 
#
#

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
    matched_words_count = 0
    position = 'Outside'
    company_word_position = 'Outside'
    
    # Check if the matched word is at the beginning or end of the search query
    if index == 0:
        position = 'Beginning'
    elif index == search_query_len - 1:
        position = 'Last'
    else:
        position = 'Inside'

    # Check if the matched word is at the beginning or end of the search query
    if j_index == 0:
        company_word_position = 'Beginning'
    elif j_index == company_words_len - 1:
        company_word_position = 'Last'
    else:
        company_word_position = 'Inside'
    
    # Ensure that the index is within the bounds of the company_words list
    # if j_index + 1 >= company_words_len:
    #     return False, position, company_word_position

    # Ensure that the next word index is within the bounds of the search_query_words list
    # if index + 1 >= search_query_len:
    #     return False, position

    # Check the context of the matched word in the search query and company name
    prev_search_word = search_query_words[index - 1]
    if index + 1 >= search_query_len and j_index + 1 >= company_words_len:
        prev_company_word = company_words[j_index - 1]
       # next_company_word = company_words[j_index + 1]
    elif index + 1 >= search_query_len and j_index + 1 < company_words_len:
        prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]
    elif index + 1 < search_query_len and j_index + 1 >= company_words_len:
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
    else:
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]

    # Check if either the previous or next words in both the search query and company name match
    if index + 1 >= search_query_len or j_index + 1 >= company_words_len:
        if prev_search_word.lower() == prev_company_word.lower(): matched_words_count += 1
    else:
        if (prev_search_word.lower() == prev_company_word.lower() or 
            next_search_word.lower() == next_company_word.lower()):
            matched_words_count += 1
    return matched_words_count, position, company_word_position

def output_highest_match(search_query, company_name, match_count, total_matched_words, position, company_word_position):
    """Output the highest match count along with relevant information."""
    print(f"Search Query: {search_query}")
    print(f"Matched Company Name: {company_name}")
    print(f"Number of Combinations: {match_count}")
    print(f"Total Length of Search Queries Matched: {total_matched_words}")
    print(f"Position in Search Query: {position}")
    print(f"Position in Company Name: {company_word_position}")
    print()

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
                total_matched_words = 0  # Initialize total matched words count
                for i, search_word in enumerate(search_query_words):
                    for j, company_word in enumerate(company_words):
                        if search_word.lower() == company_word.lower():
                            matched_words_count, position, company_word_position = check_context(search_query_words, company_words, i, j)
                            if matched_words_count > 0:
                                match_count += 1  # Increment match count
                                total_matched_words += matched_words_count
                                output_highest_match(search_query, company_name, match_count, total_matched_words, position, company_word_position)
                                break

if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)