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


@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.headless = HEADLESS
    firefox_driver = webdriver.Firefox(options=options)
    firefox_driver.implicitly_wait(5)
    firefox_driver.get(URL)
    yield firefox_driver

    # teardown
    firefox_driver.quit()


@pytest.mark.skipif(not SERVER_RUNNING, reason='requires local server running')
@pytest.mark.parametrize(
    'button_label, expected_text',
    (
        ('Restartovat', '„Chodba“'),
        ('Jdi na sever', '„Kancelář“'),
        ('Otevři', 'Co mám otevřít?'),
        ('plechovku', 'dvě kancelářské sponky'),

        # restart
        ('Restartovat', '„Chodba“'),
        ('Jdi na sever', '„Kancelář“'),
        ('Otevři', 'Co mám otevřít?'),
        ('plechovku', 'dvě kancelářské sponky'),
        ('Vezmi', 'Co mám vzít?'),
        ('sponky', 'OK'),
        ('Jdi na jih', '„Chodba“'),

        # use in a wrong room
        ('Použij', 'Co mám použít?'),
        ('sponky', 'Nevím jak.'),

        ('Otevři', 'Co mám otevřít?'),
        ('dveře', 'OK'),
        ('Jdi na východ', '„Sklad“'),
        ('Vezmi', 'Co mám vzít?'),
        ('krabici hřebíků', 'Jeden bude stačit'),
        ('Použij', 'Co mám použít?'),
        ('sponky', 'odemkl zámek mříže'),
        ('Otevři', 'Co mám otevřít?'),
        ('mříž', 'OK'),
        ('Vezmi', 'Co mám vzít?'),
        ('smeták', 'OK'),
        ('Jdi na západ', '„Chodba“'),
        ('Jdi na sever', '„Kancelář“'),

        # take an unreachable object
        ('Vezmi', 'Co mám vzít?'),
        ('vázu', 'Nedosáhnu'),

        ('Použij', 'Co mám použít?'),
        ('smeták', 'našel malý klíček'),
        ('Vezmi', 'Co mám vzít?'),
        ('klíček', 'OK'),
        ('Jdi na jih', '„Chodba“'),
        ('Jdi na východ', '„Sklad“'),
        ('Jdi na jih', '„Výklenek“'),

        # open a locked object
        ('Otevři', 'Co mám otevřít?'),
        ('trezor', 'Je zamčený'),

        ('Použij', 'Co mám použít?'),
        ('klíček', 'odemkl trezor'),
        ('Otevři', 'Co mám otevřít?'),
        ('trezor', 'našel obálku'),
        ('Vezmi', 'Co mám vzít?'),
        ('obálku', 'OK'),
    )
)
def test_web_ui(driver, button_label, expected_text):
    button = driver.find_element(By.XPATH, f'//button[text()="{button_label}"]')
    button.click()
    driver.find_element(By.XPATH, f"//*[contains(text(), '{expected_text}')]")
