# File name: word_array_Lookup.py
# Version: V000-000-006
# Output file:
# Notes: This next version builds on V000-000-005;
#        This code iterates through each search query and its lookup results. 
#        If a search query matches a ticker in the ticker table, it updates 
#        the corresponding columns in the search_query_results DataFrame accordingly. 
#        Finally, it prints the updated DataFrame. 
#        If it's a dictionary, you proceed with unpacking the items; otherwise, you handle 
#        the case where result is False.

import pandas as pd
import nltk
from nltk.stem import PorterStemmer

# Initialize the Porter Stemmer
porter = PorterStemmer()

def lookup_word(word, ticker_table, generic_core_table, company_table):
    # Words to exclude from matching
    exclude_words = ["corporation", "inc", "corp", "llc", "incorporated"]

    # Convert word to lowercase for case-insensitive comparison
    word_lower = word.lower()

    # Check for exact match in ticker table
    ticker_match = ticker_table[ticker_table['ticker'].str.lower() == word_lower]
    if not ticker_match.empty:
        return {word: ('Ticker', ticker_match['stand-alone'].values[0], ticker_match['named_entity'].values[0])}

    # Remove ".com" from company names and replace comma with space for matching
    company_table['company'] = company_table['company'].str.replace('.com', '').str.replace(',', '')

    # Check for exact match in company table
    company_match = company_table[company_table['company'].str.lower() == word_lower]
    if not company_match.empty:
        return {word: ('Company', company_match['stand-alone'].values[0], company_match['named_entity'].values[0])}

    # Check if word is not in exclude list and then proceed with partial match in company table
    if word_lower not in exclude_words:
        # Check for partial match in company table
        partial_match = company_table[company_table['company'].str.lower().apply(lambda x: word_lower in x.lower().split())]
        if not partial_match.empty:
            return {word: ('Company', partial_match['stand-alone'].values[0], partial_match['named_entity'].values[0])}

    # Stem the word for matching in generic core table
    word_stemmed = porter.stem(word_lower)

    # Check for match in generic core table (including singular/plural forms)
    generic_core_match = generic_core_table[generic_core_table['generic_core'].apply(porter.stem).str.lower() == word_stemmed]
    if not generic_core_match.empty:
        return {word: ('Generic-core', generic_core_match['stand-alone'].values[0], generic_core_match['named_entity'].values[0])}

    # If no match found
    return {word: False}

def split_and_lookup(query, ticker_table, generic_core_table, company_table):
    words = query.split()
    results = []
    for word in words:
        lookup_result = lookup_word(word, ticker_table, generic_core_table, company_table)
        results.append(lookup_result)
    return results

def process_search_query(query, lookup_results):
    status = 'open'
    qualified_target = False
    targetable_keyword = ''
    exact_match = False
    named_entity = False
    stand_alone = False
    
    for idx, result in enumerate(lookup_results):
        if any(value == False for value in result.values()):
            continue
        else:
            for word, (match_type, is_standalone, is_named_entity) in result.items():
                if match_type == 'Ticker' and word.lower() == query.lower():
                    status = 'closed'
                    qualified_target = True
                    targetable_keyword = query
                    exact_match = True
                    named_entity = is_named_entity
                    stand_alone = True
                    break
                elif match_type == 'Generic-core' and word.lower() == query.lower():
                    status = 'closed'
                    qualified_target = True
                    targetable_keyword = query
                    exact_match = True
                    named_entity = is_named_entity
                    stand_alone = True
                    break

    return {
        'Search Query': query,
        'Matching Requirement Met': any(result[word] for result in lookup_results for word in result),
        'Status': status,
        'qualified_target': qualified_target,
        'targetable keyword': targetable_keyword,
        'exact_match': exact_match,
        'named_entity': named_entity,
        'stand-alone': stand_alone
    }

def main():
    # Example tables with stand-alone column
    ticker_table_data = {
        'ticker': ['nvda', 'tsla', 'aapl'],
        'stand-alone': [True, True, True],
        'named_entity': [True, True, True]  # Add named_entity column
    }
    ticker_table = pd.DataFrame(ticker_table_data)

    generic_core_table_data = {
        'generic_core': ['stock', 'analysis', 'share', 'forecast', 'prediction', 'earning', 'outlook', 'price'],
        'stand-alone': [True, True, True, True, True, True, True, True],
        'named_entity': [False, False, False, False, False, False, False, False]  # Add named_entity column
    }
    generic_core_table = pd.DataFrame(generic_core_table_data)

    company_table_data = {
        'company': ['Microsoft Corporation', 'NVIDIA Corporation', 'Amazon.com, Inc.', 'Apple Inc.','JPMorgan Chase & Co.', 'Bank of America Corporation'],
        'stand-alone': [False, False, False, False, False, False],
        'named_entity': [True, True, True, True, True, True]  # Add named_entity column
    }
    company_table = pd.DataFrame(company_table_data)

    # Create an empty DataFrame to track search query results
    search_query_results = pd.DataFrame(columns=['Search Query', 'Matching Requirement Met', 'Status', 'qualified_target', 'targetable keyword', 'exact_match', 'named_entity', 'stand-alone'])

    # Example search queries
    search_queries = [
        "nvda stock analysis",
        "nvda",
        "stocks",
        "buy nvda stock",
        "nvidia stock analysis",
        "ai stocks",
        "apple stock price",
        "amazon stock",
        "microsoft news",
        "types of corporation",
        "companies to invest in",
        "best stocks to buy"
    ]

    # Process each search query
    for query in search_queries:
        # Perform lookups for the current search query
        lookup_results = split_and_lookup(query, ticker_table, generic_core_table, company_table)
        
        # Check if the search query contains a ticker and update named_entity accordingly
        named_entity = any(result[word][2] for result in lookup_results for word in result if result[word] != False)
        
        # Append the result to the search query results DataFrame
        search_query_results = pd.concat([search_query_results, pd.DataFrame(process_search_query(query, lookup_results), index=[0])], ignore_index=True)

    # Display the search query results
    print(search_query_results)

if __name__ == "__main__":
    main()
