import pickle
import time
import random
import string

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


if __name__ == "__main__":
    pass
