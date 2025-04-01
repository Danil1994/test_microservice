from app.driver import get_driver
from app.publisher import load_item
from app.utils import get_cookies, load_json, save_cookies


def load_items(json_data):
    category = json_data["metadata"]["source_category_name"]
    products = json_data["products"]
    driver = get_driver()
    # login(driver, username, password)
    # sign_up(driver)
    for product_link in products:
        # # test proxy
        # driver.get("https://httpbin.io/ip")
        # print(driver.find_element(By.TAG_NAME, "body").text)
        # driver.get("https://whoer.net/ru")
        # time.sleep(30)

        # save_cookies(driver)
        get_cookies(driver)
        load_item(driver, products[product_link], category)

    driver.quit()


def main():
    file_path = "Boots_MENS_Mens_Chelsea_Boots_20250401_104739.json"
    json_data = load_json(file_path)
    load_items(json_data)


if __name__ == "__main__":
    main()
