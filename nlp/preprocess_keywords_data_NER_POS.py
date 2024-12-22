# preprocess_keywords_data_NER_POS.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download the Transformer-based English model if not already installed
try:
    nlp = spacy.load("en_core_web_trf")
except OSError:
    print("Downloading the 'en_core_web_trf' model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_trf"])
    nlp = spacy.load("en_core_web_trf")

# Now you can use 'nlp' for further processing


# Sample dataset of keywords and categories
data = pd.read_csv(r'C:\\MyPrograms\\workstation\\SearchQueryCategorizer\\data\\keyword_data_training-v2.csv')

# Preprocessing
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load spaCy model with financial NER capabilities
nlp = spacy.load("en_core_web_trf")

def preprocess_text(text):
    # Tokenize text
    words = word_tokenize(text.lower())
    
    # Remove stop words and non-alphanumeric characters
    filtered_words = [word for word in words if word not in stop_words and word.isalnum()]

    # Lemmatize words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # Extract POS tags
    pos_tags = [pos[1] for pos in nltk.pos_tag(lemmatized_words)]

    # Extract Named Entities using spaCy
    doc = nlp(text)
    named_entities = [ent.label_ for ent in doc.ents]

    # Combine POS tags and Named Entities
    features = lemmatized_words + pos_tags + named_entities
    
    #check the data
    print(text,named_entities)

    return ' '.join(features)

data['clean_text'] = data['keyword'].apply(preprocess_text)

# Train-test split
# X_train, X_test, y_train, y_test = train_test_split(data['clean_text'], data['category'], test_size=0.2, random_state=42)

# # Model training
# pipeline = Pipeline([
#     ('tfidf', TfidfVectorizer()),
#     ('clf', MultinomialNB())
# ])

# pipeline.fit(X_train, y_train)

# # Evaluation
# y_pred = pipeline.predict(X_test)
# print(classification_report(y_test, y_pred))

# # Save the trained model for future use
# import joblib
# joblib.dump(pipeline, 'keyword_classifier_model.pkl')
