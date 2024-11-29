from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from model.transaction import transaction_list_parser, TransactionList

from fastapi import UploadFile


def cleaner_chain():
    llm = ChatOllama(
        model="gemma2:2b",
        temperature=0
    )
    template = """
    You are an AI designed to extract financial transactions from {type} document. Your task is to process the content and return a structured output containing only valid transactions.

    The content of the file is:
    {file_content}

    \n\n{format_instruction}
    """

    prompt_template = PromptTemplate(
        input_variables=['type', 'file_content'],
        template=template,
        partial_variables={
            "format_instruction": transaction_list_parser.get_format_instructions
        },
    )

    return prompt_template | llm | transaction_list_parser


def FileCleaner(file: UploadFile) -> TransactionList:
    chain = cleaner_chain()
    type = ""
    if "pdf" in file.content_type:
        type = "pdf"
    elif "csv" in file.content_type:
        type = "csv"

    file_content = await file.file.read()
    file_string = file_content.decode('utf-8')
    ans = chain.invoke(
        input={"type": type, "file_content": file_string}
    )
    return ans
