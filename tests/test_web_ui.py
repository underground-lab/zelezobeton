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
            ('Restartovat', 'Popis místnosti 0.'),
            ('Jdi na sever', 'Popis místnosti 1.'),
            ('Otevři', 'Co chceš otevřít?'),
            ('plechovku', 'V plechovce byl malý klíček.'),
            ('Vezmi', 'Co chceš vzít?'),
            ('klíček', 'OK'),
            ('Použij', 'Co chceš použít?'),
            ('klíček', 'To nelze.'),
            ('Jdi na jih', 'Popis místnosti 0.'),
            ('Použij', 'Co chceš použít?'),
            ('klíček', 'Odemkl jsi dveře.'),
            ('Otevři', 'Co chceš otevřít?'),
            ('dveře', 'Otevřel jsi dveře.'),
            ('Jdi na východ', 'Popis místnosti 2.'),
            ('Jdi dolů', 'Popis místnosti 3.'),
            ('Otevři', 'Co chceš otevřít?'),
            ('skříňku', 'Ve skříňce jsi našel nůžky.'),
            ('Vezmi', 'Co chceš vzít?'),
            ('nůžky', 'OK'),
    ):
        button = driver.find_element(By.XPATH, f'//button[text()="{button_label}"]')
        button.click()
        sleep(0.25)
        assert expected_text in driver.page_source
