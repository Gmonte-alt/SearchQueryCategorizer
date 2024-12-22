# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-002
# Note: incorporates NLTK lemmatization to convert words to their base or root form to improve similarity detection

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Sample search queries
queries = [
    "travel nurse housing", "traveling nurse housing", "traveling nurses housing",
    "travel nurses housing", "travel nursing housing", "travelling nurse housing",
    "housing for travel nurses", "travelling nurses housing"
]

# Data Preprocessing with lemmatization
queries = [' '.join([lemmatizer.lemmatize(word) for word in query.lower().split()]) for query in queries]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(queries)

# Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Lowered threshold for similarity
threshold = 0.6

# Identify similar queries
similar_queries = {}
for i in range(len(queries)):
    for j in range(i + 1, len(queries)):
        if cosine_sim[i, j] > threshold:
            similar_queries.setdefault(queries[i], []).append(queries[j])

# Debugging: Print cosine similarity matrix
print("Cosine Similarity Matrix:")
print(cosine_sim)

# Debugging: Print all similarity scores
print("\nAll Similarity Scores:")
for i in range(len(queries)):
    for j in range(i + 1, len(queries)):
        print(f"Similarity between '{queries[i]}' and '{queries[j]}': {cosine_sim[i, j]}")

print("\nSimilar Queries")
for key, value in similar_queries.items():
    print(f"{key}: {value}")
