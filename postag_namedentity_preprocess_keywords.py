import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

# Read keywords from CSV file
keywords_df = pd.read_csv(r'C:\\MyPrograms\\workstation\\SearchQueryCategorizer\\data\\keyword_data_training.csv')

# Extract keywords from DataFrame
keywords = keywords_df['keyword'].tolist()

# Tokenization and POS tagging
pos_tags = [pos_tag(word_tokenize(keyword)) for keyword in keywords]

# Named Entity Recognition (NER)
named_entities = [ne_chunk(pos_tag(word_tokenize(keyword))) for keyword in keywords]

# Display POS tags and Named Entities
for i, keyword in enumerate(keywords):
    print("Keyword:", keyword)
    print("POS Tags:", pos_tags[i])
    print("Named Entities:", named_entities[i])
    print()
