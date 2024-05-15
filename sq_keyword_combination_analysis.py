# sq_keyword_combination_analysis.py
# Output file: data/output_word_metrics.csv
import csv
from collections import defaultdict

def process_csv(input_file):
    """Process the CSV file and calculate word frequencies."""
    word_frequency = defaultdict(int)  # Initialize defaultdict to store word frequencies
    word_impressions = defaultdict(int)  # Initialize defaultdict to store word impressions
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = row['Search_term'].strip()  # Assuming search queries are in the 'Search_term' column
            impressions = int(row['Impressions'])  # Assuming impressions are in the 'Impressions' column

            # Split the query into words based on spaces
            words = query.split()
            # Update word frequency for each word in the query
            for word in words:
                word_frequency[word] += 1
            # Update word impressions for each word in the query
            for word in set(words):
                word_impressions[word] += impressions

            # Update word frequency for word combinations
            for i in range(len(words)):
                for j in range(i + 1, len(words)):
                    # Combine words into a unique key
                    word_combination = ' '.join(sorted([words[i], words[j]]))
                    word_frequency[word_combination] += 1

    return word_frequency, word_impressions

def write_word_metrics(word_frequency, word_impressions, output_file):
    """Write word metrics to an output CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Frequency", "Impressions"])
        for word, frequency in word_frequency.items():
            writer.writerow([word, frequency, word_impressions[word]])

if __name__ == "__main__":
    input_file = "data/2023-2024ConvertingSearchTermsReport-SearchTerm_dedupped_metrics.csv"  # Input CSV file containing search query data and performance metrics
    output_file = "data/output_word_metrics.csv"  # Output CSV file
    word_frequency, word_impressions = process_csv(input_file)
    write_word_metrics(word_frequency, word_impressions, output_file)
