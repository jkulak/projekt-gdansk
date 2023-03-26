import os
from algo import algo
from data_handling import read_csv_file, get_csv_files

DATA_DIR = "./test_data/daily/us/nyse_stocks/1/"


def main():

    # print current dirrectory
    print(os.getcwd())
    # list current directory
    print(os.listdir())
    print("Let's do it!")
    files = get_csv_files(DATA_DIR)
    for file in files:
        print(file)
        data = read_csv_file(DATA_DIR + file)
        print(algo(data, 0, 0, 0, 0, 0))


if __name__ == "__main__":
    main()
