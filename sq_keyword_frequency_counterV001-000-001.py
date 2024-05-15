# Below is a Python script that reads a search query CSV file, counts the frequency of each word, and then writes the word-frequency pairs to an output CSV file:
# file name: sq_keyword_frequency_counter.py

import csv
from collections import Counter

def count_word_frequency(query_file):
    """Count the frequency of each word and the total impressions in the search query file."""
    word_frequency = Counter()
    impressions_total = Counter()
    with open(query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            query = row[0].strip()  # Assuming search queries are in the first column
            impressions = int(row[1])  # Assuming impressions are in the second column
            words = query.split()
            word_frequency.update(words)
            for word in set(words):
                impressions_total[word] += impressions
    return word_frequency, impressions_total

def write_word_frequency(word_frequency, impressions_total, output_file):
    """Write word-frequency pairs and total impressions to an output CSV file."""
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Frequency", "Total Impressions"])
        for word, frequency in sorted_word_frequency:
            total_impressions = impressions_total[word]
            writer.writerow([word, frequency, total_impressions])

if __name__ == "__main__":
    query_file = "data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped_metrics.csv"  # Path to the CSV file containing search queries and impressions
    output_file = "data/search_query_word_frequency.csv"  # Output CSV file
    word_frequency, impressions_total = count_word_frequency(query_file)
    write_word_frequency(word_frequency, impressions_total, output_file)