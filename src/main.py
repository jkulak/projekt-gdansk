import sys
import algorithms
from data_handling import get_data_files, pd_read_data_file
from metrics import add_average_true_range, add_daily_atr_to_dataframe
from tabulate import tabulate

# DATA_DIR = "./test_data/5 min/us/nasdaq stocks/1/"
DATA_DIR = "./test_data/popular/"


def main():
    files = get_data_files(DATA_DIR)
    ticker_results = []
    ticker_total = 0

    for file in files:
        results = []
        total = 0
        df = pd_read_data_file(DATA_DIR + file)
        df = add_daily_atr_to_dataframe(df, 9)

        # Group by date column and iterate over each group
        for date, group in df.groupby("date"):
            # print(group)
            result = algorithms.the_nilesh_method(group)
            total += result
            results.append((date, result, total, group.iloc[0]["atr_9"]))

        print(
            tabulate(
                results, headers=["Date", "Result", "Total", "ATR9"], tablefmt="grid"
            )
        )

        ticker_results.append((file, total))

    # print(tabulate(ticker_results, headers=["File", "Total"], tablefmt="grid"))


if __name__ == "__main__":
    main()
