import pyautogui
import time

from selenium.common import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from app.utils import normalize_size, remove_html_tags, split_and_clean


def load_photo(driver: webdriver, photos: list) -> None:
    for photo_link in photos:
        # Find and click on the button "ADD PHOTOS"
        add_photo_btn = driver.find_element(By.XPATH, '//div[contains(text(), "PHOTO")]')
        add_photo_btn.click()
        time.sleep(3)

        # Insert the path to the file (must be a full path)
        pyautogui.write(photo_link)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)

        try:
            apply_button = driver.find_element(By.XPATH, '//button[@data-et-on-name="select_first_photo"]')
            apply_button.click()
            time.sleep(3)
        except Exception as e:
            print("Element 'select_first_photo' was not fount", e)


def input_title(driver: webdriver, name: str) -> None:
    try:
        title_input = driver.find_element(By.XPATH, '//input[@placeholder="What are you selling? (required)"]')
        title_input.send_keys(name)
        time.sleep(2)
    except Exception as e:
        print(f"Problem with title: {e}")


def input_description(driver: webdriver, desc: str) -> None:
    try:
        desc_input = driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder="Describe it! (required)"]')
        desc_input.send_keys(desc)
        time.sleep(2)
    except Exception as e:
        print(f"Problem with description: {e}")


def select_categories(driver: webdriver, item_category: str, item_subcategory: str) -> None:
    item_category = item_category.lower()
    item_category = item_category.replace("'s", "").replace("’s", "")
    try:
        # select category
        category_dropdown = driver.find_element(By.CSS_SELECTOR,
                                                'div.dropdown__selector.dropdown__selector--select-tag')
        category_dropdown.click()
        time.sleep(2)

        sub_category = driver.find_element(By.CSS_SELECTOR, f'a[data-et-name="{item_category}"]')
        sub_category.click()
        time.sleep(3)

        # select subcategory
        menu_items = driver.find_elements(By.CSS_SELECTOR, 'li.dropdown__menu__item div.p--l--7')

        for item in menu_items:
            if item.text.strip() == item_subcategory:
                item.click()
                time.sleep(3)
                return

        for item in menu_items:
            if item.text.strip() == "Other":
                item.click()
                time.sleep(3)
                return

    except Exception as e:
        print(f"Problem with categories: {e}")


def select_sizes_if_needed(driver: webdriver, sizes: list[dict]) -> None:
    # Convert the sizes from the input list to the required format
    normalized_sizes = [normalize_size(size) for size in sizes]

    """
    Looks for the 'Select Size' button, clicks it, then selects all the desired sizes.
    
    :param driver: WebDriver Selenium
    :param sizes: List of sizes in the format ["7 D", "7 1/2 D", "8 D"]
    """
    try:
        # Check if there is a "Multi Item" button (if we select several sizes)
        try:
            multi_item_button = driver.find_element(By.CSS_SELECTOR, 'button[data-et-name="multiple"]')
            multi_item_button.click()
            time.sleep(4)
        except NoSuchElementException:
            print("Button 'Multi Item' not found, continue")

        try:
            size_button = driver.find_element(By.CSS_SELECTOR, 'span.tc--lg')
            if size_button.text.strip() == "Select Size":
                size_button.click()
                time.sleep(3)

                size_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                    'li div.multi-size-selector__button__container button.multi-size-selector__button')

                # Search and click on the required sizes
                for button in size_buttons:
                    button_text = button.text.strip()
                    if button_text in normalized_sizes:
                        button.click()
                        time.sleep(1)

                print(f"Chose sizes: {normalized_sizes}")

                try:
                    done_button = driver.find_element(By.CSS_SELECTOR, 'button[data-et-name="apply"]')
                    done_button.click()
                except NoSuchElementException:
                    print("❌ Button 'Done' was not found")

        except NoSuchElementException:
            print("Button 'Select Size' not found, skipping")

    except Exception as e:
        print(f"Error when choosing size: {e}")


def input_price(driver: webdriver, price: float) -> None:
    try:
        # price = (str(row['price']))
        # price = price.replace("$", "")
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


def save_screenshot(driver: webdriver, link: str) -> None:
    try:
        driver.save_screenshot(f"screenshots/{link}.png")

    except Exception as e:
        print(f"Problem with screenshot: {e}")


def load_item(driver: webdriver, product: dict, full_category: str) -> None:
    try:
        driver.get("https://poshmark.com/create-listing")
        time.sleep(3)

        driver.find_element(By.XPATH, '//button[contains(text(), "OK")]').click()
        time.sleep(3)

        load_photo(driver, product["images"])

        input_title(driver, product["name"])

        description_full_text_html = product["product_details"]["description_full_text_html"]
        description_text = remove_html_tags(description_full_text_html)
        input_description(driver, description_text)

        subcategory, category, section = split_and_clean(full_category)
        select_categories(driver, category, subcategory)

        sizes = product["variations"]["sizes"]
        select_sizes_if_needed(driver, sizes)

        pound_price = product["price"]
        pound_price = pound_price.replace("£", "")
        dollar_price = float(pound_price) * 1.26
        input_price(driver, dollar_price)

        input_availability(driver)

        # save_screenshot(driver, product["name"])

        # Click "Next"
        save_button = driver.find_element(By.XPATH, '//button[contains(text(), "Next")]')
        save_button.click()
        time.sleep(3)

    except Exception as e:
        print(f"Problem with load item: {e}")


if __name__ == "__main__":
    pass
