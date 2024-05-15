# file name: search_query_word_split_metrics_propn_kwplanner_stockpicksV000-000-000.py
# version: V000-000-0001

import csv
import spacy
from collections import defaultdict

# List of words to exclude from being identified as proper nouns
EXCLUDE_WORDS = {'stock', 'picks', 'top', 'hedge', 'fund', 'tech', 'monday', 'budget', 'ev', 'energy', 'dividend', 'high', 'march', 'microcap'}

def extract_proper_nouns(search_query):
    """Extract proper nouns from the search query."""
    proper_nouns = []
    doc = nlp(search_query)
    for token in doc:
        if token.pos_ == 'PROPN' and token.text.lower() not in EXCLUDE_WORDS:  # Check if the token is a proper noun and not in exclude list
            proper_nouns.append(token.text)
        elif token.text.lower() == 'fool':  # Treat 'fool' as a proper noun
            proper_nouns.append(token.text)
    return proper_nouns

def process_csv(input_file, output_file):
    # Open input CSV file for reading
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ['Search Query', 'Total Impressions', 'Proper Nouns', 'Proper Nouns Impressions', 'Other Impressions']
        
        # Open output CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()  # Write header row
            
            # Process each row in the input CSV file
            for row in reader:
                search_query = row['Search Query']
                impressions = row['Total Impressions'].split(',')
                
                # Extract proper nouns from the search query
                proper_nouns = extract_proper_nouns(search_query)
                
                # Initialize dictionaries to store impressions for proper nouns and other words
                proper_nouns_impressions = defaultdict(list)
                other_impressions = []
                
                # Iterate through each word in the search query
                for word, impression in zip(search_query.split(), impressions):
                    # Check if the word is a proper noun
                    if word in proper_nouns:
                        proper_nouns_impressions[word].append(impression.strip())
                    else:
                        other_impressions.append(impression.strip())
                
                # Write row to output CSV file
                writer.writerow({
                    'Search Query': search_query,
                    'Total Impressions': ', '.join(impressions),
                    'Proper Nouns': ', '.join(proper_nouns),
                    'Proper Nouns Impressions': ', '.join([', '.join(v) for v in proper_nouns_impressions.values()]),
                    'Other Impressions': ', '.join(other_impressions)
                })

# Load the spaCy English language model
nlp = spacy.load('en_core_web_sm')

# Example usage
process_csv('data/search_query_word_split_metrics_kwplanner_stockpicks.csv', 'data/search_query_word_split_propn_kwplanner_stockpicks.csv')
# sum_total_impressions('data/search_query_word_split_metrics_kwplanner_stockpicks.csv', 'data/search_query_total_sum_word_split_kwplanner_stockpicks.csv')