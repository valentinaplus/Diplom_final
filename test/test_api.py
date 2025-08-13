import pytest
import requests
import allure

API_URL = "https://api.kinopoisk.dev/v1.4"
API_KEY = "6F8HZZE-XZ84GJR-J3AWJZM-KGR2NEB"
headers = {"X-API-KEY": API_KEY, "accept": "application/json"}


@allure.story("Получение фильма по ID")
def test_get_movie_by_id():
    """ Получение информации о фильме по его ID,
    корректные данные фильма. """
    movie_id = "3707" # ID фильма "Страсти Христовы"
    data = requests.get(API_URL +  "/movie/" + movie_id, headers=headers)

    assert data.status_code == 200
    assert data.json()["name"] == "Страсти Христовы", "Название фильма не совпадает"
