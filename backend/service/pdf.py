import PyPDF2
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from fastapi import File


def extract_text_from_pdf(file: File):
    try:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text()
                         for page in reader.pages if page.extract_text()])
        if not text.strip():
            raise ValueError("No text extracted.")
        return text
    except Exception:
        return "No text available for this document."


def split_text_into_chunks(text, max_chunk_size=1000, chunk_overlap=0):
    sentence_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", "?", "!"], chunk_size=1000,
        chunk_overlap=chunk_overlap
    )

    sentences = sentence_splitter.split_text(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def get_pdf_chunks(file: File, max_chunk_size=1000, chunk_overlap=0):
    pdf_text = extract_text_from_pdf(file)
    chucks = split_text_into_chunks(
        pdf_text, max_chunk_size=max_chunk_size, chunk_overlap=chunk_overlap)
    return chucks

