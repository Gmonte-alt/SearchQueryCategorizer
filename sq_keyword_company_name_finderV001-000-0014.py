# Python file:  sq_keyword_company_name_finder.py 
# Input file:   data/tickers_list_companyGroup7_cleanedV001-000-001.csv
# Version file: V001-000-0014 #    Update with next iteration

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
#         --note: The last file update was near perfect. Next we need to surface the ticker symbol.
#               This script updates the load_company_data function to include the name column as well.
#               Then, when iterating through the company_names dictionary, you can retrieve the company name and its associated name.
#               the output_highest_match function has been modified to include the company_name_column variable, 
#               which represents the name column from the company_file. This column is retrieved from the matches list and printed 
#               alongside other variables. Additionally, when appending matches to the matches list, the company_names[company_name] is included to fetch the corresponding name from the company_names dictionary

import csv
import re

common_words = {"corp", "corporation", "group", "capital", "trust", "stock", "inc", "incorp", "equity", "equities", "incorporated"}

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
    
    # Fork the path for company_name is >2, so the else can publish shorter matches that don't have an inside word.
    if company_words_len > 2:
        # Check the context of the matched word in the search query and company name
        # # 1 Last : Last
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
        if position == 'Last' and company_word_position == 'Last': # index + 1 >= search_query_len and j_index + 1 >= company_words_len:
            if prev_search_word.lower() == prev_company_word.lower():
                matched_words_count += 1
        # 4 Beginning : Beginning or #  7 Beginning : Inside or # 8 Inside : Beginning
        elif position == 'Beginning' and company_word_position == 'Inside': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
            if (next_search_word.lower() == next_company_word.lower()):
                matched_words_count += 1
        # 5 Beginning : Last or # 6 Last : Beginning
        elif position == 'Inside' and company_word_position == 'Inside': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
            if (prev_search_word.lower() == prev_company_word.lower() or 
                next_search_word.lower() == next_company_word.lower()):
                matched_words_count += 1
        # 5 Beginning : Last or # 6 Last : Beginning
        elif position == 'Beginning' and company_word_position == 'Beginning': # (index + 1 < search_query_len and index != 0) and j_index + 1 >= company_words_len:
            if next_company_word.lower() not in common_words and next_search_word.lower() == next_company_word.lower():
                matched_words_count += 1
        elif position == 'Inside' and company_word_position == 'Beginning':
            if next_company_word.lower() not in common_words and next_search_word.lower() == next_company_word.lower():
                matched_words_count += 1
    elif company_word_position == 'Beginning':
        matched_words_count += 1
    
    return matched_words_count, position, company_word_position

def output_highest_match(matches):
    #filtered_matches = [match for match in matches if match[2] > 0] # and match[0].lower() == 'realty income'] 
    #print(filtered_matches)
    for match in matches:
        search_query = match[0]
        company_name = match[1]
        company_name_column = match[5]
        # match_count = match[2]
        # position = match[3]
        # company_word_position = match[4]
        filtered_and_sorted_data = [
        (sq, cn, mc, sqp, cnp, ct)
        for sq, cn, mc, sqp, cnp, ct in sorted(matches, key=lambda x: x[2], reverse=True) 
        if sq == search_query and cn == company_name]
        print(filtered_and_sorted_data)
    # Process the extracted data accordingly

    # if len(matches) == 5:
    #     search_query, company_name, match_count, position, company_word_position = matches
    #     print(f"Search Query: {search_query}")
    #     print(f"Matched Company Name: {company_name}")
    #     print(f"Number of Combinations: {match_count}")
    #     print(f"Position in Search Query: {position}")
    #     print(f"Position in Company Name: {company_word_position}")
    #     print()
    # else:
    #     print(f"Error: Invalid number of elements in matches tuple. Matches length: {len(matches)}")

def process_search_queries(search_query_file, company_file):
    """Process search queries and find associated company names."""
    company_names = load_company_data(company_file)
    matches = []  # Initialize matches list
    unmatched_queries = []  # Initialize list to store unmatched queries
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
                        matches.append((search_query, company_name, match_count, "Single word match", "Single word match", company_names[company_name]))
                        matches_found = True
                else:
                    for i, search_word in enumerate(search_query_words):
                        for j, company_word in enumerate(company_words):
                            if search_word.lower() == company_word.lower():
                                matched_words_count, position, company_word_position = check_context(search_query_words, company_words, i, j)
                                if matched_words_count > 0: # search_word == 'amazon': #'microsoft': # 'growth fund of america': # 'realty income'
                                #    print(search_word.lower() == company_word.lower())
                                    match_count += 1  # Increment match count
                                    total_matched_words += matched_words_count
                                    matches_found = True  # Set flag to True as matches were found
                                    # print(search_query, company_name, match_count, position, company_word_position)
                #if matches_found:
                                    matches.append((search_query, company_name, match_count, position, company_word_position, company_names[company_name]))
                                    #print('Tuple length: ',len(matches))
            if not matches_found:
                unmatched_queries.append(search_query)  # Add unmatched query to the list
    
        # Path to the CSV file
    csv_file = 'data/search_query_keyword_company_name_unmatched_list.csv'

    # Writing the list of unmatched queries to a CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Unmatched Queries'])  # Writing header
        writer.writerows([[query] for query in unmatched_queries])  # Writing each query as a separate row

    print("Data has been written to", csv_file)
    
    output_highest_match(matches)
    
    # Print unmatched queries
    if unmatched_queries:
        print("Unmatched Queries:")
        print(f"Length of list: {len(unmatched_queries)}")
        #for query in unmatched_queries:
        #   print(query)
        # Path to the CSV file

    else:
        print("All search queries were matched.")


if __name__ == "__main__":
    search_query_file = "data/search_query_word_split_metrics.csv" #search_queries.csv"  # Path to the CSV file containing search queries
    company_file = "data/tickers_list_companyGroup7_cleaned.csv" #company_names.csv"  # Path to the CSV file containing company names
    process_search_queries(search_query_file, company_file)