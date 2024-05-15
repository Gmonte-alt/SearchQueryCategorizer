import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Sample dataset of keywords and categories
data = pd.read_csv(r'C:\\MyPrograms\\workstation\\SearchQueryCategorizer\\data\\keyword_data_training.csv')

# Concatenate two category columns into one
data['combined_category'] = data['category1'] + ' ' + data['category2']

# Preprocessing
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stop_words and word.isalnum()]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    return ' '.join(lemmatized_words)

data['clean_text'] = data['keyword'].apply(preprocess_text)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(data['clean_text'], data['combined_category'], test_size=0.2, random_state=42)

# Model training
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

pipeline.fit(X_train, y_train)

# Evaluation
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model for future use
import joblib
joblib.dump(pipeline, 'keyword_classifier_model.pkl')
