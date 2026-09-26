class Urls:
    """URL-адреса для API Яндекс.Самокат."""

    BASE_URL = "https://qa-scooter.praktikum-services.ru"

    # Эндпоинты
    COURIER_CREATE = "/api/v1/courier"                # Создание курьера (POST)
    COURIER_LOGIN = "/api/v1/courier/login"            # Логин курьера (POST)
    COURIER_DELETE = "/api/v1/courier/{courier_id}"    # Удаление курьера (DELETE)
    ORDERS_CREATE = "/api/v1/orders"                   # Создание заказа (POST)
    ORDERS_LIST = "/api/v1/orders"                     # Список заказов (GET)
    ORDERS_CANCEL = "/api/v1/orders/cancel"            # Отмена заказа (PUT)