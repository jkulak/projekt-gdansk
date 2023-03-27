import pandas as pd

pd.set_option("display.max_rows", 1500)


def add_average_true_range(df, n=9):
    # Calculate the true range
    df["tr1"] = abs(df["high"] - df["low"])
    df["tr2"] = abs(df["high"] - df["close"].shift())
    df["tr3"] = abs(df["low"] - df["close"].shift())
    df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df.drop(["tr1", "tr2", "tr3"], axis=1, inplace=True)

    # Calculate the ATR using a rolling window of 9 days
    df["atr"] = df["true_range"].rolling(window=n).mean()

    # Drop rows with missing values (due to the rolling window)
    df.dropna(inplace=True)

    return df


def custom_rolling_mean(series, window):
    values = series.values
    result = [None] * len(series)

    for i in range(window - 1, len(series)):
        result[i] = values[i - window + 1 : i + 1].mean()

    return pd.Series(result, index=series.index)


def add_daily_atr_to_dataframe(df, atr_period=3):
    # Convert the 'date' column to datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Calculate the daily true range
    daily_df = df.groupby("date").agg({"high": "max", "low": "min", "close": "last"})
    daily_df["prev_close"] = daily_df["close"].shift(1)
    daily_df["high_low"] = daily_df["high"] - daily_df["low"]
    daily_df["high_prev_close"] = abs(daily_df["high"] - daily_df["prev_close"])
    daily_df["low_prev_close"] = abs(daily_df["low"] - daily_df["prev_close"])
    daily_df["true_range"] = daily_df[
        ["high_low", "high_prev_close", "low_prev_close"]
    ].max(axis=1)

    # Calculate the average true range with a custom rolling mean function
    daily_df[f"atr_{atr_period}"] = custom_rolling_mean(
        daily_df["true_range"], atr_period
    )

    # Merge the daily ATR values with the original 5-minute dataframe
    df = df.merge(daily_df[[f"atr_{atr_period}"]].reset_index(), on="date", how="left")

    return df
