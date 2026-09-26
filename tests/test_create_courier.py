import allure
import pytest
from data.urls import Urls
from helpers.generators import generate_courier_data


@allure.feature("Создание курьера")
class TestCreateCourier:
    """Тесты для ручки POST /api/v1/courier."""

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, api_client, courier_data):
        response = api_client.post(Urls.COURIER_CREATE, data=courier_data)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Удаляем курьера после проверки
        login_response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = login_response.json()["id"]
        api_client.delete(Urls.COURIER_DELETE.format(courier_id=courier_id))

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, api_client, created_courier):
        # created_courier уже создан — пробуем создать с теми же данными
        response = api_client.post(
            Urls.COURIER_CREATE,
            data=created_courier["data"]
        )

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title("Нельзя создать курьера без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, api_client, missing_field):
        data = generate_courier_data()
        data.pop(missing_field)

        response = api_client.post(Urls.COURIER_CREATE, data=data)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"]

    @allure.title("Успешный запрос возвращает ok: true")
    def test_create_courier_returns_ok_true(self, api_client, courier_data):
        response = api_client.post(Urls.COURIER_CREATE, data=courier_data)

        assert response.json() == {"ok": True}

        # Удаляем курьера
        login_response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = login_response.json()["id"]
        api_client.delete(Urls.COURIER_DELETE.format(courier_id=courier_id))

    @allure.title("Нельзя создать курьера с уже существующим логином")
    def test_create_courier_with_existing_login(self, api_client, created_courier):
        # Генерируем нового курьера, но логин берём от существующего
        new_data = generate_courier_data()
        new_data["login"] = created_courier["data"]["login"]

        response = api_client.post(Urls.COURIER_CREATE, data=new_data)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title("Правильный код ответа 201 при создании курьера")
    def test_create_courier_status_code(self, api_client, courier_data):
        response = api_client.post(Urls.COURIER_CREATE, data=courier_data)

        assert response.status_code == 201

        # Удаляем курьера
        login_response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = login_response.json()["id"]
        api_client.delete(Urls.COURIER_DELETE.format(courier_id=courier_id))