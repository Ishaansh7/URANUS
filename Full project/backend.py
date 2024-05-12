import pandas as pd
import requests
import faiss
import re
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

NEWS_API_KEY = 'd6c7f3bd5dea44c2bcca2879c219183b'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

def fetch_news_for_title(query, num_articles=100):
    params = {
        'q': query,
        'language': 'en',
        'apiKey': NEWS_API_KEY,
        'pageSize': num_articles
    }
    response = requests.get(NEWS_API_ENDPOINT, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        
        # Create a DataFrame to store the news data
        df = pd.DataFrame(articles)
        
        return df
    else:
        print("Failed to fetch news:", response.status_code)
        return None

def get_news_recommendations(query):
    # Fetch news articles for the given search query
    news_df = fetch_news_for_title(query)
    
    if news_df is None:
        return None
    
    news_df.rename(columns={'title': 'headline', 'description': 'abstract'}, inplace=True) 
    metadata = news_df.copy()
    metadata['text'] = metadata['headline'].fillna('') + " " + metadata['abstract'].fillna('')
    metadata['text'] = metadata['text'].apply(lambda x: str(x).lower())
    metadata['text'] = metadata['text'].apply(lambda x: re.sub(r'\W+', ' ', x))

    vectorizer = HashingVectorizer(n_features=1000, binary=True)
    tfidf_matrix = vectorizer.fit_transform(metadata['text'])

    d = tfidf_matrix.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(tfidf_matrix.toarray())

    def search(index, query_vector, k=10):
        D, I = index.search(query_vector, k)
        return I[0]

    query_vector = vectorizer.transform([query])
    neighbor_indices = search(index, query_vector.toarray(), k=10)
    recommendations = []
    for idx in neighbor_indices:
        headline = metadata.iloc[idx]['headline']
        url = metadata.iloc[idx]['url']
        text = metadata.iloc[idx]['text']
        abstract = metadata.iloc[idx]['abstract']
        source = metadata.iloc[idx]['source']
        author = metadata.iloc[idx]['author']
        content = metadata.iloc[idx]['content']
        urlToImage = metadata.iloc[idx]['urlToImage']
        recommendations.append({
            'headline': headline,
            'url': url,
            'abstract': abstract,
            'text': text,
            'author': author,
            'source': source,
            'content': content,
            'urlToImage': urlToImage
        })
    
    return recommendations

if __name__ == "__main__":
    query = input("What are you looking for?\n")
    recommendations = get_news_recommendations(query)
    if recommendations is not None:
        print("Recommendations for:", query)
        print(recommendations)
        recommended_news = recommend_news(recommendations)
        print("Recommended news:")
        print(recommended_news)

def analyze_sentiment(df):
    sid = SentimentIntensityAnalyzer()
    nan_indices = df['text'].isna()
    df.loc[nan_indices, 'text'] = ''
    df['sentiment_score'] = df['text'].apply(lambda x: sid.polarity_scores(x)['compound'])

def map_sentiment(score):
    if score > 0.3:
        return 'positive'
    elif 0.3 >= score >= -0.3:
        return 'neutral'
    else:
        return 'negative'

def recommend_news(df, threshold=0.1):
    analyze_sentiment(df)
    df['sentiment_label'] = df['sentiment_score'].apply(map_sentiment)
    return df[df['sentiment_score'] >= threshold]

if __name__ == "__main__":
    query = input("What are you looking for?\n")
    recommendations = get_news_recommendations(query)
    if recommendations is not None:
        print("Recommendations for:", query)
        print(recommendations)
        recommended_news = recommend_news(recommendations)
        print("Recommended news:")
        print(recommended_news)