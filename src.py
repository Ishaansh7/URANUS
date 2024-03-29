# %%
import faiss
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

# %%
metadata = pd.read_csv('sent_news.csv', nrows = 30000).dropna()

# %%
def map_sentiment(score):
    if score > 0.3:
        return 'positive'
    elif 0.3 <= score <= -0.3:
        return 'neutral'
    else:
        return 'negative'

# Apply the function to create a new column with sentiment labels
metadata['sentiment_label'] = metadata['sentiment_score'].apply(map_sentiment)


# %%
metadata.sample(5)

# %%
# Preprocess the text data
metadata['text'] = metadata['headline'] + " " + metadata['abstract']
metadata['text'] = metadata['text'].apply(lambda x: x.lower())
metadata['text'] = metadata['text'].apply(lambda x: re.sub(r'\W+', ' ', x))

# %%
# Initialize the HashingVectorizer
vectorizer = HashingVectorizer(n_features=1000, binary=True)

# %%
# Generate the matrix of hashed features
tfidf_matrix = vectorizer.fit_transform(metadata['text'])

# %%
# Create a FAISS index
d = tfidf_matrix.shape[1]
index = faiss.IndexFlatL2(d)

# %%
# Add the vectors to the index
index.add(tfidf_matrix.toarray())


# %%
metadata

# %%
# def get_recommendations(query, vectorizer, index, metadata, k=10):
#     # Transform the query into a vector
#     query_vector = vectorizer.transform([query])
    
#     def search(index, query_vector, k=10):
#         D, I = index.search(query_vector, k)
#         return I[0]

#     # Use the index to find similar items
#     neighbor_indices = search(index, query_vector.toarray(), k)
    
#     # Fetch sentiment scores corresponding to recommended headlines
#     recommendations = []
#     for idx in neighbor_indices:
#         headline = metadata.iloc[idx]['headline']
#         sentiment_score = metadata.iloc[idx]['sentiment_score']
#         sentiment_label = metadata.iloc[idx]['sentiment_label']# Assuming you have a 'sentiment_score' column in your metadata
#         recommendations.append((headline, sentiment_score, sentiment_label))
    
#     return recommendations

# # Example usage
# x = input("Search: ")
# query = x
# recommendations = get_recommendations(query, vectorizer, index, metadata)
# print("Recommendations for:", query)
# for headline, sentiment_score, sentiment_label in recommendations:
#     print("Headline:", headline, "| Sentiment Score:", sentiment_score, "| Sentiment", sentiment_label)


# %%
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
        recommendations.append([headline, sentiment_score, sentiment_label])
    
    # Create a DataFrame from the recommendations
    recommendations_df = pd.DataFrame(recommendations, columns=['Headline', 'Sentiment Score', 'Sentiment Label'])
    
    return recommendations_df.to_string(index=False)

# Example usage
x = input("Search: ")
query = x
recommendations_df = get_recommendations(query, vectorizer, index, metadata)
print("Recommendations for:", query)
print(recommendations_df)

# %%



