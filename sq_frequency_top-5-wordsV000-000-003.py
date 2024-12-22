# file name: output/sq_frequency_top-5-words.py
# version: V000-000-003
# Note: Adds a fifth element to the script and reaggregates at the end
#

import csv
from collections import defaultdict, Counter

def read_csv_file(file_path):
    """Read a CSV file and return a list of rows as dictionaries."""
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def build_word_to_search_terms_map(search_term_data):
    """Build a map from each word to the search terms they appear in and their associated ff_purchases."""
    word_to_search_terms = defaultdict(list)

    for row in search_term_data:
        search_term = row['Search term']
        ff_purchases = float(row['ff_purchases'])
        if ff_purchases > 0:  # Only consider search terms with non-zero ff_purchases
            words_in_search_term = set(search_term.split())
            for word in words_in_search_term:
                word_to_search_terms[word].append((words_in_search_term, ff_purchases))

    return word_to_search_terms

def get_top_cooccurring_words(word_to_search_terms, top_n=5):
    """Get the top N co-occurring words for each word based on ff_purchases."""
    top_cooccurring_words = {}

    for word, search_terms in word_to_search_terms.items():
        cooccurring_word_counter = Counter()
        for words_in_search_term, ff_purchases in search_terms:
            for other_word in words_in_search_term:
                if other_word != word:
                    cooccurring_word_counter[other_word] += ff_purchases
        top_words = cooccurring_word_counter.most_common(top_n)
        top_cooccurring_words[word] = top_words

    return top_cooccurring_words

def get_top_quintuplets(word_to_search_terms, top_cooccurring_words, top_n=1):
    """Get the top co-occurring quintuplets for each word based on ff_purchases."""
    top_quintuplets = defaultdict(list)

    for word, top_words in top_cooccurring_words.items():
        for co_word, _ in top_words:
            third_level_words = top_cooccurring_words.get(co_word, [])
            for third_word, _ in third_level_words:
                if third_word != word:
                    fourth_level_words = top_cooccurring_words.get(third_word, [])
                    for fourth_word, _ in fourth_level_words:
                        if fourth_word != co_word and fourth_word != word:
                            fifth_level_words = top_cooccurring_words.get(fourth_word, [])
                            for fifth_word, _ in fifth_level_words:
                                if fifth_word != third_word and fifth_word != co_word and fifth_word != word:
                                    # Reaggregate ff_purchases
                                    total_ff_purchases = 0
                                    for words_in_search_term, ff_purchases in word_to_search_terms[word]:
                                        if all(w in words_in_search_term for w in [co_word, third_word, fourth_word, fifth_word]):
                                            total_ff_purchases += ff_purchases
                                    if total_ff_purchases > 0:
                                        top_quintuplets[word].append((co_word, third_word, fourth_word, fifth_word, total_ff_purchases))

    return top_quintuplets

def write_top_quintuplets(output_file, top_quintuplets):
    """Write the top quintuplets and their associated ff_purchases values to an output file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Co-occurring Word 1", "Co-occurring Word 2", "Co-occurring Word 3", "Co-occurring Word 4", "Total ff_purchases"])
        for word, quintuplets in top_quintuplets.items():
            for co_word, third_word, fourth_word, fifth_word, ff_purchases in quintuplets:
                writer.writerow([word, co_word, third_word, fourth_word, fifth_word, round(ff_purchases, 2)])

if __name__ == "__main__":
    word_frequency_file = "output/search_query_word_frequency.csv"  # Path to the first CSV file
    search_term_file = "output/FINAL_merged_output.csv"  # Path to the second CSV file
    output_file = "output/top_quintuplets_by_purchases.csv"  # Output CSV file

    # Read the CSV files
    word_data = read_csv_file(word_frequency_file)
    search_term_data = read_csv_file(search_term_file)

    # Build the word to search terms map
    word_to_search_terms = build_word_to_search_terms_map(search_term_data)

    # Get the top 5 co-occurring words for each word based on ff_purchases
    top_cooccurring_words = get_top_cooccurring_words(word_to_search_terms, top_n=5)

    # Get the top quintuplets based on reaggregated ff_purchases
    top_quintuplets = get_top_quintuplets(word_to_search_terms, top_cooccurring_words, top_n=1)

    # Write the top quintuplets to the output file
    write_top_quintuplets(output_file, top_quintuplets)

    print(f"Top quintuplets by purchases have been saved to {output_file}")
