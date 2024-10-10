from datetime import datetime
from datetime import timedelta

URL_HISTORY_FILES = "http://www.tennis-data.co.uk/alldata.php"
FILES_XPATH = "/html/body/table[5]/tbody/tr[2]/td[3]/"
ATP_FILES_DIR = "data/external/atp"
WTA_FILES_DIR = "data/external/wta"
FILES_DIR = "data/"

FORMAT_DATE = "%Y-%m-%d"
TODAY = datetime.now()
TOMORROW = TODAY + timedelta(days=1)
