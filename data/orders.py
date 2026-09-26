class OrderData:
    """Тестовые данные для заказов."""

    DEFAULT_ORDER = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, ул. Ленина, 1",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2026-09-30",
        "comment": "Позвоните перед доставкой",
        "color": ["BLACK"]
    }

    ORDER_WITHOUT_COLOR = {
        "firstName": "Пётр",
        "lastName": "Петров",
        "address": "Москва, ул. Пушкина, 2",
        "metroStation": 5,
        "phone": "+79997654321",
        "rentTime": 3,
        "deliveryDate": "2026-09-30",
        "comment": "Не звоните",
        "color": []
    }
