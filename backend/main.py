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
async def file_chat(file: UploadFile):
    return {"filename": file.filename, "type": file.content_type}
