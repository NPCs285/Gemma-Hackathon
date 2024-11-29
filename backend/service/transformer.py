import pandas as pd
import ollama
import numpy as np


def encode_chunks(chunks, filename):
    document_embeddings = []
    df_documents = pd.DataFrame(columns=['path', 'text_chunks', 'embeddings'])
    for chunk in chunks:
        embedding = ollama.embeddings("all-miniln", prompt=chunk)
        document_embeddings.append(embedding)
    new_row = pd.DataFrame({'name': [filename], 'text_chunks': [
                           chunks], 'embeddings': document_embeddings})
    df_documents = pd.concat([df_documents, new_row], ignore_index=True)
    return df_documents


# Switch to Chroma
# Store data in chroma and fetch it from there
def find_most_similar_chunks(query, df_documents, top_k=5):
    query_embedding = ollama.embeddings("all-miniln", prompt=[query])
    results = []
    for i, doc_embeddings in enumerate(df_documents['embeddings']):
        for j, chunk_embedding in enumerate(doc_embeddings):
            similarity = np.dot(query_embedding, chunk_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding))
            results.append({'document': df_documents['path'].iloc[i], 'chunk': df_documents['text_chunks'].iloc[i][j], 'similarity': similarity})
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]
