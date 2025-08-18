import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


@allure.story("Поиск фильма на сайте")
@pytest.mark.ui
@pytest.mark.parametrize("movie_name, suggestion_id", [
    ("Мой папа - медведь", "suggest-item-film-6561460"),
    ("Титаник", "suggest-item-film-2213"),
    ("Укради мою мечту", "suggest-item-film-6215379"),
])
def test_search_movie_by_title(driver, movie_name, suggestion_id):
    driver.get("https://www.kinopoisk.ru/")

    with allure.step(f"Вводим название фильма '{movie_name}' в поле поиска"):
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.clear()
        search_input.send_keys(movie_name)

    with allure.step("Ожидаем появления подсказки с фильмом"):
        wait = WebDriverWait(driver, 10)
        suggestion = wait.until(
            EC.visibility_of_element_located((By.ID, suggestion_id))
        )
        assert suggestion.is_displayed(), f"Подсказка фильма '{movie_name}' не отображается"


@pytest.mark.ui
def test_hover_menu(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)

    with allure.step("Ждем появления кнопки меню и наводим курсор"):
        menu_button = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'svg[width="24"][data-tid="ada90870"]')
            )
        )
        actions.move_to_element(menu_button).perform()

    with allure.step("Ждем появления выпадающего меню"):
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
@allure.story("Переход к разделу 'Скоро в кино'")
def test_click_coon_in_cinema(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 15)

    with allure.step('Ждем появления ссылки "Скоро в кино"'):
        soon_link = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'a.styles_link__I3GY8[data-tid="6a319a9e"][href="/premiere/"]'
            ))
        )

    with allure.step("Прокручиваем страницу до элемента"):
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", soon_link
        )

    with allure.step("Ждем пока элемент станет кликабельным и кликаем"):
        soon_link = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'a.styles_link__I3GY8[data-tid="6a319a9e"][href="/premiere/"]'
            ))
        )
        soon_link.click()

    with allure.step("Ожидаем появления заголовка графика кинопремьер с классом 'main_title_prem'"):
        expected_header = wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '.main_title_prem'
            ))
        )
        assert expected_header.is_displayed(), "Заголовок графика кинопремьер не отображается"


@allure.story("Взаимодействие с элементами топ-10 месяца")
@pytest.mark.ui
def test_click_arrow_top10_month(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 15)

    with allure.step('Ждем появление секции "Топ-10 за месяц" по data-tid'):
        section = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'section[data-tid="c7537407"]'
            ))
        )

    with allure.step("Прокручиваем страницу до раздела 'Топ-10 за месяц'"):
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", section)

    with allure.step("Ждем появления и кликаем по стрелочке в разделе"):
        arrow = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'span.styles_iconRightDir__25yKt.styles_icon__CyA3t'
            ))
        )
        assert arrow.is_displayed(), "Стрелочка для пролистывания не видна"
        arrow.click()