#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st

# % matchs gagnés favori
# % matchs gagnés vs rank inf
# nb games moyen
# pourcentage de matchs gagnés après avoir gagné le 1er set
# pourcentage de matchs gagnés après avoir perdu le 1er set
# pourcentage de matchs gagnés sans que l'adversaire ne gagne de set (victoire 2 ou 3-0 divisé par nb victoires)


def individual_stats(df: pd.DataFrame, player: str):
    individual_stats = {}
    player_df = df[(df["Winner"] == player) | (df["Loser"] == player)]
    victory_df = df[df["Winner"] == player]
    surfaces = player_df["Surface"].unique()
    rounds = player_df["Round"].unique()
    individual_stats["total_victory_percentage"] = len(
        player_df[player_df["Winner"] == player]
    ) / len(player_df)

    for surface in surfaces:
        surface_df = player_df[player_df["Surface"] == surface]
        individual_stats[surface.lower()] = len(surface_df[surface_df["Winner"] == player]) / len(
            surface_df
        )

    for round in rounds:
        round_df = player_df[player_df["Round"] == round]
        individual_stats[round.lower()] = len(round_df[round_df["Winner"] == player]) / len(
            round_df
        )

    player_is_favorite_df = player_df[
        ((player_df["Winner"] == player) & (player_df["B365W"] < player_df["B365L"]))
        | ((player_df["Loser"] == player) & (player_df["B365W"] > player_df["B365L"]))
    ]
    individual_stats["total_victory_percentage_as_favorite"] = len(
        player_df[(player_df["Winner"] == player) & (player_df["B365W"] < player_df["B365L"])]
    ) / len(player_is_favorite_df)

    player_is_not_favorite = player_df[
        ((player_df["Winner"] == player) & (player_df["B365W"] > player_df["B365L"]))
        | ((player_df["Loser"] == player) & (player_df["B365W"] < player_df["B365L"]))
    ]
    individual_stats["total_victory_percentage_as_not_favorite"] = len(
        player_df[(player_df["Winner"] == player) & (player_df["B365W"] > player_df["B365L"])]
    ) / len(player_is_not_favorite)

    individual_stats["victory_percentage_after_losing_1st_set"] = len(
        victory_df[victory_df["L1"] > victory_df["W1"]]
    ) / len(victory_df)

    # # Fonction interne pour calculer un pourcentage de victoire
    # def calculate_win_percentage(condition):
    #     win_count = player_df[(player_df["Winner"] == player) & condition].shape[0]
    #     total_count = player_df[condition].shape[0]
    #     return win_count / total_count if total_count > 0 else 0

    # # Pourcentage de victoires par surface
    # surfaces = player_df["Surface"].unique()
    # victory_percentage_by_surface = {
    #     surface: calculate_win_percentage(player_df["Surface"] == surface)
    #     for surface in surfaces
    # }
    # individual_stats["victory_percentage_by_surface"] = victory_percentage_by_surface

    # # Pourcentage de victoires par tour
    # rounds = player_df["Round"].unique()
    # victory_percentage_by_round = {
    #     round_: calculate_win_percentage(player_df["Round"] == round_)
    #     for round_ in rounds
    # }
    # individual_stats["victory_percentage_by_round"] = victory_percentage_by_round

    # Pourcentage de victoires en tant que favori
    # individual_stats["favorite_win_percentage"] = calculate_win_percentage(player_df["Favorite"] == player)

    # Pourcentage de victoires contre un adversaire de rang inférieur
    # individual_stats["win_percentage_vs_lower_rank"] = calculate_win_percentage(player_df["OpponentRank"] > player_df["PlayerRank"])

    # Nombre moyen de jeux
    # individual_stats["avg_games"] = player_df["Games"].mean()

    # Pourcentage de victoires après avoir gagné le 1er set
    # individual_stats["win_percentage_after_winning_first_set"] = calculate_win_percentage(player_df["FirstSetWinner"] == player)

    # Pourcentage de victoires après avoir perdu le 1er set
    # individual_stats["win_percentage_after_losing_first_set"] = calculate_win_percentage(player_df["FirstSetWinner"] != player)

    # Pourcentage de victoires sans que l'adversaire ne gagne de set
    # individual_stats["straight_set_win_percentage"] = calculate_win_percentage(player_df["SetsWon"] == 2)

    return individual_stats


# col_player1, statistics, col_player2 = st.columns(3)
col_player1, col_player2 = st.columns(2)

with col_player1:
    player1 = st.selectbox("Select your player :", st.session_state["players"], key="player1")
    if player1:
        statistics_player1 = individual_stats(st.session_state["history"], player=player1)
        st.write(statistics_player1)

with col_player2:
    player2 = st.selectbox("Select your player :", st.session_state["players"], key="player2")

    if player2:
        statistics_player2 = individual_stats(st.session_state["history"], player=player2)
        st.write(statistics_player2)
