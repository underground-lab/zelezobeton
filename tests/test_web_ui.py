# coding: utf-8

import os
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

URL = 'http://localhost:8501/'
HEADLESS = not os.getenv('NO_HEADLESS')
try:
    with urlopen(URL):
        SERVER_RUNNING = True
except OSError:
    SERVER_RUNNING = False


@pytest.fixture
def driver():
    options = Options()
    options.headless = HEADLESS
    firefox_driver = webdriver.Firefox(options=options)
    firefox_driver.implicitly_wait(5)
    yield firefox_driver

    # teardown
    firefox_driver.close()


@pytest.mark.skipif(not SERVER_RUNNING, reason='requires local server running')
def test_web_ui(driver):
    driver.get(URL)

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
            ('sponky', 'Nevím jak.'),
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
        driver.find_element(By.XPATH, f"//*[contains(text(), '{expected_text}')]")
