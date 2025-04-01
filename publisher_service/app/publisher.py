import pyautogui
import time
import pandas

from selenium.common import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from app.utils import get_cookies


def load_photo(driver: webdriver, row: dict) -> None:
    for _ in range(3):
        # Find and click on the button "ADD PHOTOS"
        add_photo_btn = driver.find_element(By.XPATH, '//div[contains(text(), "PHOTO")]')
        add_photo_btn.click()
        time.sleep(3)

        # Insert the path to the file (must be a full path)
        pyautogui.write(row['photo'])
        pyautogui.press('enter')
        time.sleep(3)

        try:
            apply_button = driver.find_element(By.XPATH, '//button[@data-et-on-name="select_first_photo"]')
            apply_button.click()
            time.sleep(3)
        except Exception as e:
            print("Element 'select_first_photo' was not fount", e)


def input_title(driver: webdriver, row: dict) -> None:
    try:
        title_input = driver.find_element(By.XPATH, '//input[@placeholder="What are you selling? (required)"]')
        title_input.send_keys(row['name'])
        time.sleep(2)
    except Exception as e:
        print(f"Problem with title: {e}")


def input_description(driver: webdriver, row: dict) -> None:
    try:
        desc_input = driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder="Describe it! (required)"]')
        desc_input.send_keys(row['description'])
        time.sleep(2)
    except Exception as e:
        print(f"Problem with description: {e}")


def select_categories(driver: webdriver, category: str, subcategory: str) -> None:
    try:
        # select category
        category_dropdown = driver.find_element(By.CSS_SELECTOR,
                                                'div.dropdown__selector.dropdown__selector--select-tag')
        category_dropdown.click()
        time.sleep(2)

        # select subcategory
        sub_category = driver.find_element(By.CSS_SELECTOR, f'a[data-et-name="{category}"]')
        sub_category.click()
        time.sleep(3)

        menu_items = driver.find_elements(By.CSS_SELECTOR, 'li.dropdown__menu__item div.p--l--7')

        for item in menu_items:
            if item.text.strip() == subcategory:
                item.click()
                break
        time.sleep(3)

    except Exception as e:
        print(f"Problem with categories: {e}")


def select_size_if_needed(driver: webdriver, row) -> None:
    """
    Проверяет наличие тега 'Select Size' и, если он есть, нажимает на него.
    """
    characteristics = row['characteristics']
    size = characteristics['Size']
    try:
        size_button = driver.find_element(By.CSS_SELECTOR, 'span.tc--lg')
        if size_button.text.strip() == "Select Size":
            size_button.click()
            time.sleep(2)
            # print("Нажатие на 'Select Size' выполнено")

        size_buttons = driver.find_elements(By.CSS_SELECTOR, 'li .multi-size-selector__button')

        for button in size_buttons:
            if button.text.strip() == size:
                button.click()
                # print(f"Размер {size} выбран")
                return

        print(f"Size {size} was not found")
    except NoSuchElementException:
        print("Tag 'Select Size' was not found, skip")


def input_price(driver: webdriver, row: dict) -> None:
    try:
        price = (str(row['price']))
        price = price.replace("$", "")
        price = int(float(price))

        original_price_input = driver.find_element(By.XPATH, '//input[@data-vv-name="originalPrice"]')
        original_price_input.send_keys(price)
        time.sleep(2)

        listing_price_input = driver.find_element(By.XPATH, '//input[@data-vv-name="listingPrice"]')
        listing_price_input.send_keys(price)
        time.sleep(2)

    except Exception as e:
        print(f"Problem with description: {e}")


def input_availability(driver: webdriver) -> None:
    try:
        driver.find_element(By.XPATH,
                            '//div[contains(@class, "dropdown__selector")]/span[text()="For Sale"]').click()
        time.sleep(2)

        driver.find_element(By.XPATH, '//ul[@data-test="dropdown_menu_list"]//a[text()="Not For Sale"]').click()
        time.sleep(5)

    except Exception as e:
        print(f"Problem with description: {e}")


def save_screenshot(driver: webdriver, row: dict, category: str) -> None:
    try:
        product_id = (row['unicum_id'])
        driver.save_screenshot(f"screenshots/{category}_{product_id}.png")

    except Exception as e:
        print(f"Problem with description: {e}")


def load_items(driver: webdriver, df: pandas, category: str, subcategory: str) -> None:
    get_cookies(driver)
    for index, row in df.iterrows():
        driver.get("https://poshmark.com/create-listing")
        time.sleep(3)

        driver.find_element(By.XPATH, '//button[contains(text(), "OK")]').click()
        time.sleep(3)

        load_photo(driver, row)

        input_title(driver, row)

        input_description(driver, row)

        select_categories(driver, category, subcategory)

        # select_size_if_needed(driver, row)

        input_price(driver, row)

        input_availability(driver)

        save_screenshot(driver, row, category)

        # Click "Next"
        save_button = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
        save_button.click()
        time.sleep(3)

    driver.quit()


if __name__ == "__main__":
    pass
