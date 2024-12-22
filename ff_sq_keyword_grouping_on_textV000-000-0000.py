# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-004

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Saple search queries
queries = [
    "travel nurse housing", "traveling nurse housing", "traveling nurses housing",
    "travel nurses housing", "travel nursing housing", "travelling nurse housing",
    "housing for travel nurses", "travelling nurses housing"
]

# Data Preprocessing (simple example)
queries = [query.lower() for query in queries]

# TF-IDF Vectorition
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(queries)

# Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Threshold for similarity
threshold = 0.8

# Identify similar queries
similar_queries = {}
for i in range(len(queries)):
    for j in range(i+1, len(queries)):
        if cosine_sim[i, j] > threshold:
            similar_queries.setdefault(queries[i], []).append(queries[j])

print("Similar Queries")
for key, value in similar_queries.items():
    print(f"{key}: {value}")
