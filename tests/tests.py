import sys
import unittest
from src import algorithms
import pandas as pd


def convert_to_dataframe(table):
    headers = ["OPEN", "HIGH", "LOW", "CLOSE"]
    dict_list = [dict(zip(headers, row)) for row in table]
    return dict_list


def convert_to_dataframe(data):
    df = pd.DataFrame(data, columns=["open", "high", "low", "close"])
    df["ticker"] = "TEST"
    df["per"] = 5
    df["date"] = pd.to_datetime(["2023-03-22"] * len(data))
    df["time"] = pd.Series([f"{i+1:06d}" for i in range(len(data))])
    df["vol"] = 100
    df["openint"] = 0
    df["true_range"] = df["high"] - df["low"]
    df["atr"] = df["true_range"].rolling(window=4).mean()
    df = df[
        [
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
            "true_range",
            "atr",
        ]
    ]
    return df


def test_data_sanity_check(tests):
    for test in tests:
        for row in test["data"]:
            assert len(row) == 4, "Each row must have 4 elements"
            assert type(row) == list, "Each row must be a list"
            assert row[0] <= row[1], "Open must be less than or equal to high"
            assert row[3] <= row[1], "Close must be less than or equal to high"
            assert row[0] >= row[2], "Open must be greater than or equal to low"
            assert row[3] >= row[2], "Close must be greater than or equal to low"
            assert row[1] >= row[2], "High must be greater than or equal to low"


def set_up_parameters():
    return [40]


