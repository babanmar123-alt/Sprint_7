import allure
import pytest
from data.urls import Urls


@allure.feature("Создание заказа")
class TestCreateOrder:
    """Тесты для ручки POST /api/v1/orders."""

    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_color(self, api_client, color):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Ленина, 1",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2026-09-30",
            "comment": "Позвоните перед доставкой",
            "color": color
        }

        response = api_client.post(Urls.ORDERS_CREATE, data=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

        # Отменяем заказ после проверки
        track = response.json()["track"]
        api_client.put(Urls.ORDERS_CANCEL, params={"track": track})

    @allure.title("Тело ответа содержит track")
    def test_create_order_returns_track(self, api_client):
        order_data = {
            "firstName": "Пётр",
            "lastName": "Петров",
            "address": "Москва, ул. Пушкина, 2",
            "metroStation": 5,
            "phone": "+79997654321",
            "rentTime": 3,
            "deliveryDate": "2026-09-30",
            "comment": "Не звоните",
            "color": ["BLACK"]
        }

        response = api_client.post(Urls.ORDERS_CREATE, data=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

        # Отменяем заказ после проверки
        track = response.json()["track"]
        api_client.put(Urls.ORDERS_CANCEL, params={"track": track})