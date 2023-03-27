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
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

    return df


def get_data_files(directory):
    return sorted([file for file in os.listdir(directory) if file.endswith(".txt")])
