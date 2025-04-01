import pickle
import time
import random
import string

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

        print(f"✅ Успешная регистрация: {username} ({email})")
        return {"username": username, "email": email, "password": password}

    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")


if __name__ == "__main__":
    pass
