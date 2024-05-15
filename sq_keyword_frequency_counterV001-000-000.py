# Below is a Python script that reads a search query CSV file, counts the frequency of each word, and then writes the word-frequency pairs to an output CSV file:
# file name: sq_keyword_frequency_counter.py

import csv
from collections import Counter

def count_word_frequency(query_file):
    """Count the frequency of each word in the search query file."""
    word_frequency = Counter()
    with open(query_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            query = row[0].strip()  # Assuming search queries are in the first column
            words = query.split()
            word_frequency.update(words)
    return word_frequency

def write_word_frequency(word_frequency, output_file):
    """Write word-frequency pairs to an output CSV file."""
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Frequency"])
        for word, frequency in sorted_word_frequency:
            writer.writerow([word, frequency])

if __name__ == "__main__":
    query_file = 'data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped.csv' # "search_queries.csv"  # Path to the CSV file containing search queries
    output_file = 'data/search_query_word_frequency.csv' # "word_frequency.csv"  # Output CSV file
    word_frequency = count_word_frequency(query_file)
    write_word_frequency(word_frequency, output_file)
