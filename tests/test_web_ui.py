# coding: utf-8

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

import pytest
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

URL = 'http://localhost:8000/'
HEADLESS = not os.getenv('NO_HEADLESS')
try:
    with urlopen(URL):
        SERVER_RUNNING = True
except OSError:
    SERVER_RUNNING = False


@pytest.fixture
def temp_dir():
    tests_dir = Path(__file__).parent
    with TemporaryDirectory(dir=tests_dir) as temp:
        yield temp


@pytest.fixture
def driver(temp_dir):
    os.environ['TMPDIR'] = temp_dir
    options = Options()
    if HEADLESS:
        options.add_argument('-headless')
    firefox_driver = Firefox(options=options)
    firefox_driver.implicitly_wait(5)
    firefox_driver.get(URL)
    yield firefox_driver

    # teardown
    firefox_driver.quit()


@pytest.mark.skipif(not SERVER_RUNNING, reason='requires local server running')
def test_web_ui(driver):

    def perform_and_wait(action, obj):
        dropdown = driver.find_element(By.ID, f'{action}_dropdown')
        button = driver.find_element(By.ID, f'{action}_{obj}_button')
        condition = staleness_of(driver.find_element(By.ID, 'room_description'))

        actions = ActionChains(driver).move_to_element(dropdown).click(button)
        wait = WebDriverWait(driver, 5)

        actions.perform()
        wait.until(condition)

    assert driver.title == 'Železo, beton'

    # start a new game
    driver.find_element(By.ID, 'new_game').click()
    assert driver.title == 'Železo, beton'
    assert 'Chodba' in driver.find_element(By.ID, 'room_description').text
    assert driver.find_element(By.ID, 'open_dropdown')
    assert 'dveře' in driver.find_element(By.ID, 'in_room').text
    assert 'minci' in driver.find_element(By.ID, 'in_inventory').text

    perform_and_wait('go', 'north')
    assert 'Kancelář' in driver.find_element(By.ID, 'room_description').text
    assert 'plechovku' in driver.find_element(By.ID, 'in_room').text
    assert driver.find_element(By.ID, 'open_dropdown')

    perform_and_wait('open', 'plechovka')
    assert 'jen dvě kancelářské sponky' in driver.find_element(By.ID, 'message').text
    assert 'sponky' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('take', 'sponky')
    assert 'OK' in driver.find_element(By.ID, 'message').text
    assert 'sponky' in driver.find_element(By.ID, 'in_inventory').text
    assert driver.find_element(By.ID, 'use_dropdown')

    # go to homepage
    driver.find_element(By.ID, 'home').click()

    # continue game
    driver.find_element(By.ID, 'continue_game').click()
    assert 'Kancelář' in driver.find_element(By.ID, 'room_description').text
    assert 'sponky' in driver.find_element(By.ID, 'in_inventory').text

    perform_and_wait('go', 'south')
    assert 'Chodba' in driver.find_element(By.ID, 'room_description').text

    perform_and_wait('open', 'dvere')
    assert 'OK' in driver.find_element(By.ID, 'message').text

    perform_and_wait('go', 'east')
    assert 'Sklad' in driver.find_element(By.ID, 'room_description').text
    assert 'smeták' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('take', 'smetak')
    assert 'OK' in driver.find_element(By.ID, 'message').text
    assert 'smeták' in driver.find_element(By.ID, 'in_inventory').text

    # go to homepage
    driver.find_element(By.ID, 'home').click()

    # start a new game
    driver.find_element(By.ID, 'new_game').click()
    assert 'Chodba' in driver.find_element(By.ID, 'room_description').text
    assert driver.find_element(By.ID, 'open_dropdown')
    assert 'sponky' not in driver.find_element(By.ID, 'in_inventory').text
    assert 'smeták' not in driver.find_element(By.ID, 'in_inventory').text

    perform_and_wait('open', 'dvere')
    assert 'OK' in driver.find_element(By.ID, 'message').text

    perform_and_wait('go', 'east')
    assert 'Sklad' in driver.find_element(By.ID, 'room_description').text
    assert 'smeták' in driver.find_element(By.ID, 'in_room').text
    assert 'krabici hřebíků' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('take', 'krabice')
    assert 'Jeden bude stačit' in driver.find_element(By.ID, 'message').text
    assert 'krabici hřebíků' in driver.find_element(By.ID, 'in_room').text
    assert 'hřebík' in driver.find_element(By.ID, 'in_inventory').text
