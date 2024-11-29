from fastapi import FastAPI, File, UploadFile

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
async def file_chat(file: UploadFile):
    return {"filename": file.filename, "type": file.content_type}

# @app.get("/transaction")
