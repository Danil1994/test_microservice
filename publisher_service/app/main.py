import pandas

from app.driver import get_driver
from app.publisher import load_items
from app.utils import get_cookies, save_cookies


meta_data = [{"data_file": "men_shoes.csv", "category": "men", "subcategory": "Shoes"},
             {"data_file": "women_jewelry.csv", "category": "women", "subcategory": "Jewelry"}]


def main():
    for data in meta_data:
        df = pandas.read_csv(data["data_file"])
        category = data["category"]
        subcategory = data["subcategory"]
        driver = get_driver()

        # # test proxy
        # driver.get("https://httpbin.io/ip")
        # print(driver.find_element(By.TAG_NAME, "body").text)
        # driver.get("https://whoer.net/ru")
        # time.sleep(30)

        # save_cookies(driver)
        get_cookies(driver)

        # login(driver, username, password)
        # sign_up(driver)

        load_items(driver, df, category, subcategory)

        driver.quit()


if __name__ == "__main__":
    main()
