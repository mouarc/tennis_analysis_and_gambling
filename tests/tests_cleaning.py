#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from tennis_analysis_and_gambling.cleaning import clean_atp
from tennis_analysis_and_gambling.cleaning import ensure_cols_score_dtype


class TestCleaning(unittest.TestCase):

    def setUp(self) -> None:
        data_atp = {
            "Comment": ["Completed", "Completed", "Completed", "Walkover"],
            "Best of": [3, 3, 5, 3],
            "Date": ["2023-01-10", "2023-01-12", "2023-01-15", "2023-01-18"],
            "Winner": [" Player A ", "Player B", " Player C ", "Player D"],
            "Loser": [" Player W", " Player X", "Player Y", " Player Z "],
            "Series": ["International Gold", "Masters", "Grand Slam", "ATP250"],
            "col1": [1, 2, "3", 4],
            "col2": ["1 ", 2, " ", 3],
        }
        self.df_test_atp = pd.DataFrame(data=data_atp)

    def test_ensure_dtypes(self):
        df_test_dtypes = ensure_cols_score_dtype(
            df=pd.DataFrame(data=self.df_test_atp),
            cols_score=["col1", "col2"],
        )
        self.assertEqual(df_test_dtypes["col1"].dtype, "float64")
        self.assertEqual(df_test_dtypes["col2"].dtype, "float64")

    def test_clean_atp(self):
        df_cleaned = clean_atp(self.df_test_atp, max_nb_sets=3, cols_score=["col1", "col2"])

        self.assertTrue((df_cleaned["Best of"] == 3).all())
        self.assertTrue((df_cleaned["Comment"] == "Completed").all())
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_cleaned["Date"]))
        self.assertEqual(df_cleaned["Winner"].iloc[0], "Player A")  # " Player A " is corrected
        self.assertEqual(df_cleaned["Loser"].iloc[0], "Player W")  # " Player W" is corrected
        self.assertEqual(
            df_cleaned["Series"].iloc[0], "ATP500"
        )  # "International Gold" is renamed "ATP500"
