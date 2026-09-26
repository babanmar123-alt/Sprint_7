import pytest
from helpers.api_client import ApiClient
from helpers.generators import generate_courier_data
from data.urls import Urls


@pytest.fixture
def api_client():
    """Фикстура для базового API-клиента."""
    return ApiClient()


@pytest.fixture
def courier_data():
    """Фикстура — генерирует данные нового курьера."""
    return generate_courier_data()


@pytest.fixture
def created_courier(api_client, courier_data):
    """Фикстура — создаёт курьера до теста и удаляет после.

    Возвращает словарь с данными курьера и его ID.
    """
    # Создаём курьера
    response = api_client.post(Urls.COURIER_CREATE, data=courier_data)
    assert response.status_code == 201, \
        f"Не удалось создать курьера: {response.status_code} {response.text}"

    # Логинимся, чтобы получить ID
    login_response = api_client.post(Urls.COURIER_LOGIN, data={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    courier_id = login_response.json().get("id")

    yield {
        "data": courier_data,
        "id": courier_id
    }

    # Удаляем курьера после теста
    if courier_id:
        api_client.delete(
            Urls.COURIER_DELETE.format(courier_id=courier_id)
        )