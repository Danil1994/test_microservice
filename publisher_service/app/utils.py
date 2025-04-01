import pickle
import re
import time
import random
import string
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def save_cookies(driver: webdriver) -> None:
    driver.get("https://poshmark.com/")

    # We give time for manual entry (or use automated entry)
    time.sleep(60)  # Enter login and password if it necessary

    # save cookies
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def get_cookies(driver: webdriver) -> None:
    driver.get("https://poshmark.com/")

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Reload the page (automatic login)
    driver.refresh()

    time.sleep(5)


def random_string(length=8) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    return f"{random_string(10)}@mailinator.com"


def login(driver: webdriver, username: str, password: str) -> None:
    driver.get('https://poshmark.com/login')
    time.sleep(5)
    driver.find_element(By.NAME, 'login_form[username_email]').send_keys(username)
    driver.find_element(By.NAME, 'login_form[password]').send_keys(password)
    driver.find_element(By.NAME, 'login_form[password]').send_keys(Keys.RETURN)
    time.sleep(5)


def sign_up(driver: webdriver) -> dict[str, str]:
    try:
        driver.get("https://poshmark.com/signup")
        time.sleep(3)

        # Generate random data
        first_name = random_string(6).capitalize()
        last_name = random_string(7).capitalize()
        email = random_email()
        username = random_string(10)
        password = random_string(12)
        # Fill form
        driver.find_element(By.CSS_SELECTOR, 'div[data-test="signup_first_name-text"] input').send_keys(first_name)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[data-test="signup_last_name-text"] input').send_keys(last_name)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[data-test="signup_email-text"] input').send_keys(email)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[data-test="signup_username-text"] input').send_keys(username)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div[data-test="signup_password-text"] input').send_keys(password)

        time.sleep(2)

        driver.find_element(By.XPATH, '//button[contains(text(), "Next")]').click()

        time.sleep(300)

        print(f"✅ Successful registration: {username} ({email})")
        return {"username": username, "email": email, "password": password}

    except Exception as e:
        print(f"❌ Registration error: {e}")


def remove_html_tags(text):
    return BeautifulSoup(text, "html.parser").get_text().strip()


def split_and_clean(text: str) -> tuple[str, str, str]:
    """
    Separate string by '>' and del extra space

    :param text: Строка в формате "Men > Shoes"
    :return: Кортеж (первое слово, второе слово)
    """
    parts = [part.strip() for part in text.split(">")]
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    else:
        raise ValueError("String should contain only one symbol '>'")


def normalize_size(size_dict: dict) -> str:
    """
    Преобразует размер из формата "7 1/2 D" в "7.5" или "8 D" в "8".
    """
    size = size_dict["name"]
    # size = size.split()[0]  # Берём только первое число
    size = size.replace(" 1/2", ".5")  # Заменяем дробь
    size = re.sub(r"[^\d.]", "", size)
    return size


def load_json(file_path: str) -> dict:
    """
    Загружает JSON-файл и возвращает его содержимое в виде словаря.

    :param file_path: Путь к JSON-файлу.
    :return: Словарь с данными из JSON.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {file_path} содержит некорректный JSON.")
        return {}


categories_dict = {
    "Accessories": ["Accessories"],
    "Bags": ["Bags"],
    "Jackets & Coats": ["Jackets & Coats"],
    "Jeans": ["Jeans"],
    "Pants": ["Pants"],
    "Shirts": ["Shirts"],
    "Shoes": ["Boots", "Shoes"],
    "Shorts": ["Shorts"],
    "Suits & Blazers": ["Suits & Blazers"],
    "Sweaters": ["Sweaters"],
    "Swim": ["Swim"],
    "Underwear & Socks": ["Underwear & Socks"],
    "Grooming": ["Grooming"],
    "Global & Traditional Wear": ["Global & Traditional Wear"],
}


def define_category(item_category: str) -> str:
    for category in categories_dict:
        if item_category in categories_dict[category]:
            return category
    return 'Other'


if __name__ == "__main__":
    pass
