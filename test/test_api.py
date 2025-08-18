import pytest
import requests
import allure
import os
from dotenv import load_dotenv

load_dotenv()  # читаем .env

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.kinopoisk.dev/v1.4"
headers = {"X-API-KEY": API_KEY, "accept": "application/json"}


@allure.story("Получение фильма по ID")
@pytest.mark.api
def test_get_movie_by_id():
    """Получение информации о фильме по его ID, корректные данные фильма."""
    movie_id = "3707"  # ID фильма "Страсти Христовы"
    with allure.step(f"Выполняем запрос GET /movie/{movie_id}"):
        response = requests.get(f"{API_URL}/movie/{movie_id}", headers=headers)
        assert response.status_code == 200, f"Ожидается статус 200, получен {response.status_code}"
        data = response.json()

    with allure.step("Проверяем, что в ответе есть название фильма и оно корректно"):
        assert "name" in data, "В ответе отсутствует поле 'name'"
        assert data["name"] == "Страсти Христовы", "Название фильма не совпадает"


@allure.story("Универсальный поиск с фильтрами")
@pytest.mark.api
def test_get_movies_with_filters():
    params = {
        "page": 1,
        "limit": 10
    }
    with allure.step("Выполняем запрос GET /movie с параметрами page=1 и limit=10"):
        response = requests.get(f"{API_URL}/movie", headers=headers,
                                params=params)
        assert response.status_code == 200, f"Статус ответа {response.status_code}, ожидается 200"
        data = response.json()

    with allure.step("Проверяем наличие ключа 'docs' и что это список"):
        assert "docs" in data, "В ответе отсутствует ключ 'docs'"
        assert isinstance(data["docs"], list), "'docs' должен быть списком"
        assert len(data["docs"]) <= 10, "Количество фильмов больше чем limit=10"


@allure.story("Поиск фильма по названию")
@pytest.mark.api
def test_search_movie_by_title():
    """ Выполняет поиск фильма по названию.
     :return: None
     """
    title = "Страсти Христовы"
    encoded_title = requests.utils.quote(title)
    endpoint = "/movie/search"
    full_url = f"{API_URL}{endpoint}?query={encoded_title}&page=1&limit=10"

    with allure.step("Отправляем запрос на поиск фильма"):
        response = requests.get(full_url, headers=headers)
        assert response.status_code == 200, f"Статус ответа {response.status_code}, ожидается 200"
        data = response.json()

    with allure.step("Проверяем структуру ответа"):
        assert "docs" in data, "В ответе отсутствует ключ 'docs'"
        assert isinstance(data["docs"], list), "'docs' должен быть списком"
        assert len(data["docs"]) > 0, "Список найденных фильмов пуст"

    with allure.step("Проверяем, что в названии первого результата есть ключевое слово"):
        first_movie = data["docs"][0]
        assert "name" in first_movie, "В первом фильме отсутствует поле 'name'"
        assert title.lower() in first_movie["name"].lower(), (
            f"Название фильма не содержит ожидаемый текст '{title}'"
        )


@allure.story("Получение списка наград и кинопремий")
@pytest.mark.api
def test_get_movie_awards():
    """
    Получение списка наград и кинопремии с проверками статуса и структуры данных.
    :return: None
    """
    endpoint = "movie/awards"
    params = {"page": 1, "limit": 10}
    full_url = f"{API_URL}/{endpoint}"

    with allure.step(f"Выполняем запрос GET {endpoint} с параметрами page=1 и limit=10"):
        response = requests.get(full_url, headers=headers, params=params)
        assert response.status_code == 200, f"Статус ответа {response.status_code}, ожидается 200"
        data = response.json()

    with allure.step("Проверяем, что ответ содержит ключ 'docs' с массивом наград"):
        assert "docs" in data, "В ответе отсутствует ключ 'docs'"
        assert isinstance(data["docs"], list), "'docs' должен быть списком"
        assert len(data["docs"]) > 0, "Список наград пуст"

    with allure.step("Проверяем структуру первого элемента списка наград"):
        first_award = data["docs"][0]
        assert isinstance(first_award, dict), "Элемент 'docs' должен быть словарем"
        expected_keys = ["id", "movieId", "nomination", "winning", "createdAt", "updatedAt"]
        for key in expected_keys:
            assert key in first_award, f"В первом элементе отсутствует поле '{key}'"

        nomination = first_award.get("nomination", {})
        assert isinstance(nomination, dict), "'nomination' должен быть словарём"
        assert "award" in nomination, "В 'nomination' отсутствует поле 'award'"

        award = nomination.get("award", {})
        assert isinstance(award, dict), "'award' должен быть словарём"
        expected_award_keys = ["title", "year"]
        for key in expected_award_keys:
            assert key in award, f"В 'award' отсутствует поле '{key}'"


@allure.story("Получение списка возможных значений статуса фильма")
@pytest.mark.api
def test_possible_status_values():
    url = "https://api.kinopoisk.dev/v1/movie/possible-values-by-field"
    params = {"field": "status"}

    with allure.step("Делаем запрос на получение возможных значений статуса фильма"):
        response = requests.get(url, headers=headers, params=params)
        assert response.status_code == 200, f"Ожидается статус 200, получен {response.status_code}"
        data = response.json()

    with allure.step("Проверяем, что ответ — список и он не пуст"):
        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, "Список значений пуст"

    with allure.step("Проверяем структуру первого элемента списка"):
        first_item = data[0]
        assert "name" in first_item, "Отсутствует ключ 'name' в элементе списка"
        assert "slug" in first_item, "Отсутствует ключ 'slug' в элементе списка"

    with allure.step("Выводим список возможных статусов"):
        allure.attach(str(data), "Возможные статусы", allure.attachment_type.TEXT)