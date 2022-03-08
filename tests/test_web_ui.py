# coding: utf-8

import os
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

URL = 'http://localhost:8000/'
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
    'button_id_prefix, paragraph_id, expected_text',
    (
        ('restart', 'room_description', '„Chodba“'),
        ('north', 'room_description', '„Kancelář“'),
        ('open', 'question', 'Co mám otevřít?'),
        ('plechovka', 'message', 'dvě kancelářské sponky'),

        # restart
        ('restart', 'room_description', '„Chodba“'),
        ('north', 'room_description', '„Kancelář“'),
        ('open', 'question', 'Co mám otevřít?'),
        ('plechovka', 'message', 'dvě kancelářské sponky'),
        ('take', 'question', 'Co mám vzít?'),
        ('sponky', 'message', 'OK'),
        ('south', 'room_description', '„Chodba“'),

        # use in a wrong room
        ('use', 'question', 'Co mám použít?'),
        ('sponky', 'message', 'Nevím jak.'),

        ('open', 'question', 'Co mám otevřít?'),
        ('dvere', 'message', 'OK'),
        ('east', 'room_description', '„Sklad“'),
        ('take', 'question', 'Co mám vzít?'),
        ('krabice', 'message', 'Jeden bude stačit'),
        ('use', 'question', 'Co mám použít?'),
        ('sponky', 'message', 'odemkl zámek mříže'),
        ('open', 'question', 'Co mám otevřít?'),
        ('mriz', 'message', 'OK'),
        ('take', 'question', 'Co mám vzít?'),
        ('smetak', 'message', 'OK'),
        ('west', 'room_description', '„Chodba“'),
        ('north', 'room_description', '„Kancelář“'),

        # take an unreachable object
        ('take', 'question', 'Co mám vzít?'),
        ('vaza', 'message', 'Nedosáhnu'),

        ('use', 'question', 'Co mám použít?'),
        ('smetak', 'message', 'našel malý klíček'),
        ('take', 'question', 'Co mám vzít?'),
        ('klicek', 'message', 'OK'),
        ('south', 'room_description', '„Chodba“'),
        ('east', 'room_description', '„Sklad“'),
        ('south', 'room_description', '„Výklenek“'),

        # open a locked object
        ('open', 'question', 'Co mám otevřít?'),
        ('trezor', 'message', 'Je zamčený'),

        ('use', 'question', 'Co mám použít?'),
        ('klicek', 'message', 'odemkl trezor'),
        ('open', 'question', 'Co mám otevřít?'),
        ('trezor', 'message', 'našel obálku'),
        ('take', 'question', 'Co mám vzít?'),
        ('obalka', 'message', 'OK'),
    )
)
def test_web_ui(driver, button_id_prefix, paragraph_id, expected_text):
    button = driver.find_element(By.ID, button_id_prefix + '_button')
    button.click()
    paragraph = driver.find_element(By.ID, paragraph_id)
    assert expected_text in paragraph.text
