# Python file:  sq_keyword_company_name_finder.py 
# Input file:   data/tickers_list_companyGroup7_cleanedV001-000-001.csv
# Version file: V001-000-0018 #    Update with next iteration

# Version change notes: Reverting back to V001-000-009
# 
#         After processing the unmatched queries and finding matches, you can update the unmatched_queries list to remove the queries that have been matched
#
#         --note: I've used a copy of the unmatched_queries list (unmatched_queries[:]) to iterate over it. 
#               This allows you to safely remove items from the original list while iterating over it.
#               Inside the loop, after appending a matched query to the matches list, 
#               I remove that query from the unmatched_queries list using the remove method.
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

    # Check the context of the matched word in the search query and company name
    # 1 Last : Last
    if position == 'Last' and company_word_position == 'Last': # index + 1 >= search_query_len and j_index + 1 >= company_words_len:
        prev_search_word = search_query_words[index - 1]
        prev_company_word = company_words[j_index - 1]
       # next_company_word = company_words[j_index + 1]
    # 2 Last : Inside
    elif position == 'Last' and company_word_position == 'Inside': # index + 1 >= search_query_len and (j_index + 1 < company_words_len and j_index != 0):
        prev_search_word = search_query_words[index - 1]
        prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]
    # 3 Inside : Last
    elif position == 'Inside' and company_word_position == 'Last': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
    # 4 Beginning : Beginning
    elif position == 'Beginning' and company_word_position == 'Beginning': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        #prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        #prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]
    # 5 Beginning : Last
    elif position == 'Beginning' and company_word_position == 'Last': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        #prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
    # 6 Last : Beginning
    elif position == 'Last' and company_word_position == 'Beginning': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        prev_search_word = search_query_words[index - 1]
        # next_search_word = search_query_words[index + 1]
        next_company_word = company_words[j_index + 1]
    #  7 Beginning : Inside
    elif position == 'Beginning' and company_word_position == 'Inside': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        # prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]
    # 8 Inside : Beginning
    elif position == 'Inside' and company_word_position == 'Beginning': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        # prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]
    # 9 Inside : Inside
    else:
        prev_search_word = search_query_words[index - 1]
        next_search_word = search_query_words[index + 1]
        prev_company_word = company_words[j_index - 1]
        next_company_word = company_words[j_index + 1]

    # Check if either the previous or next words in both the search query and company name match
    # 1 Last : Last or # 2 Last : Inside or # 3 Inside : Last
    if (position == 'Last'or position == 'Inside'
        ) and (company_word_position == 'Last' or company_word_position == 'Inside'): # index + 1 >= search_query_len and j_index + 1 >= company_words_len:
        if prev_search_word.lower() == prev_company_word.lower():
            matched_words_count += 1
    # 4 Beginning : Beginning or #  7 Beginning : Inside or # 8 Inside : Beginning
    elif (position == 'Beginning' or position == 'Inside'
          ) and (company_word_position == 'Beginning' or company_word_position == 'Inside'): # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        if (next_search_word.lower() == next_company_word.lower()):
            matched_words_count += 1
    # 5 Beginning : Last or # 6 Last : Beginning
    elif position == 'Inside' and company_word_position == 'Inside': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
        if (prev_search_word.lower() == prev_company_word.lower() or 
            next_search_word.lower() == next_company_word.lower()):
            matched_words_count += 1
    # 5 Beginning : Last or # 6 Last : Beginning
    return matched_words_count, position, company_word_position

def output_highest_match(matches):
    # Group matches by search query
    grouped_matches = {}
    for match in matches:
        search_query = match[0]
        if search_query not in grouped_matches:
            grouped_matches[search_query] = [match]
        else:
            grouped_matches[search_query].append(match)
    
    # Process each group
    for search_query, group in grouped_matches.items():
        print(f"Search Query: {search_query}")
        
        # Sort the group by match count and then by the length of the company name
        sorted_group = sorted(group, key=lambda x: (x[2], len(x[1])), reverse=True)
        
        # Print the sorted group
        for item in sorted_group:
            print(item)
        
        # Extract the tuple with the highest match count and shortest company name
        highest_match = sorted_group[0]
        
        # Find the first occurrence of the search query + company name combination
        first_occurrence = None
        for match in group:
            if match[1] == highest_match[1]:
                first_occurrence = match
                break
        
        # Print the tuple with the highest match count and shortest company name
        print("Tuple with highest match count and shortest company name:", highest_match)
        
        # Print the tuple with the first occurrence positions
        if first_occurrence:
            print("Tuple with first occurrence positions:", first_occurrence)
        else:
            print("No first occurrence found for this company name.")
        
        # Add additional processing logic if needed
        
        print()  # Add a newline for readability
        
        # company_name = match[1]
        # match_count = match[2]
        # position = match[3]
        # company_word_position = match[4]
        # filtered_and_sorted_data = [
        # (sq, cn, mc, sqp, cnp)
        # for sq, cn, mc, sqp, cnp in sorted(matches, key=lambda x: x[2], reverse=True) 
        # if sq == search_query and cn == company_name]
        # print(filtered_and_sorted_data)
    # Process the extracted data accordingly

    #     print(f"Error: Invalid number of elements in matches tuple. Matches length: {len(matches)}")

def process_search_queries(search_query_file, company_file):
    """Process search queries and find associated company names."""
    company_names = load_company_data(company_file)
    matches = []  # Initialize matches list
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search Query'].strip()
            search_query_words = search_query.split()
            matches_found = False  # Flag to track if matches were found for this search query
            for company_name in company_names:
                company_words = company_name.split()
                match_count = 0  # Initialize match count
                total_matched_words = 0  # Initialize total matched words count
                if len(search_query_words) == 1 or len(company_words) == 1:
                    if search_query.lower() == company_name.lower():
                        match_count = 1
                        total_matched_words = 1
                        #matches.append((search_query, company_name, match_count, "Single word match", "Single word match", company_names[company_name]))
                        matches_found = True
                else:
                    for i, search_word in enumerate(search_query_words):
                        for j, company_word in enumerate(company_words):
                            if search_word.lower() == company_word.lower():
                                matched_words_count, position, company_word_position = check_context(search_query_words, company_words, i, j)
                                if matched_words_count > 0: #and search_query == 'growth fund of america': # 'realty income'
                                    match_count += 1  # Increment match count
                                    total_matched_words += matched_words_count
                                    matches_found = True  # Set flag to True as matches were found
                                    # print(search_query, company_name, match_count, position, company_word_position)
                #if matches_found:
                                    matches.append((search_query, company_name, match_count, position, company_word_position, company_names[company_name]))
                                    #print('Tuple length: ',len(matches))
    output_highest_match(matches)




if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #data/search_query_word_split_metrics-sp500.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/ticker_mktIndex_combined_data.csv" #data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)