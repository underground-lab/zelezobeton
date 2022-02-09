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
            ('Jdi na sever', '"Kancelář"'),
            ('Otevři', 'Co mám otevřít?'),
            ('plechovku', 'dvě kancelářské sponky'),
            ('Restartovat', '"Chodba"'),
            ('Jdi na sever', '"Kancelář"'),
            ('Otevři', 'Co mám otevřít?'),
            ('plechovku', 'dvě kancelářské sponky'),
            ('Vezmi', 'Co mám vzít?'),
            ('sponky', 'OK'),
            ('Jdi na jih', '"Chodba"'),
            ('Použij', 'Co mám použít?'),
            ('sponky', 'jak mám udělat'),
            ('Otevři', 'Co mám otevřít?'),
            ('dveře', 'OK'),
            ('Jdi na východ', '"Sklad"'),
            ('Použij', 'Co mám použít?'),
            ('sponky', 'odemkl zámek mříže'),
            ('Otevři', 'Co mám otevřít?'),
            ('mříž', 'OK'),
            ('Vezmi', 'Co mám vzít?'),
            ('smeták', 'OK'),
            ('Jdi na západ', '"Chodba"'),
            ('Jdi na sever', '"Kancelář"'),
            ('Vezmi', 'Co mám vzít?'),
            ('vázu', 'Nedosáhnu'),
            ('Použij', 'Co mám použít?'),
            ('smeták', 'našel malý klíček'),
            ('Vezmi', 'Co mám vzít?'),
            ('klíček', 'OK'),
            ('Jdi na jih', '"Chodba"'),
            ('Jdi na východ', '"Sklad"'),
            ('Jdi na jih', '"Výklenek"'),
            ('Použij', 'Co mám použít?'),
            ('klíček', 'odemkl trezor'),
            ('Otevři', 'Co mám otevřít?'),
            ('trezor', 'našel obálku'),
            ('Vezmi', 'Co mám vzít?'),
            ('obálku', 'OK'),
    ):
        button = driver.find_element(By.XPATH, f'//button[text()="{button_label}"]')
        button.click()
        sleep(0.33)
        assert expected_text in driver.page_source
