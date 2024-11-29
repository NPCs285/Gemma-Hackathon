import pandas as pd
import ollama
import numpy as np
import faiss


def encode_chunks(chunks, filename):
    document_embeddings = []
    df_documents = pd.DataFrame(columns=['path', 'text_chunks', 'embeddings'])
    for chunk in chunks:
        embedding = ollama.embeddings("all-miniln", prompt=[chunk])
        document_embeddings.append(embedding)
    new_row = pd.DataFrame({'name': [filename], 'text_chunks': [
                           chunks], 'embeddings': document_embeddings})
    df_documents = pd.concat([df_documents, new_row], ignore_index=True)
    return df_documents


# Switch to Chroma
# Store data in chroma and fetch it from there
def find_most_similar_chunks(query, df_documents, top_k=5):
    all_embeddings = np.vstack(df_documents['embeddings'].tolist())
    dimension = all_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(all_embeddings)

    query_embedding = ollama.embeddings("all-miniln", prompt=[query])
    distances, indices = index.search(query_embedding, top_k)
    results = []
    total_chunks = sum(len(chunks) for chunks in df_documents['text_chunks'])
    for i, idx in enumerate(indices[0]):
        if idx < total_chunks:
            doc_idx = 0
            chunk_idx = idx
            while chunk_idx >= len(df_documents['text_chunks'].iloc[doc_idx]):
                chunk_idx -= len(df_documents['text_chunks'].iloc[doc_idx])
                doc_idx += 1
            results.append({
                'document': df_documents['path'].iloc[doc_idx],
                'chunk': df_documents['text_chunks'].iloc[doc_idx][chunk_idx],
                'distance': distances[0][i]
            })
    return results
