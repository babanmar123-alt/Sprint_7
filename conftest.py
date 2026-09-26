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
    """Фикстура — создаёт курьера до теста и удаляет после."""
    response = api_client.post(Urls.COURIER_CREATE, data=courier_data)

    if response.status_code != 201:
        raise Exception(
            f"Не удалось создать курьера в фикстуре: "
            f"{response.status_code} {response.text}"
        )

    login_response = api_client.post(Urls.COURIER_LOGIN, data={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    courier_id = login_response.json().get("id")

    yield {
        "data": courier_data,
        "id": courier_id
    }

    if courier_id:
        api_client.delete(Urls.COURIER_DELETE.format(courier_id=courier_id))


@pytest.fixture
def cleanup_courier(api_client):
    """Фикстура для удаления курьеров, созданных в тесте.

    Возвращает список — в него тест добавляет ID курьеров для удаления.
    """
    couriers_to_delete = []
    yield couriers_to_delete

    for courier_id in couriers_to_delete:
        api_client.delete(Urls.COURIER_DELETE.format(courier_id=courier_id))


@pytest.fixture
def cleanup_order(api_client):
    """Фикстура для отмены заказов, созданных в тесте.

    Возвращает список — в него тест добавляет track заказов для отмены.
    """
    orders_to_cancel = []
    yield orders_to_cancel

    for track in orders_to_cancel:
        api_client.put(Urls.ORDERS_CANCEL, params={"track": track})