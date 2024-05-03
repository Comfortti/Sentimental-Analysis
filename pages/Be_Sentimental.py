# Import libraries
import re
import string
import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

# Disable SSL certificate verification in NLTK
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Load dataset
data = pd.read_csv(r"music_album_reviews.csv")

# Handle missing values - use average rating for Ratings, remove null reviews
data['Rating'].fillna(data['Rating'].mean(), inplace=True)
data.dropna(subset=['Review'], inplace=True)
data.drop_duplicates(inplace=True)

# Function to clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text) # Removes text enclosed in brackets
    text = re.sub('https?://\S+|www\.\S+', '', text) # Removes URLs from the text
    text = re.sub('<.*?>+', '', text) # Removes text enclosed in <>
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) # Removes all punctuation marks from the text
    text = re.sub('\n', '', text) # Removes newline characters from the text
    text = re.sub('\w*\d\w*', '', text) # Removes words with numbers
    return text

# Function to preprocess text
def preprocess_text(text):
    # Remove words with numbers
    text = re.sub('\w*\d\w*', '', text)
    # Remove words with length less than or equal to 2
    text = ' '.join(word for word in text.split() if len(word) > 2)
    return text

# Clean and preprocess the text
data['clean_text'] = data['Review'].apply(clean_text)
data['final_text'] = data['clean_text'].apply(preprocess_text)

# Function to derive sentiment using TextBlob
def get_textblob_sentiment(text):
    testimonial = TextBlob(text)
    return "Positive" if testimonial.sentiment.polarity > 0 else "Negative"

# Train TF-IDF model
tfidf = TfidfVectorizer(lowercase=False)
X = tfidf.fit_transform(data['final_text'])
y_tb = data['final_text'].apply(get_textblob_sentiment)

# Streamlit app
def main():
    st.title("Analyse Your Album Reviews!")

    user_input = st.text_area("Enter your album review here for a sentiment analysis:")

    if st.button("Analyse"):
        cleaned_input = clean_text(user_input)
        preprocessed_input = preprocess_text(cleaned_input)
        sentiment = get_textblob_sentiment(preprocessed_input)
        st.write(f"Analysis: {sentiment} comment")

if __name__ == "__main__":
    main()