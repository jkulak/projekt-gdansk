import sys
import algorithms
from data_handling import read_data_file, get_data_files, pd_read_data_file
from metrics import add_average_true_range
from tabulate import tabulate

DATA_DIR = "./test_data/5 min/us/nyse stocks/1/"


def main():
    results = []
    files = get_data_files(DATA_DIR)
    for file in files:
        df = pd_read_data_file(DATA_DIR + file)
        df = add_average_true_range(df)

        # Group by date column and iterate over each group
        for date, group in df.groupby("date"):
            # Do something with each group, such as calculating daily statistics or plotting data
            # print(f"Date: {date}")
            # print(group.head())
            result = algorithms.the_nilesh_method(group)
            results.append({date, result})

        print(tabulate(results, headers=["Date", "Result"], tablefmt="grid"))
        sys.exit(0)


if __name__ == "__main__":
    main()
