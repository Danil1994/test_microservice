import random

from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

PROXY = [
    "socks5://1552iibq9u3:h716yn5lcx@213.109.192.192:1080"
]


def parse_proxy(proxy_str: str):
    parsed = urlparse(proxy_str)
    proxy_username, proxy_password = parsed.username, parsed.password
    proxy_address, proxy_port = parsed.hostname, parsed.port

    return proxy_username, proxy_password, proxy_address, str(proxy_port)


def get_driver() -> webdriver:
    proxy_str = random.choice(PROXY)
    proxy_username, proxy_password, proxy_address, proxy_port = parse_proxy(proxy_str)
    proxy_url = f"socks5://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"

    seleniumwire_options = {
        "proxy": {
            "http": proxy_url,
            "https": proxy_url
        },
    }

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")

    # initialize the Chrome driver with service, selenium-wire options, and chrome options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        # seleniumwire_options=seleniumwire_options,
        options=options
    )

    return driver


if __name__ == "__main__":
    pass