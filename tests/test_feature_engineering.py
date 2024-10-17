#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import numpy as np
import pandas as pd

from tennis_analysis_and_gambling.feature_engineering import add_feaures_odds_ranks
from tennis_analysis_and_gambling.feature_engineering import add_targets


class TestFeatureEngineering(unittest.TestCase):

    def setUp(self) -> None:
        data_atp = {
            "Comment": ["Completed", "Completed", "Completed", "Walkover"],
            "Best of": [3, 3, 5, 3],
            "Date": ["2023-01-10", "2023-01-12", "2023-01-15", "2023-01-18"],
            "Winner": [" Player A ", "Player B", " Player C ", "Player D"],
            "Loser": [" Player W", " Player X", "Player Y", " Player Z "],
            "Series": ["International Gold", "Masters", "Grand Slam", "ATP250"],
            "W1": [6, 6, 6, 3],
            "L1": [2, 4, 0, 6],
            "W2": [6, 3, 6, 7],
            "L2": [3, 6, 0, 5],
            "W3": [np.nan, 6, 1, 7],
            "L3": [np.nan, 4, 6, 6],
            "W4": [np.nan, np.nan, 6, np.nan],
            "L4": [np.nan, np.nan, 0, np.nan],
            "W5": [np.nan, np.nan, np.nan, np.nan],
            "L5": [np.nan, np.nan, np.nan, np.nan],
            "Wsets": [2, 2, 3, 2],
            "Lsets": [0, 1, 1, 1],
            "B365W": [1.1, 1.5, 1.5, 2.5],
            "B365L": [5.0, 2.3, 2.25, 1.4],
            "WRank": [1, 20, 100, 30],
            "LRank": [40, 35, 95, 65],
        }
        self.df_test_atp = pd.DataFrame(data=data_atp)

    def test_add_features_odds_ranks(self):
        df_featured = add_feaures_odds_ranks(self.df_test_atp)

        expected_sumodd_col = pd.Series([6.1, 3.8, 3.75, 3.9], name="SumOdd")
        expected_gapodd_col = pd.Series([3.9, 0.8, 0.75, 1.1], name="GapOdd")
        expected_productodd_col = pd.Series([5.5, 3.45, 3.375, 3.5], name="ProductOdd")
        expected_sumrank_col = pd.Series([41, 55, 195, 95], name="SumRank")
        expected_gaprank_col = pd.Series([39, 15, 5, 35], name="GapRank")

        pd.testing.assert_series_equal(df_featured["SumOdd"], expected_sumodd_col)
        pd.testing.assert_series_equal(df_featured["GapOdd"], expected_gapodd_col)
        pd.testing.assert_series_equal(df_featured["ProductOdd"], expected_productodd_col)
        pd.testing.assert_series_equal(df_featured["SumRank"], expected_sumrank_col)
        pd.testing.assert_series_equal(df_featured["GapRank"], expected_gaprank_col)

    def test_add_targets(self):
        df_targets = add_targets(self.df_test_atp, "atp")
        expected_total_games = pd.Series([17, 29, 25, 34], dtype=float, name="TotalGames")
        expected_total_sets = pd.Series([2, 3, 4, 3], name="TotalSets")
        expected_both_score = pd.Series([False, True, True, True], name="BothScore")
        expected_fav_odd_win = pd.Series([True, True, True, False], name="FavOddWin")
        expected_fav_rank_win = pd.Series([True, True, False, True], name="FavRankWin")

        pd.testing.assert_series_equal(df_targets["TotalGames"], expected_total_games)
        pd.testing.assert_series_equal(df_targets["TotalSets"], expected_total_sets)
        pd.testing.assert_series_equal(df_targets["BothScore"], expected_both_score)
        pd.testing.assert_series_equal(df_targets["FavOddWin"], expected_fav_odd_win)
        pd.testing.assert_series_equal(df_targets["FavRankWin"], expected_fav_rank_win)
