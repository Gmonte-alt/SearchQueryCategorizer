# File name: word_array_Lookup.py
# Version: V000-000-000
# Output file:
# Notes: Looks-up words from search queries in tables and identifies the table
#        the word belongs to, returning an array for that word
#        This version utilizes nltk PorterStemmer to look-up plural word types i.e. stock vs stocks

import pandas as pd
import nltk
from nltk.stem import PorterStemmer

# Initialize the Porter Stemmer
porter = PorterStemmer()

def lookup_word(word, ticker_table, generic_core_table):
    # Convert word to lowercase for case-insensitive comparison
    word_lower = word.lower()

    # Check for exact match in ticker table
    ticker_match = ticker_table[ticker_table['ticker'].str.lower() == word_lower]
    if not ticker_match.empty:
        return {word: ('Ticker', ticker_match['stand-alone'].values[0])}

    # Stem the word for matching in generic core table
    word_stemmed = porter.stem(word_lower)

    # Check for match in generic core table (including singular/plural forms)
    generic_core_match = generic_core_table[generic_core_table['generic_core'].apply(porter.stem).str.lower() == word_stemmed]
    if not generic_core_match.empty:
        return {word: ('Generic-core', generic_core_match['stand-alone'].values[0])}

    # If no match found
    return {word: False}

def split_and_lookup(query, ticker_table, generic_core_table):
    words = query.split()
    results = []
    for word in words:
        lookup_result = lookup_word(word, ticker_table, generic_core_table)
        results.append(lookup_result)
    return results

def main():
    # Example tables with stand-alone column
    ticker_table_data = {
        'ticker': ['nvda', 'tsla', 'aapl'],
        'stand-alone': [True, True, True]
    }
    ticker_table = pd.DataFrame(ticker_table_data)

    generic_core_table_data = {
        'generic_core': ['stock', 'analysis', 'share', 'forecast', 'prediction', 'earning', 'outlook', 'price'],
        'stand-alone': [True, True, True, True, True, True, True, True]
    }
    generic_core_table = pd.DataFrame(generic_core_table_data)

    # Example search queries
    search_queries = [
        "nvda stock analysis",
        "nvda",
        "buy nvda stock",
        "nvidia stock analysis",
        "ai stocks"
    ]

    # Perform lookups for each search query
    for query in search_queries:
        lookup_results = split_and_lookup(query, ticker_table, generic_core_table)

        # Print the lookup results
        print(f"Lookup results for query '{query}':")
        for result in lookup_results:
            for key, value in result.items():
                if value:
                    print(f"{key}: {value[0]} (Stand-alone: {value[1]})")
                else:
                    print(f"{key}: {value}")

if __name__ == "__main__":
    main()
