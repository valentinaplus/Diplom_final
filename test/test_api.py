import pytest
import requests
import allure

API_URL = "https://api.kinopoisk.dev/v1.4"
API_KEY = "6F8HZZE-XZ84GJR-J3AWJZM-KGR2NEB"
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
    """ Тестируем поиск фильмов по названию с использованием параметров. """
    title = "Страсти Христовы"
    encoded_title = requests.utils.quote(title)
    endpoint = "/movie/search"
    full_url = f"{API_URL}{endpoint}?query={encoded_title}&page=1&limit=10"

    with allure.step("Отправляем запрос на поиск фильма"):
        response = requests.get(full_url, headers=headers)
        assert response.status_code == 200, f"Статус ответа {response.status_code}, ожидается 200"
        data = response.json()


@allure.story("Получение списка наград и кинопремий")
@pytest.mark.api
def test_get_movie_awards():
    endpoint = "movie/awards"
    params = {"page": 1, "limit": 10}
    full_url = f"{API_URL}/{endpoint}"

    with allure.step(f"Выполняем запрос GET {endpoint} с параметрами page=1 и limit=10"):
        response = requests.get(full_url, headers=headers)
        assert response.status_code == 200, f"Статус ответа {response.status_code}, ожидается 200"
        data = response.json()


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