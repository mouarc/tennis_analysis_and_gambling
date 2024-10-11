#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from os import listdir
from os import makedirs
from os import path

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tennis_analysis_and_gambling.config import ATP_FILES_DIR
from tennis_analysis_and_gambling.config import ATP_START_YEAR
from tennis_analysis_and_gambling.config import FILES_XPATH
from tennis_analysis_and_gambling.config import URL_HISTORY_FILES
from tennis_analysis_and_gambling.config import WTA_FILES_DIR


def set_driver(url: str) -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver


def save_file_from_url(file_url: str, file_name: str):
    response = requests.get(file_url)
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"{file_name} downloaded")


def fetch_history_file(year: int, atp_or_wta: str) -> None:

    current_year = datetime.now().year
    atp_suffix = current_year - year + 1
    wta_suffix = atp_suffix + current_year - ATP_START_YEAR + 1

    if atp_or_wta.lower() == "atp":
        # xpath is built as follow: "/html/body/table[5]/tbody/tr[2]/td[3]/[_suffix_]"
        # ATP history files are from current year (suffix: 1) to 2000
        # WTA history files follow the last ATP history file
        # e.g.: if current year is 2027, 2027 ATP file' suffix will be 1,
        # 2000 ATP file' suffix will be 28
        # and 2027 WTA file' suffix wille be 29
        data_dir = ATP_FILES_DIR
        suffix = atp_suffix
    elif atp_or_wta.lower() == "wta":
        suffix = wta_suffix
        data_dir = WTA_FILES_DIR
    else:
        raise ValueError(f"{atp_or_wta} not correct. Please select 'ATP' or 'WTA'")

    if suffix < 1:
        raise FileNotFoundError(f"No file found for {atp_or_wta} {year}")

    driver = set_driver(url=URL_HISTORY_FILES)
    try:
        wait = WebDriverWait(driver, 3)
        dynamic_xpath = f"{FILES_XPATH}a[{suffix}]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, dynamic_xpath)))
        element_text = element.text

        if str(year) in element_text:
            file_url = element.get_attribute("href")
            if isinstance(file_url, str):
                file_name = path.join(data_dir, f"{atp_or_wta.lower()}_{file_url.split('/')[-1]}")
                makedirs(data_dir, exist_ok=True)
                save_file_from_url(file_url=file_url, file_name=file_name)
        else:
            raise FileNotFoundError(f"No file found for {atp_or_wta} {year}")
    finally:
        driver.quit()


def concat_history_files(atp_or_wta: str, files_path: str = None) -> pd.DataFrame:
    if not files_path:
        if atp_or_wta.lower() == "atp":
            files_path = ATP_FILES_DIR
        elif atp_or_wta.lower() == "wta":
            files_path = WTA_FILES_DIR
        else:
            raise ValueError(f"{atp_or_wta} not valid. Please select 'ATP' or 'WTA'.")
    history_files = listdir(files_path)
    df_history = pd.DataFrame()

    for file in history_files:
        if file.endswith(".xls") or file.endswith(".xlsx"):
            file_path = path.join(files_path, file)
            df_tmp = pd.read_excel(file_path)
            df_history = pd.concat([df_history, df_tmp])
    return df_history
