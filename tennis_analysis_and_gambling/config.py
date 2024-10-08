from datetime import datetime, timedelta

URL_HISTORY_ATP_FILES = "http://www.tennis-data.co.uk/alldata.php"
ATP_FILE_XPATH = "/html/body/table[5]/tbody/tr[2]/td[3]/"
ATP_FILES_DIR = "data/external/atp"
FILES_DIR = "data/"

FORMAT_DATE = "%Y-%m-%d"
TODAY = datetime.now()
TOMORROW = TODAY + timedelta(days=1)
