import pandas as pd


def calculate_average_true_range(data, n=9):
    df = pd.DataFrame(data)
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(
        float
    )

    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"]).abs()
    low_close = (df["low"] - df["close"]).abs()

    tr = high_low.combine(high_close, max).combine(low_close, max)
    atr = tr.rolling(window=n).mean()

    return atr
