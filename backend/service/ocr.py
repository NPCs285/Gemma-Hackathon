import pytesseract
from PIL import Image
import pandas as pd
import re


def ocr_to_text(image_path, psm_mode=6):

    image = Image.open(image_path)
    custom_config = f'--psm {psm_mode}'
    raw_text = pytesseract.image_to_string(image, config=custom_config)
    rows = raw_text.split('\n')
    transactions = []

    for row in rows:
        # Regex patterns to identify date, amount, and balance
        date_pattern = r'\d{2} \w{3} \d{4}'  # Example: "27 Aug 2024"
        amount_pattern = r"-?\d{1,3}(,\d{3})*(\.\d{2})?"  # Example: "-227.00" or "123.45"
        balance_pattern = r"\d{1,3}(,\d{3})*(\.\d{2})?"  # Example: "13,045.08"

        if re.search(date_pattern, row) and re.search(amount_pattern, row):
            date = re.search(date_pattern, row).group(0)
            amount = re.search(amount_pattern, row).group(0)
            balance_match = re.search(balance_pattern, row)
            balance = balance_match.group(0) if balance_match else "Unknown"
            transactions.append({
                "Date": date,
                "Details": row.strip(),
                "Amount": amount,
                "Balance": balance
            })
    df = pd.DataFrame(transactions)
    return {"status": "success", "transactions": df.to_dict(orient="records")}
    

   