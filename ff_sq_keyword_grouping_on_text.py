# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-008 data/location_property_city_state.csv
# Note: re-introducing the tf-idf vectorizer and faise nearest neighbor for the search-term-final classification

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import faiss
import re
import time
import ahocorasick

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Custom UK to US spelling correction
uk_to_us_dict = {
    "travelling": "traveling",
    "organisation": "organization",
    "colour": "color",
    # Add more as needed
}

def uk_to_us_correction(word):
    return uk_to_us_dict.get(word, word)

# Custom normalization to treat "travel" and "traveling" as the same
def custom_normalization(word):
    if word in ["travel", "traveling"]:
        return "travel"
    if word in ["nurse", "nursing"]:
        return "nurse"
    if word in ["website", "websites", "site", "sites"]:
        return "website"
    if word in ["rent", "renting"]:
        return "rent"
    if word in ["mid term", "midterm"]:
        return "mid term"
    return word

# Data Preprocessing with UK to US correction, custom normalization, lemmatization, and character cleaning
def preprocess(query):
    query = str(query)  # Ensure the query is a string
    query = re.sub(r'[^\w\s]', '', query)  # Remove non-alphanumeric characters
    corrected_query = query.lower().split()
    us_corrected_query = [uk_to_us_correction(word) for word in corrected_query]
    normalized_query = [custom_normalization(word) for word in us_corrected_query]
    lemmatized_query = [lemmatizer.lemmatize(word) for word in normalized_query if word]
    return ' '.join([word for word in lemmatized_query if word])

# Function to build Aho-Corasick automaton for city names
def build_automaton(cities):
    automaton = ahocorasick.Automaton()
    for city in cities:
        automaton.add_word(city, city)
    automaton.make_automaton()
    return automaton

# Function to check if the search term contains any full city name using Aho-Corasick automaton and return the matched city
def contains_city(search_term, automaton):
    if not isinstance(search_term, str):
        return False, None  # Handle non-string values
    search_term_lower = ' ' + search_term.lower() + ' '  # Add leading and trailing spaces
    for end_index, city in automaton.iter(search_term_lower):
        if len(city) > 3:  # Ensure the city name has a minimum length
            # Check for word boundaries around the city name
            city_pattern = re.compile(r'\b' + re.escape(city) + r'\b')
            if city_pattern.search(search_term_lower):
                return True, city
    return False, None

# Function to clean city names
def clean_city_state(name):
    name = str(name).lower()  # Ensure the name is a string and convert to lowercase
    name = re.sub(r'[^\w\s]', '', name)  # Remove non-alphanumeric characters
    return name

# List of high-frequency non-city terms to filter out
non_city_terms = set([
    'housing', 'nurse', 'travel', 'furnished', 'apartments'
    # Add more as needed
])

# Enhanced function to check for city names with additional filtering and return the matched city
def contains_city_enhanced(search_term, automaton):
    if not isinstance(search_term, str):
        return False, None
    search_term_lower = ' ' + search_term.lower() + ' '  # Add leading and trailing spaces
    for end_index, city in automaton.iter(search_term_lower):
        if len(city) > 3 and city not in non_city_terms:  # Apply length and non-city term filter
            # Check for word boundaries around the city name
            city_pattern = re.compile(r'\b' + re.escape(city) + r'\b')
            if city_pattern.search(search_term_lower):
                return True, city
    return False, None

# Load the CSV files
input_file = 'output/FINAL_merged_output.csv'
location_file = 'data/location_property_city_state.csv'
output_file = 'output/FINAL_merged_output_normalized_with_similarity.csv'

# Read location data and clean it
location_data = pd.read_csv(location_file)
location_data['PROPERTY_CITY'] = location_data['PROPERTY_CITY'].apply(clean_city_state)

# Extract unique cities and build Aho-Corasick automaton
unique_cities = location_data['PROPERTY_CITY'].unique()
automaton = build_automaton(unique_cities)

