import allure
from data.urls import Urls


@allure.feature("Список заказов")
class TestListOrders:
    """Тесты для ручки GET /api/v1/orders."""

    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_list(self, api_client):
        response = api_client.get(Urls.ORDERS_LIST)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Список заказов не пустой")
    def test_orders_list_not_empty(self, api_client):
        response = api_client.get(Urls.ORDERS_LIST)

        assert response.status_code == 200
        orders = response.json()["orders"]
        assert len(orders) > 0, "Список заказов пуст"