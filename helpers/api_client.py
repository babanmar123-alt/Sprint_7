import requests
from data.urls import Urls


class ApiClient:
    """Базовый клиент для работы с API Яндекс.Самокат."""

    def __init__(self):
        self.base_url = Urls.BASE_URL

    def post(self, endpoint, data=None, params=None):
        """POST-запрос. Отправляет данные как JSON."""
        return requests.post(f"{self.base_url}{endpoint}", json=data, params=params)

    def get(self, endpoint, params=None):
        """GET-запрос."""
        return requests.get(f"{self.base_url}{endpoint}", params=params)

    def put(self, endpoint, data=None, params=None):
        """PUT-запрос. Отправляет данные как JSON."""
        return requests.put(f"{self.base_url}{endpoint}", json=data, params=params)

    def delete(self, endpoint, params=None):
        """DELETE-запрос."""
        return requests.delete(f"{self.base_url}{endpoint}", params=params)