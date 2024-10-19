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
    """
    Configures and launches a Chrome WebDriver with specific options to open a given URL.

    Args:
        url (str): The URL that the browser will navigate to after launching the driver.

    Returns:
        WebDriver: A configured instance of the Chrome WebDriver.

    The driver is launched with the following options:
        - "--no-sandbox": Disables the use of the sandbox, commonly used in environments without a user interface.
        - "--headless": Runs the browser in headless mode (without a graphical interface), useful for server environments.
        - "--remote-debugging-port=9222": Opens a port for remote debugging.
        - "--disable-gpu": Disables GPU usage, useful in environments without GPU access.
    """
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
    """
    Downloads and saves an ATP or WTA tennis match history file (in XLS format) for a specified year from
    http://www.tennis-data.co.uk/alldata.php.

    Args:
        year (int): The year for which you want to download the history file
        atp_or_wta (str): Either "ATP" for men's tennis matches or "WTA" for women's tennis matches

    Raises:
        ValueError: If the atp_or_wta argument is not correctly set to "ATP" or "WTA".
        FileNotFoundError: If the file is not found. This can happen if the specified year does not exist
        in the history files available on the website.
    """

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
    """
    Concatenates all ATP or WTA history files from a specified directory into a single DataFrame.

    Args:
        atp_or_wta (str): Specifies whether to concatenate ATP or WTA files. Must be either "ATP" for men's tennis matches
                          or "WTA" for women's tennis matches.
        files_path (str, optional): The path to the directory containing the history files. Defaults to None,
                                    in which case the function will use ATP_FILES_DIR for ATP or WTA_FILES_DIR for WTA.

    Raises:
        ValueError: If atp_or_wta is not "ATP" or "WTA", a ValueError is raised.

    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from all ATP or WTA history files.

    Notes:
        - The function scans the specified directory for files with the ".xls" or ".xlsx" extensions.
        - It reads each file into a temporary DataFrame using `pd.read_excel()` and concatenates them into a single DataFrame.
        - If `files_path` is not provided, the function defaults to predefined directories for ATP or WTA data.
    """
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
