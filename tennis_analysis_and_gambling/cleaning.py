#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from tennis_analysis_and_gambling.config import ATP_SERIES_TO_RENAME
from tennis_analysis_and_gambling.config import NUMERIC_COLS


def clean_atp(
    df: pd.DataFrame,
    max_nb_sets: int,
    series_to_rename: dict = ATP_SERIES_TO_RENAME,
    cols_to_correct: list = NUMERIC_COLS,
) -> pd.DataFrame:
    df = df[df["Comment"] == "Completed"]  # keep only completed games
    df = df[df["Best of"] == max_nb_sets]
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
    df[cols] = df[cols].replace("NR", np.nan)
    df[cols] = df[cols].replace(" ", np.nan).astype(dtype)
    return df
