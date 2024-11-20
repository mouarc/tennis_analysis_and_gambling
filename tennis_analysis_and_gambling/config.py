from datetime import datetime
from datetime import timedelta

URL_HISTORY_FILES = "http://www.tennis-data.co.uk/alldata.php"
FILES_XPATH = "/html/body/table[5]/tbody/tr[2]/td[3]/"
ATP_FILES_DIR = "data/external/atp"
WTA_FILES_DIR = "data/external/wta"
ATP_START_YEAR = 2000
WTA_START_YEAR = 2007
FILES_DIR = "data/"

FORMAT_DATE = "%Y-%m-%d"
TODAY = datetime.now()
TOMORROW = TODAY + timedelta(days=1)

ATP_SERIES_TO_RENAME = {
    "International Gold": "ATP500",
    "Masters": "Masters 1000",
    "International": "ATP250",
}

WTA_SERIES_TO_RENAME = {
    "International": "WTA250",
    "Premier": "WTA500",
    "Tier 3": "WTA250",
    "Tier 4": "WTA250",
    "Tier 1": "WTA1000",
    "Tier 2": "WTA500",
    "Tour Championships": "WTA Finals",
    "Grand Slam": "WTA Grand Slam",
}

NUMERIC_COLS = [
    "W1",
    "L1",
    "W2",
    "L2",
    "W3",
    "L3",
    "W4",
    "L4",
    "W5",
    "L5",
    "Wsets",
    "Lsets",
    "WRank",
    "LRank",
]

RANK_COLS = [
    "WRank",
    "LRank",
]

ATP_SCORE_COLS = [
    "W1",
    "L1",
    "W2",
    "L2",
    "W3",
    "L3",
    "W4",
    "L4",
    "W5",
    "L5",
]

WTA_SCORE_COLS = [
    "W1",
    "L1",
    "W2",
    "L2",
    "W3",
    "L3",
]

SETS_COLS = [
    "Wsets",
    "Lsets",
]

ODDS_COLS = [
    "B365W",
    "B365L",
]

RANK_COLS = [
    "WRank",
    "LRank",
]

MAIN_ATP_COLS = [
    "Date",
    "Location",
    "Tournament",
    "Series",
    "Court",
    "Surface",
    "Round",
    "Best of",
    "Winner",
    "Loser",
    "WRank",
    "LRank",
    "W1",
    "L1",
    "W2",
    "L2",
    "W3",
    "L3",
    "W4",
    "L4",
    "W5",
    "L5",
    "Wsets",
    "Lsets",
    "B365W",
    "B365L",
]

MAIN_WTA_COLS = [
    "Date",
    "Location",
    "Tournament",
    "Tier",
    "Court",
    "Surface",
    "Round",
    "Best of",
    "Winner",
    "Loser",
    "WRank",
    "LRank",
    "W1",
    "L1",
    "W2",
    "L2",
    "W3",
    "L3",
    "Wsets",
    "Lsets",
    "B365W",
    "B365L",
]
