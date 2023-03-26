import pandas as pd


def add_average_true_range(df, n=9):
    # Calculate the true range
    df["tr1"] = abs(df["high"] - df["low"])
    df["tr2"] = abs(df["high"] - df["close"].shift())
    df["tr3"] = abs(df["low"] - df["close"].shift())
    df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df.drop(["tr1", "tr2", "tr3"], axis=1, inplace=True)

    # Calculate the ATR using a rolling window of 9 days
    df["atr"] = df["true_range"].rolling(window=n).mean()

    return df
