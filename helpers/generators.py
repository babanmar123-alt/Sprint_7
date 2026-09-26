import random
import string


def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_courier_data():
    """Генерирует данные для нового курьера."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }