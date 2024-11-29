from fastapi import File
import pandas as pd


def get_csv_dataframe(file: File):
    df = pd.read_csv(file)
    return df
