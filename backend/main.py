from insights_agent import PostgresInsightsAgent
from service.transformer import encode_chunks, find_most_similar_chunks
import ollama
from fastapi import FastAPI, File, UploadFile

from service.pdf import get_pdf_chunks
from service.ocr import ocr_to_text
from service.transactions import get_all_transactions, get_category_transactions, insert_txn

from agents.cleaner import FileCleaner
from agents.categoriser import Categoriser

from helper_utils import flatten, str_to_float

app = FastAPI()


@app.get("/")
async def hello_world():
    return "Hello"

# Create a runner obj,
# Takes in the file and processes it in the background


@app.post("/file/upload")
async def file_upload(file: UploadFile):
    ans = FileCleaner(file)
    txns = []
    for obj in ans:
        txns.append(obj.to_list())
    flatten_arr = flatten(txns)

    final_txns = []
    for txn in flatten_arr:
        try:
            if len(txn['remarks']) == 0 or len(txn['amount']) == 0:
                continue
            updated_txn = Categoriser(txn)
            float_amt = str_to_float(updated_txn.amount)
            insert_txn(remarks=updated_txn.remarks,
                       amount=float_amt, category=updated_txn.category)
            final_txns.append(updated_txn)
        except Exception as e:
            print(f"Error with value {txn}: \n{e}\n\n")

    return final_txns


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


@app.get("/transactions")
def retrive_transactions():
    return get_all_transactions()


@app.get("/transctions/category")
def retrive_category_wise():
    return get_category_transactions()
