from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture(scope="function")
def driver():
    """
    Инициализация WebDriver для Chrome.
    Настраивает неявное ожидание 10 секунд.
    После теста драйвер автоматически закрывается.
    """
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@allure.story("Поиск фильма на сайте")
@pytest.mark.ui
def test_search_russian_word(driver):
    driver.get("https://www.kinopoisk.ru/")
    driver.find_element(By.NAME, "kp_query").send_keys("Мой папа - медведь")
    assert driver.find_element(By.ID, "suggest-item-film-6561460")


@pytest.mark.ui
def test_hover_menu(driver):
    driver.get("https://www.kinopoisk.ru/")

    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)


    menu_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'svg[width="24"][data-tid="ada90870"]')
        )
    )
    actions.move_to_element(menu_button).perform()

    dropdown = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            'div.styles_dropdown__pB0b8.styles_openedDropdown__SXWF8.styles_dropdownDefault__r8tyV'
        ))
    )

    assert dropdown.is_displayed(), "Выпадающее меню не открылось при наведении"


@pytest.mark.ui
def test_hover_menu_serials(driver):
    driver.get("https://www.kinopoisk.ru/")

    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    # Наводим на кнопку меню
    menu_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'svg[width="24"][data-tid="ada90870"]')
        )
    )
    actions.move_to_element(menu_button).perform()
    # Ждем выпадающее меню
    dropdown = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            'div.styles_dropdown__pB0b8.styles_openedDropdown__SXWF8.styles_dropdownDefault__r8tyV'
        ))
    )

    # Кликаем по пункту "Сериалы" в меню
    serials_element = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'a.styles_root__i41Qt.styles_darkThemeItem__P_q_d[href="/lists/categories/movies/3/"][data-tid="de7c6530"]'
        ))
    )
    serials_element.click()

    # На новой странице появляется нужный заголовок
    series_header = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//span[contains(@class,'styles_name__7luvu') and contains(text(), 'Все сериалы онлайн')]"
        ))
    )
    assert series_header.is_displayed()


@pytest.mark.ui
def test_click_coon_in_cinema(driver):
    driver.get("https://www.kinopoisk.ru/")

    wait = WebDriverWait(driver, 15)

    #Ждём появления "Скоро в кино"
    soon_link = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'a.styles_link__I3GY8[data-tid="6a319a9e"][href="/premiere/"]'
        ))
    )
    # Прокручиваем страницу до элемента
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", soon_link)

    # Опционально: подождать, пока элемент станет кликабельным
    soon_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'a.styles_link__I3GY8[data-tid="6a319a9e"][href="/premiere/"]'
        ))
    )

    # Кликаем по ссылке
    soon_link.click()


def test_click_arrow_top10_month(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 15)

    # Ждем появление секции "Топ-10 за месяц" по data-tid
    section = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'section[data-tid="c7537407"]'
        ))
    )

    # Прокручиваем страницу до этого раздела
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", section)

    # Ждем появления стрелочки в разделе (уточните селектор по классу стрелочки)
    arrow = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'span.styles_iconRightDir__25yKt.styles_icon__CyA3t'
        ))
    )

    # Кликаем по стрелочке
    arrow.click()