import allure
import pytest
from data.urls import Urls
from helpers.generators import generate_courier_data


@allure.feature("Создание курьера")
class TestCreateCourier:
    """Тесты для ручки POST /api/v1/courier."""

    @allure.title("Курьера можно создать. Ответ: 201 + ok: true")
    def test_create_courier_success(self, api_client, courier_data, cleanup_courier):
        response = api_client.post(Urls.COURIER_CREATE, data=courier_data)

        # Проверяем и код, и тело ответа
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Регистрируем курьера на удаление (удалится после теста, даже при падении)
        login_response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = login_response.json()["id"]
        cleanup_courier.append(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, api_client, created_courier):
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

    @allure.title("Нельзя создать курьера с уже существующим логином")
    def test_create_courier_with_existing_login(self, api_client, created_courier):
        new_data = generate_courier_data()
        new_data["login"] = created_courier["data"]["login"]

        response = api_client.post(Urls.COURIER_CREATE, data=new_data)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]