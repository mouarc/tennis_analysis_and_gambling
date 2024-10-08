#!/usr/bin/env python3
# coding: utf-8

import unittest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import InvalidArgumentException

from tennis_analysis_and_gambling.utils import (
    set_driver,
)
from tennis_analysis_and_gambling.config import (
    URL_HISTORY_ATP_FILES,
)

class TestUtils(unittest.TestCase):

    def test_set_driver(self):
        driver = set_driver(url=URL_HISTORY_ATP_FILES)
        self.assertEqual(type(driver), WebDriver)
        self.assertEqual(driver.current_url, URL_HISTORY_ATP_FILES)

    def test_set_driver_fail(self):
        with self.assertRaises(InvalidArgumentException):
            set_driver(url="fake_url")
