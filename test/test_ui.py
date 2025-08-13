from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.fixture()
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(50)
    yield driver
    driver.quit()


def test_search_russian_word(driver):
    driver.get("https://www.kinopoisk.ru/")
    driver.find_element(By.NAME, "kp_query").send_keys("Мой папа-медведь")
    assert driver.find_element(By.ID, "suggest-item-film-6561460")

