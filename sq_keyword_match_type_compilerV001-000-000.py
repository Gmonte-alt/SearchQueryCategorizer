# sq_keyword_match_type_compiler.py
# Output file:
# Version: V001-000-000
import csv

def filter_search_queries(input_file, output_file, threshold):
    # Initialize a list to store filtered search queries
    filtered_queries = []

    # Read data from input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search Query']
            search_query_words = search_query.split()
            impressions = [int(i.strip()) for i in row['Total Impressions'].split(',')]
            
            # Determine the match type for each search query
            target_keyword = []
            match_type = "Exact"
            for i, search_query_word in enumerate(search_query_words):
                for j, impression in enumerate(impressions):
                    if i == j and impression > 1000:
                        target_keyword.append(search_query_word)
            if len(search_query_words) == len(target_keyword):
                match_type = "Exact"
            else:
                match_type = "Phrase"
            
            # Append the filtered search query to the list
            filtered_queries.append({'search_query': search_query, 'target_keyword': ', '.join(target_keyword), 'match_type': match_type})

    # Write filtered data to output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['search_query', 'target_keyword', 'match_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for query in filtered_queries:
            writer.writerow(query)

# Example usage: Filter search queries with an impression threshold of 1000
filter_search_queries('data/sq_keyword_company_name_highest_match_results_single-word_output-metrics.csv', 'data/sq_keyword_recommended_match_type.csv', 1000)
