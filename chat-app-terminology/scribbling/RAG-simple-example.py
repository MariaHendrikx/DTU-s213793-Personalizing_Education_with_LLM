from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample corpus: a small collection of documents
documents = [
    "The sky is blue and beautiful.",
    "Love this blue and beautiful sky!",
    "The quick brown fox jumps over the lazy dog.",
    "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
    "I love green eggs, ham, sausages, and bacon!",
    "The brown fox is quick and the blue dog is lazy!",
    "The sky is very blue and the sky is very beautiful today",
    "The dog is lazy but the brown fox is quick!"
]

# Queries: what we will search for in our corpus
queries = [
    "The blue sky is beautiful",
    "Quick brown foxes",
]

# Step 1: Vectorization - Convert text documents to vectors
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(documents)
document_vectors = vectorizer.transform(documents)

# Step 2: Transform queries into the same vector space as documents
query_vectors = vectorizer.transform(queries)

# Step 3: Retrieve most similar document for each query
for query, query_vector in zip(queries, query_vectors):
    # Calculate cosine similarity between query and all documents
    similarities = cosine_similarity(query_vector, document_vectors)
    
    # Find the index of the document with the highest similarity
    most_similar_doc_index = np.argmax(similarities)
    
    # Fetch the most similar document from the corpus
    most_similar_doc = documents[most_similar_doc_index]
    
    print(f"Query: {query}\nMost Similar Document: {most_similar_doc}\n")

# Explanation of what's happening:
# 1. Vectorization: The TfidfVectorizer converts text into a high-dimensional sparse matrix where each dimension corresponds to a unique word (excluding stop words) in the corpus. TF-IDF scores represent the importance of each word within the documents.
# 2. Query Vectorization: Queries are transformed into vectors using the same vocabulary and TF-IDF weighting scheme as the documents.
# 3. Similarity Calculation: Cosine similarity measures how similar the query vector is to each of the document vectors. A higher cosine similarity score indicates a higher degree of similarity.
# 4. Retrieval: The document with the highest similarity score to the query is considered the most relevant and is retrieved as the result.
