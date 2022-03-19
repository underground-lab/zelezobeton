# coding: utf-8

import os
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
def driver():
    options = Options()
    options.headless = HEADLESS
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
        condition = staleness_of(driver.find_element(By.ID, 'message'))

        actions = ActionChains(driver).move_to_element(dropdown).click(button)
        wait = WebDriverWait(driver, 5)

        actions.perform()
        wait.until(condition)

    driver.find_element(By.ID, 'restart_button').click()
    assert 'Chodba' in driver.find_element(By.ID, 'room_description').text
    assert 'dveře' in driver.find_element(By.ID, 'in_room').text
    assert 'minci' in driver.find_element(By.ID, 'in_inventory').text

    driver.find_element(By.ID, 'north_button').click()
    assert 'Kancelář' in driver.find_element(By.ID, 'room_description').text
    assert 'plechovku' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('open', 'plechovka')
    assert 'jen dvě kancelářské sponky' in driver.find_element(By.ID, 'message').text
    assert 'sponky' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('take', 'sponky')
    assert 'OK' in driver.find_element(By.ID, 'message').text
    assert 'sponky' in driver.find_element(By.ID, 'in_inventory').text

    driver.find_element(By.ID, 'restart_button').click()
    assert 'Chodba' in driver.find_element(By.ID, 'room_description').text
    assert 'sponky' not in driver.find_element(By.ID, 'in_inventory').text

    perform_and_wait('open', 'dvere')
    assert 'OK' in driver.find_element(By.ID, 'message').text

    driver.find_element(By.ID, 'east_button').click()
    assert 'Sklad' in driver.find_element(By.ID, 'room_description').text
    assert 'krabici hřebíků' in driver.find_element(By.ID, 'in_room').text

    perform_and_wait('take', 'krabice')
    assert 'Jeden bude stačit' in driver.find_element(By.ID, 'message').text
    assert 'krabici hřebíků' in driver.find_element(By.ID, 'in_room').text
    assert 'hřebík' in driver.find_element(By.ID, 'in_inventory').text
