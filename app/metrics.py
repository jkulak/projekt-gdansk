import pandas as pd


def calculate_average_true_range(data, n=9):
    df = pd.DataFrame(data)
    df[["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]] = df[
        ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]
    ].astype(float)

    high_low = df["<HIGH>"] - df["<LOW>"]
    high_close = (df["<HIGH>"] - df["<CLOSE>"]).abs()
    low_close = (df["<LOW>"] - df["<CLOSE>"]).abs()

    tr = high_low.combine(high_close, max).combine(low_close, max)
    atr = tr.rolling(window=n).mean()

    return atr
