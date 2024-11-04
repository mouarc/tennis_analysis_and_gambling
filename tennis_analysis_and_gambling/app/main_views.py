#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px

from tennis_analysis_and_gambling.app.config import COLORS_MAPPING


def surface_repartition_figure(df: pd.DataFrame):
    df["Year"] = pd.to_datetime(df["Date"]).dt.year
    df_grouped = df.groupby(["Year", "Surface"]).size().reset_index(name="Match Count")
    fig = px.bar(
        df_grouped,
        x="Year",
        y="Match Count",
        color="Surface",
        color_discrete_map=COLORS_MAPPING,
        barmode="group",
        title="Number of matches per surface per year",
    )
    return fig
