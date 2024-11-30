from service.transformer import encode_chunks, find_most_similar_chunks
import ollama
from fastapi import FastAPI, File, UploadFile
from langchain_ollama import ChatOllama

from service.pdf import get_pdf_chunks
from service.ocr import ocr_to_text
from service.csv import csv_to_text
from agents.cleaner import FileCleaner

import csv
from io import StringIO

import chromadb
from chromadb.utils import embedding_functions

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="all-minilm"
)

chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")

app = FastAPI()


@app.get("/")
async def hello_world():
    return "Hello"


@app.post("/file/upload")
async def file_upload(file: UploadFile):
    ans = FileCleaner(file)
    return ans


@app.post("/file/chat")
async def file_chat(file: UploadFile, query: str):
    chunks = get_pdf_chunks(file.file)
    df_documents = encode_chunks(chunks, file.filename)
    similar_chunks = find_most_similar_chunks(query, df_documents)
    context = " ".join([chunk['chunk'] for chunk in similar_chunks])
    response = ollama.generate(
        model="gemma2:2b", prompt=f"Context: {context}\n\nQuestion: {query}")

    return {"response": response}


@app.post("/file/ocr")
async def file_ocr(file: UploadFile, query: str):
    ocr_result = ocr_to_text(file.file)
    context = " ".join([transaction["Details"]
                       for transaction in ocr_result["transactions"]])
    response = ollama.generate(
        model="gemma2:2b", prompt=f"Context: {context}\n\nQuestion: {query}")

    return {"response": response}


@app.post("/file/csv")
async def file_csv(file: UploadFile, query: str):
    # Note: Used Chromadb for storing and retrieving relevant chunks
    #     Try to use present functions
    content = file.file.read()
    text_content = content.decode('utf-8')
    csv_reader = csv.reader(StringIO(text_content))
    rows = [row for row in csv_reader]
    chunks = []
    for row in rows:
        chunks.append(' '.join(row))
    # df_documents = encode_chunks(chunks, file.filename)
    # similar_chunks = find_most_similar_chunks(query, df_documents)
    # context = " ".join([chunk['chunk'] for chunk in similar_chunks])

    # Using ChromaDB for storing and getting relevant chunks
    for i, row in enumerate(rows):
        chunks.append({"id": f"{i+1}", "text": ' '.join(row)})

    collection = chroma_client.get_or_create_collection(
        name=file.filename, embedding_function=ollama_ef
    )

    def get_ollama_embeddings(text):
        response = ollama.embeddings(model="all-minilm", prompt=text)
        return response['embedding']

    for chunk in chunks:
        chunk['embedding'] = get_ollama_embeddings(chunk['text'])
        if len(chunk['text']) == 0 or len(chunk['embedding']) == 0:
            continue
        collection.upsert(
            ids=chunk['id'], documents=chunk['text'], embeddings=chunk['embedding'])

    results = collection.query(query_texts=query, n_results=10)
    context = [doc for sublist in results['documents']
               for doc in sublist]

    llm = ChatOllama(
        model="gemma2:2b",
        temperature=0.0,
        top_k=10
    )
    message = f"Context: {context}\n\n Question: {query}"
    response = llm.invoke(message)

    chroma_client.delete_collection(file.filename)
    return {"response": response}
