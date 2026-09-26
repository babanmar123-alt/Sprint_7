import allure
import pytest
from data.urls import Urls
from data.orders import OrderData


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
    def test_create_order_with_color(self, api_client, color, cleanup_order):
        order_data = OrderData.DEFAULT_ORDER.copy()
        order_data["color"] = color

        response = api_client.post(Urls.ORDERS_CREATE, data=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

        # Регистрируем заказ на отмену (отменится после теста, даже при падении)
        cleanup_order.append(response.json()["track"])