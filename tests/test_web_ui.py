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
    'id_to_click, id_to_read, expected_text',
    (
        ('restart_button', 'room_description', '„Chodba“'),
        ('north_button', 'room_description', '„Kancelář“'),
        ('open_button', 'question', 'Co mám otevřít?'),
        ('plechovka_button', 'message', 'jen dvě kancelářské sponky'),
        ('take_button', 'question', 'Co mám vzít?'),

        # cancel object selection
        ('back_home', 'room_description', '„Kancelář“'),
        ('take_button', 'question', 'Co mám vzít?'),
        ('sponky_button', 'message', 'OK'),
        ('south_button', 'room_description', '„Chodba“'),
        ('open_button', 'question', 'Co mám otevřít?'),
        ('dvere_button', 'message', 'OK'),

        # restart
        ('restart_button', 'room_description', '„Chodba“'),
        ('north_button', 'room_description', '„Kancelář“'),
        ('take_button', 'question', 'Co mám vzít?'),
        ('plechovka_button', 'message', 'OK'),
        ('south_button', 'room_description', '„Chodba“'),
        ('open_button', 'question', 'Co mám otevřít?'),
        ('plechovka_button', 'message', 'našel dvě kancelářské sponky'),

        # use in a wrong room
        ('use_button', 'question', 'Co mám použít?'),
        ('sponky_button', 'message', 'Nevím jak.'),

        ('open_button', 'question', 'Co mám otevřít?'),
        ('dvere_button', 'message', 'OK'),
        ('east_button', 'room_description', '„Sklad“'),
        ('use_button', 'question', 'Co mám použít?'),
        ('sponky_button', 'message', 'odemkl zámek mříže'),
        ('take_button', 'question', 'Co mám vzít?'),

        # cancel object selection
        ('back_home', 'room_description', '„Sklad“'),
        ('open_button', 'question', 'Co mám otevřít?'),
        ('mriz_button', 'message', 'OK'),
    )
)
def test_web_ui(driver, id_to_click, id_to_read, expected_text):
    element_to_click = driver.find_element(By.ID, id_to_click)
    element_to_click.click()
    element_to_read = driver.find_element(By.ID, id_to_read)
    assert expected_text in element_to_read.text
