#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from tennis_analysis_and_gambling.config import ATP_SERIES_TO_RENAME
from tennis_analysis_and_gambling.config import NUMERIC_COLS


def clean_atp(
    df: pd.DataFrame,
    series_to_rename: dict = ATP_SERIES_TO_RENAME,
    cols_to_correct: list = NUMERIC_COLS,
) -> pd.DataFrame:
    """
    Cleans and standardizes an ATP match history DataFrame by filtering, correcting, and renaming columns.

    Args:
        df (pd.DataFrame): The DataFrame containing raw ATP match data.
        max_nb_sets (int): The maximum number of sets for filtering matches (e.g., 3 for best of 3, 5 for best of 5).
        series_to_rename (dict, optional): A dictionary for renaming "Series" column values to standardize names.
                                        Defaults to ATP_SERIES_TO_RENAME.
        cols_to_correct (list, optional): A list of columns to convert to numeric type. Defaults to NUMERIC_COLS.

    Returns:
        pd.DataFrame: The cleaned and standardized DataFrame.

    The cleaning process includes:
        - Filtering for completed matches only.
        - Filtering matches by the maximum number of sets (e.g., best of 3 or 5).
        - Removing odds that are less than 1.
        - Standardizing date format and stripping whitespace from "Winner" and "Loser" columns.
        - Renaming "Series" values based on the provided dictionary.
        - Ensuring that specified columns are of type float.
        - Removing duplicate rows and resetting the index.

    Notes:
        - The "Series" renaming is based on ATP Tour categories, and more details can be found at https://en.wikipedia.org/wiki/ATP_Tour.
        - The function assumes the DataFrame has columns "Comment", "Best of", "Date", "Winner", "Loser", and "Series".
    """

    df = df[df["Comment"] == "Completed"]  # keep only completed games
    df = df[(df["B365W"] >= 1) & (df["B365L"] >= 1)]  # odds can't be less than 1
    df = df[~df["Best of"].isnull()]  # Delete rows where 'Best of' is null
    df["Date"] = pd.to_datetime(df["Date"])
    df["Winner"] = df["Winner"].apply(lambda x: x.strip())
    df["Loser"] = df["Loser"].apply(lambda x: x.strip())

    # Series old names are changed to standardize
    # See https://en.wikipedia.org/wiki/ATP_Tour for more details
    df["Series"] = df["Series"].replace(series_to_rename)
    df = ensure_cols_dtype(df=df, cols=cols_to_correct, dtype="float")
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def ensure_cols_dtype(df: pd.DataFrame, cols: list, dtype: str) -> pd.DataFrame:
    """
    Ensures that specified columns in a DataFrame are of a given data type, replacing invalid values.

    Args:
        df (pd.DataFrame): The DataFrame containing the columns to be processed.
        cols (list): A list of column names to be checked and converted.
        dtype (str): The target data type to convert the columns to (e.g., "float", "int").

    Returns:
        pd.DataFrame: The DataFrame with the specified columns converted to the given data type.

    The process includes:
        - Replacing invalid values such as "NR" (Not Ranked) and blank spaces with NaN.
        - Converting the specified columns to the provided data type.

    Notes:
        - This function is useful for standardizing numeric columns that may contain non-numeric placeholders like "NR".
        - Ensure that `dtype` is a valid string representation of a NumPy or pandas data type.
    """
    df[cols] = df[cols].replace("NR", np.nan)
    df[cols] = df[cols].replace(" ", np.nan).astype(dtype)
    return df
