# sq_keyword_word-split_lookup.py
# Output file: data/search_query_word_split_metrics.csv output/FINAL_merged_output.csv output/search_query_word_frequency.csv
import csv

def load_reference_table(reference_file):
    """Load the reference table from a CSV file."""
    reference_table = {}
    with open(reference_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['Word'].strip()  # Assuming the word column is named 'Word'
            ff_purchases_metric = row['Total ff_purchases']  # Assuming the conversion metric column is named 'Conversion Metric'
            reference_table[word] = ff_purchases_metric
    return reference_table

def process_search_queries(search_query_file, reference_table):
    """Process the search queries and look up conversion metrics."""
    search_query_metrics = []
    with open(search_query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            search_query = row['Search term'].strip()  # Assuming the search query column is named 'Search Query'
            ff_purchases = row['ff_purchases']  # Assuming the impressions column is named 'Impressions'
            query_metrics = []
            for word in search_query.split():
                ff_purchases_metric = reference_table.get(word, None)
                if ff_purchases_metric:
                    query_metrics.append(ff_purchases_metric)
            search_query_metrics.append({
                'Search Query': search_query,
                'SQ_ff_purchases': ff_purchases,
                'Total ff_purchases': ', '.join(query_metrics)
            })
    return search_query_metrics

def write_output(output_file, search_query_metrics):
    """Write the processed search queries with conversion metrics to an output CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Search Query', 'SQ_ff_purchases', 'Total ff_purchases']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in search_query_metrics:
            writer.writerow(row)

if __name__ == "__main__":
    reference_file = "output/search_query_word_frequency.csv"  # Path to the CSV file containing the reference table
    search_query_file = "output/NEW_filtered_aggregated_output.csv" # "data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped_metrics.csv"  # Path to the CSV file containing the search queries
    output_file = "output/search_query_word_split_metrics.csv"  # Output CSV file

    # Load reference table
    reference_table = load_reference_table(reference_file)

    # Process search queries and look up conversion metrics
    search_query_metrics = process_search_queries(search_query_file, reference_table)

    # Write the processed search queries with conversion metrics to an output CSV file
    write_output(output_file, search_query_metrics)
