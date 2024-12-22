# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-005
# Note: debugs the original v000-000-004 script

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize the lemmatizer and spell checker
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()

# Sample search queries
queries = [
    "travel nurse housing", "traveling nurse housing", "traveling nurses housing",
    "travel nurses housing", "travel nursing housing", "travelling nurse housing",
    "housing for travel nurses", "travelling nurses housing", "travel nurse housing san diego"
]

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
    return word

# Data Preprocessing with spell checking, UK to US correction, custom normalization, and lemmatization
def preprocess(query):
    corrected_query = [spell.correction(word) for word in query.lower().split()]
    us_corrected_query = [uk_to_us_correction(word) for word in corrected_query]
    normalized_query = [custom_normalization(word) for word in us_corrected_query]
    lemmatized_query = [lemmatizer.lemmatize(word) for word in normalized_query]
    return ' '.join(lemmatized_query)

preprocessed_queries = [preprocess(query) for query in queries]

# Create a mapping from preprocessed queries to original queries
preprocessed_to_original = {preprocessed: original for original, preprocessed in zip(queries, preprocessed_queries)}

# Print the preprocessed queries for debugging
print("Preprocessed Queries:")
for original, preprocessed in zip(queries, preprocessed_queries):
    print(f"Original: {original} -> Preprocessed: {preprocessed}")
print("Preprocessed Queries", preprocessed_queries)


# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(preprocessed_queries)
print(tfidf_matrix)

# Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Lowered threshold for similarity
threshold = 0.0

# Identify similar queries
similar_queries = {}
for i in range(len(preprocessed_queries)):
    for j in range(i + 1, len(preprocessed_queries)):
        print(i,j," Cosine: ", cosine_sim[i, j])
        # Check if cosine similarity score is greater than the threshold
        if cosine_sim[i, j] > threshold:
            # Add j-th query to the list of similar queries for i-th query
            similar_queries.setdefault(preprocessed_queries[i], set()).add(preprocessed_queries[j])
            print(similar_queries)
            similar_queries.setdefault(preprocessed_queries[j], set()).add(preprocessed_queries[i])
            print(similar_queries)

# Debugging: Print cosine similarity matrix
print("Cosine Similarity Matrix:")
print(cosine_sim)

# Debugging: Print all similarity scores
print("\nAll Similarity Scores:")
for i in range(len(preprocessed_queries)):
    for j in range(i + 1, len(preprocessed_queries)):
        print(f"Similarity between '{preprocessed_queries[i]}' and '{preprocessed_queries[j]}': {cosine_sim[i, j]}")

print("\nSimilar Queries")
for key, value in similar_queries.items():
    #print("key: ",key," value: ",value)
    # Retrieve the original query for the key and each similar query
    original_key = preprocessed_to_original[key]
    original_values = [preprocessed_to_original[v] for v in value]
    print(f"Original: {original_key} -> {key}: {list(original_values)}")