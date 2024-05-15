# sq_keyword_frequency_counter.py
# Output file: data/search_query_word_frequency.csv
# Below is a Python script that reads a search query CSV file, counts the frequency of each word, and then writes the word-frequency pairs to an output CSV file:
# file name: sq_keyword_frequency_counter.py

import csv
from collections import Counter

def count_word_frequency(query_file):
    """Count the frequency of each word and the total metrics in the search query file."""
    word_frequency = Counter()
    impressions_total = Counter()
    # clicks_total = Counter()  # Initialize clicks_total as Counter
    # conversions_total = Counter()  # Initialize conversions_total as Counter
    # spend_total = Counter()  # Initialize spend_total as Counter
    with open(query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row
        # clicks_index = header.index('Clicks') if 'Clicks' in header else None
        # conversions_index = header.index('Conversions') if 'Conversions' in header else None
        # spend_index = header.index('Spend') if 'Spend' in header else None
        # if clicks_index is None:
        #     raise ValueError("Clicks column not found in input CSV file")
        # if conversions_index is None:
        #     raise ValueError("Conversions column not found in input CSV file")
        # if spend_index is None:
        #     raise ValueError("Spend column not found in input CSV file")
        for row in reader:
            query = row[0].strip()  # Assuming search queries are in the first column
            impressions = int(row[1])  # Assuming impressions are in the second column
            # clicks = int(row[clicks_index])
            # conversions = float(row[conversions_index])  # Convert to float instead of int
            # spend = int(float(row[spend_index].replace('$', '').replace(',', '')))  # Remove $ and , before converting to float and then int
            words = query.split()
            word_frequency.update(words)
            for word in set(words):
                impressions_total[word] += impressions
                # clicks_total[word] += clicks  # Update clicks_total
                # conversions_total[word] += conversions  # Update conversions_total
                # spend_total[word] += spend  # Update spend_total
    return word_frequency, impressions_total

def write_word_frequency(word_frequency, impressions_total, output_file):
    """Write word-frequency pairs and total metrics to an output CSV file."""
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Frequency", "Total Impressions"])
        for word, frequency in sorted_word_frequency:
            total_impressions = impressions_total[word]
            # total_clicks = clicks_total[word]
            # total_conversions = round(conversions_total[word])  # Round to the nearest whole number
            # total_spend = spend_total[word]
            # total_cost_per_click = round(total_spend / total_clicks, 2) if total_clicks > 0 else 0
            # total_cost_per_conversion = round(total_spend / total_conversions, 2) if total_conversions > 0 else 0
            # total_conversion_rate = round(total_conversions / total_clicks, 2) if total_clicks > 0 else 0
            # total_click_thru_rate = round(total_clicks / total_impressions, 2) if total_impressions > 0 else 0
            writer.writerow([word, frequency, total_impressions])

if __name__ == "__main__":
    query_file = "c:/MyPrograms/workstation/GoogleAdsSearchReportsHrly/keywordplanner\outputnvda_kwplanner_tickers.csv" #"data/stock picks-KeywordStats2024-04-11at08_49_40-download.csv"  # data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped_metrics.csv # Path to the CSV file containing search queries and metrics
    output_file = "data/search_query_word_frequency_kwplanner_nvda.csv"  # "data/search_query_word_frequency.csv" # Output CSV file
    word_frequency, impressions_total = count_word_frequency(query_file)
    write_word_frequency(word_frequency, impressions_total, output_file)