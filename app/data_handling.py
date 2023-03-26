import csv
import os
import pandas as pd


def pd_read_data_file(file_path):
    df = pd.read_csv(
        file_path,
        header=0,
        names=[
            "ticker",
            "per",
            "date",
            "time",
            "open",
            "high",
            "low",
            "close",
            "vol",
            "openint",
        ],
    )
    return df


def get_data_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".txt")]


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def read_data_file(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = [
            {k: float(v) if is_float(v) else v for k, v in row.items()}
            for row in reader
        ]
    # return headers, data
    return data
