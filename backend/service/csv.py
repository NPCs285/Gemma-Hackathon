from fastapi import File
import pandas as pd



def csv_to_text(file: File):
    df = pd.read_csv(file)
    return df
