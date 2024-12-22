# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-007
# Note: re-introducing the tf-idf vectorizer and faise nearest neighbor for the search-term-final classification

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import faiss

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

# Data Preprocessing with UK to US correction, custom normalization, and lemmatization
def preprocess(query):
    corrected_query = query.lower().split()
    us_corrected_query = [uk_to_us_correction(word) for word in corrected_query]
    normalized_query = [custom_normalization(word) for word in us_corrected_query]
    lemmatized_query = [lemmatizer.lemmatize(word) for word in normalized_query if word]
    return ' '.join([word for word in lemmatized_query if word])

# Load the CSV file
input_file = 'output/FINAL_merged_output.csv'
output_file = 'output/FINAL_merged_output_normalized_with_similarity.csv'

# Read the CSV file in chunks
chunk_size = 1000  # Adjust chunk size as needed
chunks = pd.read_csv(input_file, chunksize=chunk_size)

# Initialize list to store preprocessed queries
all_preprocessed_queries = []
query_frequencies = {}

# Process each chunk
for i, chunk in enumerate(chunks):
    chunk['search_term_normalized'] = chunk['Search term'].apply(preprocess)
    for query in chunk['search_term_normalized'].tolist():
        all_preprocessed_queries.append(query)
        if query in query_frequencies:
            query_frequencies[query] += 1
        else:
            query_frequencies[query] = 1
    if i == 0:
        chunk.to_csv(output_file, index=False)
    else:
        chunk.to_csv(output_file, mode='a', header=False, index=False)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(all_preprocessed_queries)

# Convert TF-IDF matrix to a dense format for Faiss
tfidf_matrix_dense = tfidf_matrix.toarray().astype('float32')

# Create the index
index = faiss.IndexFlatL2(tfidf_matrix_dense.shape[1])  # L2 distance is equivalent to cosine similarity
index.add(tfidf_matrix_dense)

# Perform the search for the nearest neighbors
k = 5  # Number of nearest neighbors
D, I = index.search(tfidf_matrix_dense, k)

# Threshold for similarity (e.g., keep top k similar terms)
threshold = 0.2

# Identify similar queries
similar_queries = {}
similarity_scores = []

for i in range(len(all_preprocessed_queries)):
    for j in range(1, k):  # Skip the first neighbor as it is the query itself
        if D[i, j] < threshold:
            similar_queries.setdefault(all_preprocessed_queries[i], []).append(all_preprocessed_queries[I[i, j]])
            similarity_scores.append({
                'query_1': all_preprocessed_queries[i],
                'query_2': all_preprocessed_queries[I[i, j]],
                'similarity': 1 - D[i, j]  # Convert L2 distance to similarity
            })

# Create a mapping from similar queries to the most representative query
query_to_final = {}
for key, values in similar_queries.items():
    # Choose the most representative query based on frequency or other heuristic
    representative_query = max([key] + values, key=lambda x: query_frequencies.get(x, 0))
    for value in values:
        query_to_final[value] = representative_query
    query_to_final[key] = representative_query

# Apply the mapping to the original dataframe
def map_to_final(query):
    preprocessed_query = preprocess(query)
    return query_to_final.get(preprocessed_query, preprocessed_query)

# Read the CSV file again to apply the final mapping
chunks = pd.read_csv(input_file, chunksize=chunk_size)
for i, chunk in enumerate(chunks):
    chunk['search_term_final'] = chunk['Search term'].apply(map_to_final)
    if i == 0:
        chunk.to_csv(output_file, index=False)
    else:
        chunk.to_csv(output_file, mode='a', header=False, index=False)

# Create a DataFrame from similarity scores
similarity_df = pd.DataFrame(similarity_scores)

# Save similarity scores to a separate CSV file
similarity_output_file = 'output/FINAL_merged_similarity_scores.csv'
similarity_df.to_csv(similarity_output_file, index=False)

print(f"Output saved to {output_file}")
print(f"Similarity scores saved to {similarity_output_file}")
