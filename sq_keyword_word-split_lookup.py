# sq_keyword_word-split_lookup.py
# Output file: data/search_query_word_split_metrics.csv
import csv

def load_reference_table(reference_file):
    """Load the reference table from a CSV file."""
    reference_table = {}
    with open(reference_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['Word'].strip()  # Assuming the word column is named 'Word'
            impression_metric = row['Total Impressions']  # Assuming the conversion metric column is named 'Conversion Metric'
            reference_table[word] = impression_metric
    return reference_table

def process_search_queries(search_query_file, reference_table):
    """Process the search queries and look up conversion metrics."""
    search_query_metrics = []
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search_term'].strip()  # Assuming the search query column is named 'Search Query'
            impressions = row['Impressions']  # Assuming the impressions column is named 'Impressions'
            query_metrics = []
            for word in search_query.split():
                impression_metric = reference_table.get(word, None)
                if impression_metric:
                    query_metrics.append(impression_metric)
            search_query_metrics.append({
                'Search Query': search_query,
                'SQ_Impressions': impressions,
                'Total Impressions': ', '.join(query_metrics)
            })
    return search_query_metrics

def write_output(output_file, search_query_metrics):
    """Write the processed search queries with conversion metrics to an output CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Search Query', 'SQ_Impressions', 'Total Impressions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in search_query_metrics:
            writer.writerow(row)

if __name__ == "__main__":
    reference_file = "data/search_query_word_frequency.csv"  # Path to the CSV file containing the reference table
    search_query_file = "data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped_metrics.csv"  # Path to the CSV file containing the search queries
    output_file = "data/search_query_word_split_metrics.csv"  # Output CSV file

    # Load reference table
    reference_table = load_reference_table(reference_file)

    # Process search queries and look up conversion metrics
    search_query_metrics = process_search_queries(search_query_file, reference_table)

    # Write the processed search queries with conversion metrics to an output CSV file
    write_output(output_file, search_query_metrics)
