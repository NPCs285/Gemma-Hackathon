from insights_agent import PostgresInsightsAgent
from service.transformer import encode_chunks, find_most_similar_chunks
import ollama
from fastapi import FastAPI, File, UploadFile

from service.pdf import get_pdf_chunks
from service.ocr import ocr_to_text
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

@app.post("/file/ocr")
async def file_ocr(file: UploadFile, query: str):
    ocr_result=ocr_to_text(file.file)
    context = " ".join([transaction["Details"] for transaction in ocr_result["transactions"]])
    response = ollama.generate(
        model="gemma2:2b", prompt=f"Context: {context}\n\nQuestion: {query}")

    return {"response": response}

  
@app.get("/insights")
async def insights(query: str):
    try:
        agent = PostgresInsightsAgent()
        print("PostgreSQL Transaction Insights Agent")
        print("====================================")
            
        print("\nAnalyzing...")
        response = agent.get_insights(query)
        print("\nInsights:", response)
        return {"response": response}
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"response": f"An unexpected error occurred: {e}"}
