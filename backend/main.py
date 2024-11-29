from service.transformer import encode_chunks, find_most_similar_chunks
import ollama
from fastapi import FastAPI, File, UploadFile
from service.pdf import get_pdf_dataframe
from service.csv import get_csv_dataframe

app = FastAPI()


@app.get("/")
async def hello_world():
    return "Hello"


@app.post("/file/upload")
async def file_upload(file: UploadFile):
    df = get_csv_dataframe(file.file)
    print(df)
    return {"filename": file.filename, "type": file.content_type}


@app.post("/file/chat")
async def file_chat(file: UploadFile, query: str):
    chunks = get_pdf_dataframe(file.file)
    df_documents = encode_chunks(chunks, file.filename)
    similar_chunks = find_most_similar_chunks(query, df_documents)
    context = " ".join([chunk['chunk'] for chunk in similar_chunks])
    response = ollama.ask("gemma", prompt=f"Context: {context}\n\nQuestion: {query}")
    
    return {"response": response}