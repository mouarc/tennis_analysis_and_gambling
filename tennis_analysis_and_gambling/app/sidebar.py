#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

import pandas as pd
import streamlit as st
from pandas.api.types import is_categorical_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_object_dtype

from tennis_analysis_and_gambling.utils import fetch_history_file

current_year = datetime.now().year


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI in the sidebar to let viewers filter columns
    Inspired by https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    with st.sidebar:
        with st.container(border=True):
            modify = st.checkbox("Add filters", key=1)

            if not modify:
                return df

            filtered_df = df.copy()

            # Try to convert datetimes into a standard format (datetime, no timezone)
            for col in filtered_df.columns:
                if is_object_dtype(filtered_df[col]):
                    try:
                        filtered_df[col] = pd.to_datetime(filtered_df[col])
                    except Exception:
                        pass

                if is_datetime64_any_dtype(filtered_df[col]):
                    filtered_df[col] = filtered_df[col].dt.tz_localize(None)

            modification_container = st.container()

            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", filtered_df.columns)
                for column in to_filter_columns:
                    left, right = st.columns((1, 20))
                    # Treat columns with < 10 unique values as categorical
                    if (
                        is_categorical_dtype(filtered_df[column])
                        or filtered_df[column].nunique() < 10
                    ):
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            filtered_df[column].unique(),
                            default=list(filtered_df[column].unique()),
                        )
                        filtered_df = filtered_df[filtered_df[column].isin(user_cat_input)]
                    elif is_numeric_dtype(filtered_df[column]):
                        _min = float(filtered_df[column].min())
                        _max = float(filtered_df[column].max())
                        step = (_max - _min) / 100
                        user_num_input = right.slider(
                            f"Values for {column}",
                            min_value=_min,
                            max_value=_max,
                            value=(_min, _max),
                            step=step,
                        )
                        filtered_df = filtered_df[filtered_df[column].between(*user_num_input)]
                    elif is_datetime64_any_dtype(filtered_df[column]):
                        user_date_input = right.date_input(
                            f"Values for {column}",
                            value=(
                                filtered_df[column].min(),
                                filtered_df[column].max(),
                            ),
                        )
                        if len(user_date_input) == 2:
                            user_date_input = tuple(map(pd.to_datetime, user_date_input))
                            start_date, end_date = user_date_input
                            filtered_df = filtered_df.loc[
                                filtered_df[column].between(start_date, end_date)
                            ]
                    else:
                        user_text_input = right.text_input(
                            f"Substring or regex in {column}",
                        )
                        if user_text_input:
                            filtered_df = filtered_df[
                                filtered_df[column].astype(str).str.contains(user_text_input)
                            ]

                if st.button("Reset filters", key="reset_filters"):
                    filtered_df = df

            return filtered_df


def update_history():
    with st.sidebar:
        st.button(
            "Update history",
            key="update",
            on_click=fetch_history_file,
            args=(current_year, "atp"),
        )


def sidebar():
    update_history()
    st.session_state["history"] = filter_dataframe(st.session_state["history"])
