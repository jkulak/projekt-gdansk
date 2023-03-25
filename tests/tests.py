import sys
import unittest
from app import algo


def convert_to_dict_list(table):
    headers = ["OPEN", "HIGH", "LOW", "CLOSE"]
    dict_list = [dict(zip(headers, row)) for row in table]
    return dict_list


def test_data_sanity_check(tests):
    for test in tests:
        for row in test["data"]:
            assert len(row) == 4, "Each row must have 4 elements"
            assert type(row) == list, "Each row must be a list"
            assert row[0] <= row[1], "Open must be less than or equal to high"
            assert row[3] <= row[1], "Close must be less than or equal to high"
            assert row[0] >= row[2], "Open must be greater than or equal to low"
            assert row[3] >= row[2], "Close must be greater than or equal to low"
            assert row[1]


def set_up_parameters():
    return [10, 20, 30, 40, 50]


class TestAlgo(unittest.TestCase):
    def test_algo_case1(self):
        "Test case 1: going up, buy at u1, sell at u2"

        tests = [
            {
                "case_name": "in first minute, trigger buy and stop loss",
                "data": [
                    [29, 41, 28, 40],
                    [99, 99, 99, 99],
                ],
                "expected_result": -10,
            },
            {
                "case_name": "b",
                "data": [
                    [30, 51, 28, 40],
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
                "case_name": "n",
                "data": [
                    [30, 39, 30, 39],  # nothing is happening
                    [31, 41, 31, 39],  # trigger buy
                    [31, 39, 31, 39],  # nothing is happening
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
            # {
            #     "case_name": "p",
            #     "data": [
            #         [30, 39, 30, 39],  # nothing is happening
            #         [31, 41, 31, 39],  # trigger buy
            #         [31, 42, 31, 39],  # sell is not happening
            #         [29, 45, 29, 45],  # partial win
            #     ],
            #     "expected_result": 10,
            # },
        ]
        test_data_sanity_check(tests)

        for test in tests:
            with self.subTest(test["case_name"]):
                self.assertAlmostEqual(
                    algo.algo(convert_to_dict_list(test["data"]), *set_up_parameters()),
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
            "algo() returns an float"
            self.assertEqual(
                type(
                    algo.algo(convert_to_dict_list(test["data"]), *set_up_parameters())
                ),
                float,
            )


if __name__ == "__main__":
    unittest.main()
