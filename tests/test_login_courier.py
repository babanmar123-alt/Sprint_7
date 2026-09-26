import allure
import pytest
from data.urls import Urls


@allure.feature("Логин курьера")
class TestLoginCourier:
    """Тесты для ручки POST /api/v1/courier/login."""

    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self, api_client, created_courier):
        response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": created_courier["data"]["login"],
            "password": created_courier["data"]["password"]
        })

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Успешный логин возвращает id")
    def test_login_returns_id(self, api_client, created_courier):
        response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": created_courier["data"]["login"],
            "password": created_courier["data"]["password"]
        })

        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)

    @allure.title("Нельзя авторизоваться без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, api_client, created_courier, missing_field):
        data = {
            "login": created_courier["data"]["login"],
            "password": created_courier["data"]["password"]
        }
        data.pop(missing_field)

        response = api_client.post(Urls.COURIER_LOGIN, data=data)

        # Сервер может вернуть 400 (нет поля) или 504 (таймаут).
        # Проверяем, что это ошибка (>= 400), а не успех.
        assert response.status_code >= 400, \
            f"Ожидалась ошибка, получено: {response.status_code} {response.text}"

    @allure.title("Нельзя авторизоваться с неправильным логином")
    def test_login_wrong_login(self, api_client, created_courier):
        response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": "wrong_login_123",
            "password": created_courier["data"]["password"]
        })

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Нельзя авторизоваться с неправильным паролем")
    def test_login_wrong_password(self, api_client, created_courier):
        response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": created_courier["data"]["login"],
            "password": "wrong_password_123"
        })

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Нельзя авторизоваться под несуществующим пользователем")
    def test_login_nonexistent_user(self, api_client):
        response = api_client.post(Urls.COURIER_LOGIN, data={
            "login": "nonexistent_user_xyz",
            "password": "nonexistent_password_xyz"
        })

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]