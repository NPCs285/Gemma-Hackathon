from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
async def hello_world():
    return "Hello"


@app.post("/file/upload")
async def file_upload(file: UploadFile):
    return {"filename": file.filename, "type": file.content_type}


@app.post("/file/chat")
async def file_chat(file: UploadFile):
    return {"filename": file.filename, "type": file.content_type}
