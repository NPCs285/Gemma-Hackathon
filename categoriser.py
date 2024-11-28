from langchain_core.prompts import PromptTemplate
from model.transaction import transaction_parser, Transaction
from langchain_ollama import ChatOllama

from db.db import create_db_conn
from sql.transaction import Querier as TransactionQuerier
from helper_utils import generate_uuid

llm = ChatOllama(
    model="gemma2:2b",
    temperature=0
)


def categoriser_chain():
    template = """
    You will receive a input representing a financial transaction which contains the fields 'remarks' and 'amount'
    Your task is to determine the category of the transaction based on the remarks field.
    The transaction for which the category has to be figured out is:
    {transaction}

    Instructions:
    Analyze the remarks to infer the purpose of the transaction.

    Map the transaction to one of the following predefined categories:

    - Food: Includes restaurants, cafes, fast food, and dining expenses.
    - Shopping: Includes purchases of clothing, electronics, or general retail.
    - Transportation: Includes spending on fuel, public transport, ride-sharing, or vehicle expenses.
    - Utilities & Bills: Includes payments for electricity, water, internet, or other recurring bills.
    - Entertainment: Includes streaming services, movies, or recreational activities.
    - Travel: Includes bookings for flights, hotels, or travel-related expenses.
    - Unknown: Use this category if the remarks does not provide enough context to classify.

    If the remarks contains ambiguous or insufficient information, set the category field to 'Unknown'.
    Generate only the required output with the values provided in the input and your inference, nothing else.


    \n\n{format_instruction}
    """

    prompt_template = PromptTemplate(
        input_variables=['transaction'],
        template=template,
        partial_variables={
            "format_instruction": transaction_parser.get_format_instructions()
        },
    )

    return prompt_template | llm | transaction_parser


# Use Transaction class and change input as required
def Categoriser(input: Transaction) -> Transaction:
    chain = categoriser_chain()
    ans = chain.invoke(
        input={'transaction': input_statement},
    )
    return ans


txn_list = ["PCD/1407/Wow Momo DLF Wow Chick/CHENNAI281124/14:27",
            "PCD/1407/EVERSUB INDIA PRIVATE/CHENNAI281124/14:27",
            "BATH & BODY WORKS 2095 CHAMPAIGN IL 225519 11/17",
            "Zelle Payment From Deepika Satishkumar 22549586066",
            "Card Purchase  10/26 Lyft *Ride Fri 10Pm Lyft.Com Ca Card 6083",
            "UPI/Blinkit/432947349655/OidZTBLINUPIC24"]

input_statement = {"remarks": txn_list[4], "amount": 251}

ans = Categoriser(input_statement)

conn = create_db_conn()
transaction_querier = TransactionQuerier(conn=conn)
id = generate_uuid()
transaction_querier.insert_transaction(
    id=id, amount=ans.amount, remarks=ans.remarks, category=ans.category)
conn.commit()

# values = transaction_querier.get_transaction()
# for txn in values:
#     print(txn)
