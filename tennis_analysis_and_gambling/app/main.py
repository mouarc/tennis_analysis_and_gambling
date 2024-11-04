#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from datetime import datetime
from os import listdir

import pandas as pd
import streamlit as st

from tennis_analysis_and_gambling.app.main_views import (
    surface_repartition_figure,
)
from tennis_analysis_and_gambling.cleaning import (
    clean_atp,
)
from tennis_analysis_and_gambling.config import ATP_FILES_DIR
from tennis_analysis_and_gambling.config import ATP_START_YEAR
from tennis_analysis_and_gambling.config import MAIN_ATP_COLS
from tennis_analysis_and_gambling.config import WTA_FILES_DIR
from tennis_analysis_and_gambling.utils import concat_history_files
from tennis_analysis_and_gambling.utils import fetch_history_file


current_year = datetime.now().year
atp_history_years = range(ATP_START_YEAR, current_year + 1)


def check_files_presence(year: int, atp_or_wta: str, update_current_year: bool) -> None:
    if atp_or_wta.lower() == "atp":
        data_dir = ATP_FILES_DIR
    elif atp_or_wta.lower() == "wta":
        data_dir = WTA_FILES_DIR
    else:
        raise ValueError(f"{atp_or_wta} not correct. Please select 'ATP' or 'WTA'")

    files_list = listdir(data_dir)
    if any(str(year) in filename for filename in files_list):
        pass
    else:
        fetch_history_file(year=year, atp_or_wta=atp_or_wta)

    # current year's file is updated each week
    if update_current_year:
        fetch_history_file(year=current_year, atp_or_wta=atp_or_wta)


def prepare_dataset(atp_or_wta: str) -> pd.DataFrame:
    history_df = concat_history_files(atp_or_wta=atp_or_wta)
    history_df = clean_atp(history_df)
    return history_df[MAIN_ATP_COLS].sort_values("Date").reset_index(drop=True)


def main(atp_or_wta: str, update_current_year: bool):
    for year in range(ATP_START_YEAR, current_year + 1):
        check_files_presence(
            year=year, atp_or_wta=atp_or_wta, update_current_year=update_current_year
        )
    df = prepare_dataset(atp_or_wta=atp_or_wta)
    st.dataframe(df)
    fig_surface_rep = surface_repartition_figure(df=df)
    st.plotly_chart(fig_surface_rep)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("circuit", help="Either ATP or WTA")
    parser.add_argument(
        "--update_current_year",
        action="store_true",
        help="Set this flag if you want to update the current year's results",
    )
    args = parser.parse_args()
    st.title(f"{args.circuit} HISTORY")
    with st.spinner(text="Reading history files..."):
        main(args.circuit, args.update_current_year)
