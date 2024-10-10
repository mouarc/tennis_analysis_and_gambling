#!/usr/bin/env python3
# coding: utf-8
import unittest
from os import path
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.webdriver import WebDriver

from tennis_analysis_and_gambling.config import ATP_FILES_DIR
from tennis_analysis_and_gambling.config import URL_HISTORY_FILES
from tennis_analysis_and_gambling.utils import fetch_history_file
from tennis_analysis_and_gambling.utils import save_file_from_url
from tennis_analysis_and_gambling.utils import set_driver


class TestUtils(unittest.TestCase):

    def test_set_driver(self):
        driver = set_driver(url=URL_HISTORY_FILES)
        self.assertEqual(type(driver), WebDriver)
        self.assertEqual(driver.current_url, URL_HISTORY_FILES)

    def test_set_driver_fail(self):
        with self.assertRaises(InvalidArgumentException):
            set_driver(url="fake_url")

    @patch("builtins.open", new_callable=mock_open)
    @patch("requests.get")
    def test_save_file_from_url(self, mock_get, mock_file):
        mock_response = MagicMock()
        mock_response.content = b"file content"
        mock_get.return_value = mock_response

        file_url = "http://example.com/testfile"
        file_name = "testfile.txt"
        save_file_from_url(file_url, file_name)
        mock_get.assert_called_once_with(file_url)
        mock_file.assert_called_once_with(file_name, "wb")
        mock_file().write.assert_called_once_with(b"file content")

    def test_fetch_history_file_fail_on_atp_wta(self):
        with self.assertRaises(ValueError):
            fetch_history_file(0, "wrong_atp_wta")

    def test_fetch_history_file_fail_on_year(self):
        with self.assertRaises(FileNotFoundError):
            fetch_history_file(99999, "atp")

    @patch("tennis_analysis_and_gambling.utils.makedirs")
    @patch("tennis_analysis_and_gambling.utils.save_file_from_url")
    @patch("selenium.webdriver.support.ui.WebDriverWait")
    def test_fetch_history_file_atp(self, mock_wait, mock_save_file, mock_makedirs):
        year = 2023
        mock_element = MagicMock()
        mock_element.text = f"{year}"
        mock_element.get_attribute.return_value = "2023/2023.xlsx"
        mock_wait.return_value.until.return_value = mock_element

        atp_or_wta = "atp"
        fetch_history_file(year, atp_or_wta)

        expected_file_name = path.join(ATP_FILES_DIR, f"{atp_or_wta}_2023.xlsx")
        mock_save_file.assert_called_once_with(
            file_url="http://www.tennis-data.co.uk/2023/2023.xlsx", file_name=expected_file_name
        )
        mock_makedirs.assert_called_once_with(ATP_FILES_DIR, exist_ok=True)
        self.assertTrue("2023.xlsx" in mock_element.get_attribute.return_value)
