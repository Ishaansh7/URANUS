# %%
import faiss
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

# %%
metadata = pd.read_csv('final_data.csv').dropna()

# %%
metadata.head()

# %%
metadata.info()

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
        links = metadata.iloc[idx]['links']
        sentiment_score = metadata.iloc[idx]['sentiment_score']
        sentiment_label = metadata.iloc[idx]['sentiment_label']
        recommendations.append([headline, sentiment_score, sentiment_label, links])
    
    # Create a DataFrame from the recommendations
    recommendations_df = pd.DataFrame(recommendations, columns=['Headline', 'Sentiment Score', 'Sentiment Label','Links'])
    
    return recommendations_df.to_string(index=False)


x = input("Search: ")
query = x
recommendations_df = get_recommendations(query, vectorizer, index, metadata)
print("Recommendations for:", query)
print(recommendations_df)


