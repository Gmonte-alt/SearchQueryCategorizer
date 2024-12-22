# file name: ff_sq_keyword_grouping_on_text.py
# Version: V000-000-006
# Note: removed the tf-idf vectorizer & cosine calculation in place for a batch processor

import nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd

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
output_file = 'output/FINAL_merged_output_normalized.csv'

# Read the CSV file in chunks
chunk_size = 1000  # Adjust chunk size as needed
chunks = pd.read_csv(input_file, chunksize=chunk_size)

# Process each chunk and append to the output file
for i, chunk in enumerate(chunks):
    chunk['search_term_normalized'] = chunk['Search term'].apply(preprocess)
    if i == 0:
        chunk.to_csv(output_file, index=False)
    else:
        chunk.to_csv(output_file, mode='a', header=False, index=False)

print(f"Output saved to {output_file}")
