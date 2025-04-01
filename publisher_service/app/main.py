import pandas
import json

from app.driver import get_driver
from app.publisher import load_items
from app.utils import get_cookies, save_cookies


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


# meta_data = [{"data_file": "men_shoes.csv", "category": "men", "subcategory": "Shoes"},
#              {"data_file": "women_jewelry.csv", "category": "women", "subcategory": "Jewelry"}]

file_path = "Boots_MENS_Mens_Chelsea_Boots_20250401_104739.json"
full_data = load_json(file_path)


def main():
    category = full_data["metadata"]["source_category_name"]
    products = full_data["products"]
    driver = get_driver()
    for product_link in products:
        print("PROD", products[product_link])

    # subcategory = data["subcategory"]

    # # test proxy
    # driver.get("https://httpbin.io/ip")
    # print(driver.find_element(By.TAG_NAME, "body").text)
    # driver.get("https://whoer.net/ru")
    # time.sleep(30)

    # save_cookies(driver)
        get_cookies(driver)

    # login(driver, username, password)
    # sign_up(driver)

        load_items(driver, products[product_link], category, product_link)

    driver.quit()


if __name__ == "__main__":
    main()
