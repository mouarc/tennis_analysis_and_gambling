#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from tennis_analysis_and_gambling.config import ATP_SCORE_COLS
from tennis_analysis_and_gambling.config import ODDS_COLS
from tennis_analysis_and_gambling.config import RANK_COLS
from tennis_analysis_and_gambling.config import SETS_COLS
from tennis_analysis_and_gambling.config import WTA_SCORE_COLS


def add_features_odds_ranks(df: pd.DataFrame):
    """
    Adds new features related to betting odds and player rankings to the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing tennis match data, including columns for betting odds and player rankings.

    Returns:
        pd.DataFrame: The DataFrame with new columns added for the following features:
            - "SumOdd": The sum of all betting odds from the columns in `ODDS_COLS`.
            - "GapOdd": The absolute difference between the odds for the winner ("B365W") and the loser ("B365L").
            - "ProductOdd": The product of the odds for the winner ("B365W") and the loser ("B365L").
            - "SumRank": The sum of player rankings from the columns in `RANK_COLS`.
            - "GapRank": The absolute difference between the winner's rank ("WRank") and the loser's rank ("LRank").

    Notes:
        - The function assumes that the columns `ODDS_COLS` and `RANK_COLS` are predefined lists of relevant columns for betting odds and player rankings.
        - The odds used for "GapOdd" and "ProductOdd" are based on the "B365W" (winner) and "B365L" (loser) columns.
        - The player rankings used for "GapRank" are based on the "WRank" (winner's rank) and "LRank" (loser's rank) columns.
    """
    df["SumOdd"] = df[ODDS_COLS].sum(axis=1)
    df["GapOdd"] = abs(df["B365W"] - df["B365L"])
    df["ProductOdd"] = df["B365W"] * df["B365L"]
    df["SumRank"] = df[RANK_COLS].sum(axis=1)
    df["GapRank"] = abs(df["WRank"] - df["LRank"])
    return df


def add_targets(df: pd.DataFrame, atp_or_wta: str) -> pd.DataFrame:
    """
    Adds target columns to the DataFrame, which include total games, total sets, and boolean outcomes
    based on match statistics, betting odds, and player rankings.

    Args:
        df (pd.DataFrame): The DataFrame containing tennis match data, including score, sets, odds, and rankings.
        atp_or_wta (str): Specifies whether the data corresponds to ATP or WTA matches. Must be either "ATP" or "WTA".

    Returns:
        pd.DataFrame: The DataFrame with the following target columns added:
            - "TotalGames": The total number of games played in the match, calculated by summing the relevant score columns.
            - "TotalSets": The total number of sets played in the match.
            - "BothScore": A boolean value indicating whether both players scored at least one set.
            - "FavOddWin": A boolean value indicating whether the player with the lower odds (the favorite) won the match.
            - "FavRankWin": A boolean value indicating whether the player with the better ranking (the favorite) won the match.

    Raises:
        ValueError: If `atp_or_wta` is not "ATP" or "WTA".

    Notes:
        - The function determines which score columns to use based on whether the data is for ATP or WTA matches.
        - For "BothScore", a value of `True` means the losing player won at least one set.
        - For "FavOddWin", a value of `True` means the favorite based on betting odds (lower odds) won the match.
        - For "FavRankWin", a value of `True` means the favorite based on player ranking won the match.
    """
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
    """
    Updates the Elo ranking of tennis players based on match outcomes and stores the updated rankings in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing match data, with columns for the winner and loser of each match.
        initial_elo (int, optional): The initial Elo rating assigned to all players. Defaults to 1500.

    Returns:
        pd.DataFrame: The DataFrame with two new columns:
            - "elo_Winner": The Elo rating of the match winner before the match.
            - "elo_Loser": The Elo rating of the match loser before the match.

    Process:
        - The function first initializes all players with the same starting Elo rating (`initial_elo`).
        - For each match, it retrieves the current Elo ratings for the winner and the loser.
        - It then updates both players' Elo ratings based on the outcome of the match using the `calculate_elo_ranking` function.
        - The updated Elo ratings for both players are stored in `elo_Winner` and `elo_Loser`.

    Notes:
        - The function assumes that a separate `calculate_elo_ranking` function is available to handle the Elo ranking calculation.
        - The Elo rating is updated iteratively for each match in the DataFrame.
        - The initial Elo rating can be adjusted via the `initial_elo` parameter.
    """
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
    Calculates the new Elo ratings for the winner and the loser of a match based on their current ratings.

    Args:
        winner (str): The name of the player who won the match.
        loser (str): The name of the player who lost the match.
        elo_dict (dict): A dictionary containing the current Elo ratings of all players.
        k_factor (int, optional): The K-factor, which determines the sensitivity of the rating system. Defaults to 32.

    Returns:
        tuple: A tuple containing the updated Elo ratings for the winner and the loser as:
            - new_elo_rank_winner (float): The updated Elo rating of the winner.
            - new_elo_rank_loser (float): The updated Elo rating of the loser.

    Process:
        - The function retrieves the current Elo ratings of both the winner and the loser.
        - It calculates the expected outcome of the match using the Elo formula, which compares the ratings of both players.
        - The winner's Elo rating is increased, and the loser's rating is decreased, based on the match outcome and the expected value.
        - The K-factor controls how much the Elo rating changes, with a higher K-factor leading to larger rating adjustments.

    Notes:
        - The Elo formula is used to calculate the expected value, which determines the probability of the winner winning based on the current ratings.
        - The K-factor is set to 32 by default, but it can be adjusted to make the rating changes more or less sensitive.
        - For more information on the Elo rating system, refer to https://en.wikipedia.org/wiki/Elo_rating_system.
    """
    actual_elo_rank_winner = elo_dict[winner]
    actual_elo_rank_loser = elo_dict[loser]

    expected_value = 1 / (1 + 10 ** ((actual_elo_rank_loser - actual_elo_rank_winner) / 400))

    new_elo_rank_winner = actual_elo_rank_winner + k_factor * (1 - expected_value)
    new_elo_rank_loser = actual_elo_rank_loser + k_factor * (0 - (1 - expected_value))

    return new_elo_rank_winner, new_elo_rank_loser
