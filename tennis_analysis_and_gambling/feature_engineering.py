#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from tennis_analysis_and_gambling.config import ATP_SCORE_COLS
from tennis_analysis_and_gambling.config import ODDS_COLS
from tennis_analysis_and_gambling.config import RANK_COLS
from tennis_analysis_and_gambling.config import SETS_COLS
from tennis_analysis_and_gambling.config import WTA_SCORE_COLS


def add_feaures_odds_ranks(df: pd.DataFrame):
    df["SumOdd"] = df[ODDS_COLS].sum(axis=1)
    df["GapOdd"] = abs(df["B365W"] - df["B365L"])
    df["ProductOdd"] = df["B365W"] * df["B365L"]
    df["SumRank"] = df[RANK_COLS].sum(axis=1)
    df["GapRank"] = abs(df["WRank"] - df["LRank"])
    return df


def add_targets(df: pd.DataFrame, atp_or_wta: str) -> pd.DataFrame:
    if atp_or_wta.lower() == "atp":
        score_cols = ATP_SCORE_COLS
    elif atp_or_wta.lower() == "wta":
        score_cols = WTA_SCORE_COLS
    else:
        raise ValueError((f"{atp_or_wta} not correct. Please select 'ATP' or 'WTA'"))

    df["TotalGames"] = df[score_cols].sum(axis=1)
    df["TotalSets"] = df[SETS_COLS].sum(axis=1)
    # Both scores at least one set
    df["BothScore"] = df.apply(lambda row: True if row["Lsets"] > 0 else False, axis=1)
    # Favorite player according to the odds wins
    df["FavOddWin"] = df.apply(lambda row: True if row["B365W"] < row["B365L"] else False, axis=1)
    # Favorite player according to his rank wins
    df["FavRankWin"] = df.apply(lambda row: True if row["WRank"] < row["LRank"] else False, axis=1)

    return df


def update_elo_rank(df: pd.DataFrame, initial_elo: int = 1500) -> pd.DataFrame:
    players = pd.concat([df["Winner"], df["Loser"]]).unique()
    elo_dict = pd.Series(initial_elo, index=players)
    for index, row in df.iterrows():
        winner = row["Winner"]
        loser = row["Loser"]

        elo_winner = elo_dict[winner]
        elo_loser = elo_dict[loser]

        new_elo_winner, new_elo_loser = calculate_elo_ranking(winner, loser, elo_dict)

        elo_dict[winner] = new_elo_winner
        elo_dict[loser] = new_elo_loser

        df.loc[index, "elo_Winner"] = elo_winner
        df.loc[index, "elo_Loser"] = elo_loser
    return df


def calculate_elo_ranking(winner: str, loser: str, elo_dict: dict, k_factor: int = 32):
    """
    Calculate new ELO ratings
    https://en.wikipedia.org/wiki/Elo_rating_system

    """
    actual_elo_rank_winner = elo_dict[winner]
    actual_elo_rank_loser = elo_dict[loser]

    expected_value = 1 / (1 + 10 ** ((actual_elo_rank_loser - actual_elo_rank_winner) / 400))

    new_elo_rank_winner = actual_elo_rank_winner + k_factor * (1 - expected_value)
    new_elo_rank_loser = actual_elo_rank_loser + k_factor * (0 - (1 - expected_value))

    return new_elo_rank_winner, new_elo_rank_loser
