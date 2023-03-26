from collections import defaultdict
import algorithms
from data_handling import read_data_file, get_data_files, pd_read_data_file
from metrics import calculate_average_true_range
import os

DATA_DIR = "./test_data/5_min/us/nyse_stocks/1/"


def group_rows_by_date(data):

    return rows_by_date


def main():

    files = get_data_files(DATA_DIR)
    for file in files:
        data = pd_read_data_file(DATA_DIR + file)

        data_atr = calculate_average_true_range(data)

        rows_by_date = group_rows_by_date(data)
        for date, rows in rows_by_date.items():
            print(date, rows)

            index, first_row = rows[0]
            print(index, first_row)
            os.exit(1)
            # if index >= 9:
            #     avg_true_range = data_atr[index - 9]
            #     print(
            #         f"Running algo for date {date} with average true range {avg_true_range}"
            #     )
            #     algo(first_row)
            #     print(algo(first_row, 1, 2, 3, 4, 5))
            # else:
            #     print(
            #         f"Skipping date {date} as there are not enough previous days to calculate ATR"
            #     )


if __name__ == "__main__":
    main()
