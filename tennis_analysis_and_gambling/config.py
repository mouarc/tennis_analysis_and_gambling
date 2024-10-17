from datetime import datetime
from datetime import timedelta

URL_HISTORY_FILES = "http://www.tennis-data.co.uk/alldata.php"
FILES_XPATH = "/html/body/table[5]/tbody/tr[2]/td[3]/"
ATP_FILES_DIR = "data/external/atp"
WTA_FILES_DIR = "data/external/wta"
ATP_START_YEAR = 2000
FILES_DIR = "data/"

FORMAT_DATE = "%Y-%m-%d"
TODAY = datetime.now()
TOMORROW = TODAY + timedelta(days=1)

ATP_SERIES_TO_RENAME = {
    "International Gold": "ATP500",
    "Masters": "Masters 1000",
    "International": "ATP250",
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