# Read the CSV file in chunks
chunk_size = 1000  # Adjust chunk size as needed
chunks = pd.read_csv(input_file, chunksize=chunk_size)

# Initialize list to store preprocessed queries and processed chunks
all_preprocessed_queries = []
processed_chunks = []

# Process each chunk sequentially
start_time = time.time()
for chunk in chunks:
    chunk['search_term_normalized'] = chunk['Search term'].apply(preprocess)
    chunk['contains_city'], chunk['matched_city'] = zip(*chunk['Search term'].apply(lambda x: contains_city_enhanced(x, automaton)))
    processed_chunks.append(chunk)
    all_preprocessed_queries.extend(chunk['search_term_normalized'].tolist())

# Combine processed chunks into a single DataFrame
full_df = pd.concat(processed_chunks, ignore_index=True)

# Save the full DataFrame to the output file
full_df.to_csv(output_file, index=False)
print(f"Preprocessing completed in {time.time() - start_time:.2f} seconds.")

# TF-IDF Vectorization
start_time = time.time()
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(full_df['search_term_normalized'])
print(f"TF-IDF Vectorization completed in {time.time() - start_time:.2f} seconds.")

# Convert TF-IDF matrix to a dense format for Faiss
tfidf_matrix_dense = tfidf_matrix.toarray().astype('float32')

# Create the index
start_time = time.time()
index = faiss.IndexFlatL2(tfidf_matrix_dense.shape[1])  # L2 distance is equivalent to cosine similarity
index.add(tfidf_matrix_dense)
print(f"Faiss Index creation completed in {time.time() - start_time:.2f} seconds.")

# Perform the search for the nearest neighbors
start_time = time.time()
k = 5  # Number of nearest neighbors
D, I = index.search(tfidf_matrix_dense, k)
print(f"Nearest neighbors search completed in {time.time() - start_time:.2f} seconds.")

# Threshold for similarity (e.g., keep top k similar terms)
threshold = 0.2

# Identify similar queries
similar_queries = {}
similarity_scores = []

start_time = time.time()
for i in range(len(full_df)):
    for j in range(1, k):  # Skip the first neighbor as it is the query itself
        if D[i, j] < threshold:
            similar_queries.setdefault(full_df['search_term_normalized'][i], []).append(full_df['search_term_normalized'][I[i, j]])
            similarity_scores.append({
                'query_1': full_df['search_term_normalized'][i],
                'query_2': full_df['search_term_normalized'][I[i, j]],
                'similarity': 1 - D[i, j]  # Convert L2 distance to similarity
            })
print(f"Similarity identification completed in {time.time() - start_time:.2f} seconds.")

# Create a frequency dictionary for normalized search terms
frequency_dict = full_df['search_term_normalized'].value_counts().to_dict()

# Create a mapping from similar queries to the most representative query using the frequency dictionary
start_time = time.time()
query_to_final = {key: max([key] + values, key=lambda x: frequency_dict.get(x, 0)) for key, values in similar_queries.items()}
print(f"Mapping creation completed in {time.time() - start_time:.2f} seconds.")

# Apply the mapping to the original dataframe using vectorized operations
start_time = time.time()
full_df['search_term_final'] = full_df['search_term_normalized'].map(query_to_final).fillna(full_df['search_term_normalized'])
print(f"Final mapping and saving completed in {time.time() - start_time:.2f} seconds.")

# Save the full DataFrame with the search_term_final column to the output file
full_df.to_csv(output_file, index=False)

# Create a DataFrame from similarity scores
similarity_df = pd.DataFrame(similarity_scores)

# Save similarity scores to a separate CSV file
similarity_output_file = 'output/FINAL_merged_similarity_scores.csv'
similarity_df.to_csv(similarity_output_file, index=False)

print(f"Similarity scores saved to {similarity_output_file}")
print(f"Overall script completed in {time.time() - start_time:.2f} seconds.")
