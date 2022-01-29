# coding: utf-8

from time import sleep
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = 'http://localhost:8501/'
try:
    with urlopen(URL):
        SERVER_RUNNING = True
except OSError:
    SERVER_RUNNING = False


@pytest.fixture
def driver():
    firefox_driver = webdriver.Firefox()
    yield firefox_driver

    # teardown
    firefox_driver.close()


@pytest.mark.skipif(not SERVER_RUNNING, reason='requires local server running')
def test_web_ui(driver):
    driver.get(URL)
    sleep(1)

    for button_label, expected_text in (
            ('Restartovat', '"Chodba"'),
            ('Jdi na sever', '"Pracovna"'),
            ('Otevři', 'Co mám otevřít?'),
            ('plechovku', 'V plechovce byl malý klíček.'),
            ('Vezmi', 'Co mám vzít?'),
            ('klíček', 'OK'),
            ('Jdi na jih', '"Chodba"'),
            ('Použij', 'Co mám použít?'),
            ('klíček', 'jak mám udělat'),
            ('Otevři', 'Co mám otevřít?'),
            ('dveře', 'Otevřel jsem dveře.'),
            ('Jdi na východ', '"Sklad"'),
            ('Jdi dolů', '"Sklep"'),
            ('Použij', 'Co mám použít?'),
            ('klíček', 'Odemkl jsem trezor.'),
            ('Otevři', 'Co mám otevřít?'),
            ('trezor', 'V trezoru jsem našel nůžky.'),
            ('Vezmi', 'Co mám vzít?'),
            ('nůžky', 'OK'),
            ('Jdi nahoru', '"Sklad"'),
            ('Jdi na západ', '"Chodba"'),
    ):
        button = driver.find_element(By.XPATH, f'//button[text()="{button_label}"]')
        button.click()
        sleep(0.25)
        assert expected_text in driver.page_source
