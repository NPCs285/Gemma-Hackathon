from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from model.transaction import base_transaction_parser, transaction_list_parser, BaseTransaction

from fastapi import UploadFile
from service.pdf import get_pdf_chunks
from typing import List


def cleaner_chain():
    llm = ChatOllama(
        model="gemma2:2b",
        temperature=0.0,
    )
    template = """
    You are an AI designed to extract financial transactions from {type} document. Your task is to process the content and return a structured output containing only valid transactions.
    The content of the file is:
    ```
    {file_content}
    ```
    Generate the output and output only. Do not add unncessary details or texts. The output should contain data from the input content.
    If you cannot find proper transactions, return an empty object. If you find relvant fields, add them to the output as they are present
    in the input file.

    The format for the output is
    json
    ```
    {{
        "transactions": [
            {{
                "remarks": "The description about the transaction",
                "amount": "The amount credited or debited during the transaction",
            }}
        ]
    }}
    ```
    """

    prompt_template = PromptTemplate(
        input_variables=['type',  'file_content'],
        template=template,
        partial_variables={
            "format_instruction": transaction_list_parser.get_format_instructions()
        },
    )

    return prompt_template | llm | transaction_list_parser


def FileCleaner(file: UploadFile) -> List[BaseTransaction]:
    chain = cleaner_chain()
    type = ""
    if "pdf" in file.content_type:
        type = "pdf"
        output = []
        file_chunks = get_pdf_chunks(
            file.file, max_chunk_size=1900, chunk_overlap=100)
        print(len(file_chunks))

        for chunk in file_chunks:
            ans = chain.invoke(
                input={"type": type,  "file_content": chunk}
            )
            print(ans)
            print("\n\n\n")
            output.append(ans)
        print("Done")

    elif "csv" in file.content_type:
        type = "csv"

    return output
