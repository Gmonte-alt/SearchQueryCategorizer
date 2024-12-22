# file name: output/sq_frequency_top-5-words.py
# version: V000-000-002
# Note: Adds a third element to the script
#

import csv
from collections import defaultdict, Counter

def read_csv_file(file_path):
    """Read a CSV file and return a list of rows as dictionaries."""
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def aggregate_ff_purchases(word_data, search_term_data):
    """Aggregate ff_purchases for each word and its co-occurring words."""
    word_ff_purchases = defaultdict(Counter)

    # Create a map of words to their search terms
    word_to_search_terms = defaultdict(list)
    for row in word_data:
        word = row['Word']
        word_to_search_terms[word].append(row)

    # Process search terms and aggregate ff_purchases
    for row in search_term_data:
        search_term = row['Search term']
        ff_purchases = float(row['ff_purchases'])
        if ff_purchases > 0:  # Only consider search terms with non-zero ff_purchases
            words_in_search_term = search_term.split()
            for word in words_in_search_term:
                if word in word_to_search_terms:
                    for other_word in words_in_search_term:
                        if other_word != word:
                            word_ff_purchases[word][other_word] += ff_purchases

    return word_ff_purchases

def get_top_cooccurring_words(word_ff_purchases, top_n=5):
    """Get the top N co-occurring words for each word based on ff_purchases."""
    top_cooccurring_words = {}

    for word, cooccurring_words in word_ff_purchases.items():
        top_words = cooccurring_words.most_common(top_n)
        top_cooccurring_words[word] = top_words

    return top_cooccurring_words

def get_top_triplets(word_ff_purchases, top_cooccurring_words, top_n=1):
    """Get the top co-occurring triplets for each word based on ff_purchases."""
    top_triplets = defaultdict(list)

    for word, top_words in top_cooccurring_words.items():
        for co_word, _ in top_words:
            third_level_words = word_ff_purchases[co_word].most_common(top_n)
            for third_word, _ in third_level_words:
                if third_word != word:
                    fourth_level_words = word_ff_purchases[third_word].most_common(top_n)
                    for fourth_word, ff_purchases in fourth_level_words:
                        if fourth_word != co_word and fourth_word != word:
                            top_triplets[word].append((co_word, third_word, fourth_word, ff_purchases))

    return top_triplets

def write_top_triplets(output_file, top_triplets):
    """Write the top triplets and their associated ff_purchases values to an output file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Co-occurring Word 1", "Co-occurring Word 2", "Co-occurring Word 3", "Total ff_purchases"])
        for word, triplets in top_triplets.items():
            for co_word, third_word, fourth_word, ff_purchases in triplets:
                writer.writerow([word, co_word, third_word, fourth_word, round(ff_purchases, 2)])

if __name__ == "__main__":
    word_frequency_file = "output/search_query_word_frequency.csv"  # Path to the first CSV file
    search_term_file = "output/FINAL_merged_output.csv"  # Path to the second CSV file
    output_file = "output/top_quadruplets_by_purchases.csv"  # Output CSV file

    # Read the CSV files
    word_data = read_csv_file(word_frequency_file)
    search_term_data = read_csv_file(search_term_file)

    # Aggregate ff_purchases for each word and its co-occurring words
    word_ff_purchases = aggregate_ff_purchases(word_data, search_term_data)

    # Get the top 5 co-occurring words for each word based on ff_purchases
    top_cooccurring_words = get_top_cooccurring_words(word_ff_purchases, top_n=5)

    # Get the top quadruplets based on ff_purchases
    top_quadruplets = get_top_triplets(word_ff_purchases, top_cooccurring_words, top_n=1)

    # Write the top quadruplets to the output file
    write_top_triplets(output_file, top_quadruplets)

    print(f"Top quadruplets by purchases have been saved to {output_file}")
