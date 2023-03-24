import csv
import os
import fnmatch
import sys

TEST_DATA_DIR = "tests/data/"
TEST_SETUP_FLIE = "tests/setup.csv"
TEST_SCENARIONS_FLIE = "tests/scenarios.csv"


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def read_csv_file(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = [
            {k: float(v) if is_float(v) else v for k, v in row.items()}
            for row in reader
        ]
    # return headers, data
    return data


def run_tests():
    print("Running tests...")

    # Read the test files
    test_setup = read_csv_file(TEST_SETUP_FLIE)[0]
    test_scenarios = read_csv_file(TEST_SCENARIONS_FLIE)

    for scenario in test_scenarios:
        print(f"Running {scenario['case_name']} ", end="")

        test_data = read_csv_file(TEST_DATA_DIR + scenario["case_name"] + ".csv")

        if (
            algo(
                test_data,
                test_setup["b"],
                test_setup["u1"],
                test_setup["u2"],
                test_setup["d1"],
                test_setup["d2"],
            )
            == scenario["result"]
        ):
            print("✅")
        else:
            print("🚫")


# returns stock price difference between buying price to selling price
# TICKER,PER,DATE,TIME,OPEN,HIGH,LOW,CLOSE,VOL,OPENINT
def algo(data, b, u1, u2, d1, d2):

    for row in data:

        # case 1, going up, buy at u1, sell at u2
        if (row["HIGH"] >= u2 or row["OPEN"] >= u2 or row["CLOSE"] >= u2) and (
            row["LOW"] > b
        ):
            return u2 - u1

        # case 2, locking at u1 and

    return 1


def main():
    print("Let's do it!")
    run_tests()


if __name__ == "__main__":
    main()