class TestAlgo(unittest.TestCase):
    def test_algo_case1(self):
        "Test case 1: going up, buy at u1, sell at u2"

        tests = [
            {
                "case_name": "in first minute, trigger buy and stop loss",
                "data": [
                    [30, 41, 28, 40],  # h >= u1, l <= s
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "b",
                "data": [
                    [30, 51, 28, 40],  # h >= u2, l <= s
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "c",
                "data": [
                    [30, 40, 28, 40],
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "d",
                "data": [
                    [30, 40, 30, 40],
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": -10,
            },
            {
                "case_name": "e",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 50, 31, 39],  # buy and sell equal u2
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": 10,
            },
            {
                "case_name": "f",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 51, 31, 39],  # buy and sell greater u2
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": 10,
            },
            {
                "case_name": "g",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 50, 31, 39],  # buy and sell equal u2
                ],
                "expected_result": 10,
            },
            {
                "case_name": "h",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 51, 31, 39],  # buy and sell greater u2
                ],
                "expected_result": 10,
            },
            {
                "case_name": "j",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [31, 51, 31, 39],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "k",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [31, 51, 31, 39],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "l",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [31, 39, 31, 39],  # sell is not happening
                    [31, 51, 31, 39],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "m",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [29, 39, 29, 39],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "o",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [31, 51, 31, 39],  # trigger sell
                    [29, 39, 29, 39],  # loss
                ],
                "expected_result": 10,
            },
        ]
        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case2(self):
        "Test case 1: going up, buy at u1, sell between u1 and u2, partial win"

        tests = [
            {
                "case_name": "case 2 a",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 31, 45],  # partial win
                ],
                "expected_result": 5,
            },
            {
                "case_name": "case 2 b",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy greater u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 31, 45],  # partial win
                ],
                "expected_result": 5,
            },
            {
                "case_name": "case 2 c",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 29, 45],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 2 d",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy greater u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 29, 45],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 2 e",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 30, 45],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 2 f",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy greater u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 30, 45],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 2 g",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy greater u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 30, 45],  # loss
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 72, 31, 72],  # sell is not happening
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 2 h",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 36, 31, 34],  # sell is not happening
                    [31, 40, 31, 33],  # sell is not happening
                    [33, 46, 31, 46],  # partial win
                ],
                "expected_result": 6,
            },
        ]

        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case3(self):
        "Test case 3: going up, buy at u1, sell between s and u1, partial loss"

        tests = [
            {
                "case_name": "case 3 a",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 31, 35],  # partial loss
                ],
                "expected_result": -5,
            },
            {
                "case_name": "case 3 b",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy greater u1
                    [31, 42, 31, 39],  # sell is not happening
                    [31, 45, 31, 35],  # partial loss
                ],
                "expected_result": -5,
            },
            {
                "case_name": "case 3 h",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 40, 31, 39],  # trigger buy equal u1
                    [31, 36, 31, 34],  # sell is not happening
                    [31, 40, 31, 33],  # sell is not happening
                    [33, 46, 31, 36],  # partial loss
                ],
                "expected_result": -4,
            },
        ]

        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case_not_trade(self):
        "Test case no trade was triggered, returns zero"

        tests = [
            {
                "case_name": "case no trade a",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 39, 31, 39],  # nothing is happening
                    [31, 38, 31, 38],  # nothing is happening
                    [31, 38, 31, 35],  # no trade
                ],
                "expected_result": 0,
            },
            {
                "case_name": "case no trade b",
                "data": [
                    [30, 31, 29, 29],  # nothing is happening
                    [23, 23, 21, 23],  # nothing is happening
                    [24, 24, 22, 23],  # nothing is happening
                    [25, 29, 24, 27],  # no trade
                ],
                "expected_result": 0,
            },
            {
                "case_name": "case no trade b",
                "data": [
                    [30, 39, 21, 29],  # nothing is happening
                    [23, 38, 21, 31],  # nothing is happening
                    [34, 38, 25, 29],  # nothing is happening
                    [21, 38, 21, 38],  # no trade
                ],
                "expected_result": 0,
            },
        ]

        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case9(self):
        "Test case 9: going down, buy at d1, sell at d2"

        tests = [
            {
                "case_name": "in first minute, trigger buy and stop loss",
                "data": [
                    [30, 30, 19, 21],  # l < d1, h >= s
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "b",
                "data": [
                    [30, 30, 9, 21],  # l < d2, h >= s
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "c",
                "data": [
                    [30, 32, 20, 32],
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "d",
                "data": [
                    [30, 30, 20, 20],
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": -10,
            },
            {
                "case_name": "e",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 10, 21],  # buy and sell equal d2
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": 10,
            },
            {
                "case_name": "f",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 9, 21],  # buy and sell lower d2
                    [99, 99, 99, 99],  # is not reached
                ],
                "expected_result": 10,
            },
            {
                "case_name": "g",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 10, 21],  # buy and sell equal d2
                ],
                "expected_result": 10,
            },
            {
                "case_name": "h",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 9, 21],  # buy and sell lower d2
                ],
                "expected_result": 10,
            },
            {
                "case_name": "j",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy
                    [29, 29, 9, 21],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "k",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy
                    [29, 29, 9, 21],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "l",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy
                    [29, 29, 21, 21],  # sell is not happening
                    [29, 29, 9, 21],  # trigger sell
                ],
                "expected_result": 10,
            },
            {
                "case_name": "m",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy
                    [31, 31, 21, 21],  # loss
                ],
                "expected_result": -10,
            },
            {
                "case_name": "o",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy
                    [29, 29, 9, 21],  # trigger sell
                    [25, 31, 21, 21],  # loss
                ],
                "expected_result": 10,
            },
        ]
        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case8(self):
        "Test case 8: going down, buy at d1, sell between d1 and d2, partial win"

        tests = [
            {
                "case_name": "case 8 a",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 15, 15],  # partial win
                ],
                "expected_result": 5,
            },
            {
                "case_name": "case 8 b",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy lower d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 15, 15],  # partial win
                ],
                "expected_result": 5,
            },
            {
                "case_name": "case 8 c",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [25, 31, 21, 21],  # loss h>s
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 8 d",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy lower d1
                    [29, 29, 18, 21],  # sell is not happening
                    [25, 31, 21, 21],  # loss h>s
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 8 e",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 30, 15, 15],  # loss h=s
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 8 f",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy lower d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 30, 15, 15],  # loss h=s
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 8 g",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy lower d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 30, 15, 15],  # loss h=s
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 4, 4],  # sell is not happening
                ],
                "expected_result": -10,
            },
            {
                "case_name": "case 8 h",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 18, 21],  # sell is not happeningg
                    [27, 29, 14, 14],  # partial win
                ],
                "expected_result": 6,
            },
        ]

        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_algo_case7(self):
        "Test case 7: going down, buy at d1, sell between s and d1, partial loss"

        tests = [
            {
                "case_name": "case 7 a",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 25, 25],  # partial loss
                ],
                "expected_result": -5,
            },
            {
                "case_name": "case 7 b",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 19, 21],  # trigger buy lower d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 25, 25],  # partial loss
                ],
                "expected_result": -5,
            },
            {
                "case_name": "case 7 h",
                "data": [
                    [30, 30, 21, 21],  # nothing is happening
                    [29, 29, 20, 21],  # trigger buy equal d1
                    [29, 29, 18, 21],  # sell is not happening
                    [29, 29, 18, 21],  # sell is not happeningg
                    [27, 29, 24, 24],  # partial loss
                ],
                "expected_result": -4,
            },
        ]

        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algorithms.the_nilesh_method(
                        convert_to_dataframe(test["data"]), 40
                    ),
                    test["expected_result"],
                    places=5,
                )

    def test_type(self):
        tests = [
            {
                "case_name": "standard",
                "data": [
                    [30, 41, 30, 40],
                    [40, 50, 31, 40],
                    [40, 41, 31, 40],
                    [40, 41, 31, 40],
                ],
                "expected_result": 10,
            }
        ]

        test_data_sanity_check(tests)

        for test in tests:
            "algo() returns a float"
            self.assertEqual(
                type(
                    algorithms.the_nilesh_method(convert_to_dataframe(test["data"]), 40)
                ),
                float,
            )


if __name__ == "__main__":
    unittest.main()
