import streamlit as st
import numpy as np
import pandas as pd
import faiss
import src
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

# Load the metadata and index from the source file
metadata = pd.read_csv('sentinlinks.csv', nrows = 30000).dropna()

def map_sentiment(score):
    if score > 0.3:
        return 'positive'
    elif 0.3 >= score >= -0.3:
        return 'neutral'
    else:
        return 'negative'

metadata['sentiment_label'] = metadata['sentiment_score'].apply(map_sentiment)

metadata['text'] = metadata['headline'] + " " + metadata['abstract']
metadata['text'] = metadata['text'].apply(lambda x: x.lower())
metadata['text'] = metadata['text'].apply(lambda x: re.sub(r'\W+', ' ', x))

vectorizer = HashingVectorizer(n_features=1000, binary=True)
tfidf_matrix = vectorizer.fit_transform(metadata['text'])
index = faiss.IndexFlatL2(tfidf_matrix.shape[1])
index.add(tfidf_matrix.toarray())

# Define the Streamlit app
def recommend_news(query):
    recommendations_df = get_recommendations(query, vectorizer, index, metadata)
    return recommendations_df

def get_recommendations(query, vectorizer, index, metadata, k=10):
    # Transform the query into a vector
    query_vector = vectorizer.transform([query])
    
    def search(index, query_vector, k=10):
        D, I = index.search(query_vector, k)
        return I[0]

    # Use the index to find similar items
    neighbor_indices = search(index, query_vector.toarray(), k)
    
    # Fetch sentiment scores and labels corresponding to recommended headlines
    recommendations = []
    for idx in neighbor_indices:
        headline = metadata.iloc[idx]['headline']
        sentiment_score = metadata.iloc[idx]['sentiment_score']
        sentiment_label = metadata.iloc[idx]['sentiment_label']
        links = metadata.iloc[idx]['links']
        recommendations.append([headline, sentiment_score, sentiment_label,links])
    
    # Create a Streamlit dataframe from the recommendations
    recommendations_df = pd.DataFrame(recommendations, columns=['Headline', 'Sentiment Score', 'Sentiment Label','Links'])
    st_df = st.dataframe(recommendations_df)
    
    return st_df
    
st.title("URANUS: News Recommendation System :fish:")
st.header("Enter a keyword:")
user_input = st.text_input("Search:")
if user_input:
    st_df = get_recommendations(user_input, vectorizer, index, metadata)
    st.write(st_df)
