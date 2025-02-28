import time

import pytest
from pytest import fixture
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pytestflow.webdriver_factory import WebDriverFactory

@pytest.fixture(scope="session", autouse=True)
def driver():
    """

    """
    driver_factory = WebDriverFactory(browser="chrome")
    driver = driver_factory.get_webdriver()
    yield driver
    driver_factory.quit_webdriver()


@pytest.mark.test_one
def test_launch(driver):

    driver.implicitly_wait(10)
    driver.get("https://www.youtube.com")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("cheap thrill")
    search_box.send_keys(Keys.RETURN)
    first_video = driver.find_element(By.XPATH, '(//a[@id="video-title"])[1]')
    first_video.click()
    time.sleep(60) # relax for one minute