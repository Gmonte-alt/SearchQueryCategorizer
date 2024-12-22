# file name: output/sq_frequency_top-5-words.py
# version: V000-000-004
# Note: Loops through all five cooccurrences sorts descending on ff_purchases
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

def get_top_combinations(word_to_search_terms, top_cooccurring_words, level):
    """Get the top co-occurring combinations for each word based on ff_purchases."""
    top_combinations = defaultdict(list)
    seen_combinations = set()

    for word, top_words in top_cooccurring_words.items():
        combinations_to_check = [tuple(sorted([co_word for co_word, _ in top_words[:i]])) for i in range(level, 1, -1)]
        for combination in combinations_to_check:
            if len(combination) == level and combination not in seen_combinations:
                seen_combinations.add(combination)
                total_ff_purchases = 0
                for words_in_search_term, ff_purchases in word_to_search_terms[word]:
                    if all(w in words_in_search_term for w in combination):
                        total_ff_purchases += ff_purchases
                if total_ff_purchases > 0:
                    top_combinations[word].append((combination, total_ff_purchases))

    return top_combinations

def flatten_combinations(top_combinations, max_length=5):
    """Flatten the nested combination dictionary into a list of tuples."""
    flattened = []
    for word, combinations in top_combinations.items():
        for combination, ff_purchases in combinations:
            # Ensure the combination has the correct length
            padded_combination = list(combination) + [""] * (max_length - len(combination))
            flattened.append((word, *padded_combination, ff_purchases))
    return flattened

def write_top_combinations(output_file, top_combinations):
    """Write the top combinations and their associated ff_purchases values to an output file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Co-occurring Word 1", "Co-occurring Word 2", "Co-occurring Word 3", "Co-occurring Word 4", "Total ff_purchases"])
        for row in top_combinations:
            writer.writerow([*row[:6], round(row[6], 2)])

if __name__ == "__main__":
    word_frequency_file = "output/search_query_word_frequency.csv"  # Path to the first CSV file
    search_term_file = "output/FINAL_merged_output.csv"  # Path to the second CSV file
    output_file = "output/top_combinations_by_purchases.csv"  # Output CSV file

    # Read the CSV files
    word_data = read_csv_file(word_frequency_file)
    search_term_data = read_csv_file(search_term_file)

    # Build the word to search terms map
    word_to_search_terms = build_word_to_search_terms_map(search_term_data)

    # Get the top 5 co-occurring words for each word based on ff_purchases
    top_cooccurring_words = get_top_cooccurring_words(word_to_search_terms, top_n=5)

    # Get the top combinations for different levels of co-occurring words
    all_combinations = []
    for level in range(5, 1, -1):  # Levels 5, 4, 3, 2
        top_combinations = get_top_combinations(word_to_search_terms, top_cooccurring_words, level)
        flattened_combinations = flatten_combinations(top_combinations)
        all_combinations.extend(flattened_combinations)

    # Sort all combinations by total ff_purchases in descending order
    sorted_combinations = sorted(all_combinations, key=lambda x: x[-1], reverse=True)

    # Write the top combinations to the output file
    write_top_combinations(output_file, sorted_combinations)

    print(f"Top combinations by purchases have been saved to {output_file}")


