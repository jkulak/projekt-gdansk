import csv
import os


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
