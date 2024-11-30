from service.transformer import encode_chunks, find_most_similar_chunks
import ollama
from fastapi import FastAPI, File, UploadFile

from service.pdf import get_pdf_chunks

from agents.cleaner import FileCleaner

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

# @app.get("/transaction")
