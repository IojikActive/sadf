import csv
import requests
import json
import sys
import logging
import html_to_json
import time
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


logger = logging.getLogger("ParserOzone")
console_handler = logging.StreamHandler("console")

def init_driver():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("log-level=3")
    # chrome_options.add_argument("headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    return driver



def get_url_product():
    pass
    # return result_url_str

def get_json(driver):
    url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2" \
          "?url=/product/avtomaticheskaya-kofemashina-inhouse-rozhkovaya-coffee-arte-icm1507-seryy-397529235/"
    # response = requests.get(url=url)
    driver.get(url)

    logger.warning("create a html_string ")
    html_string = driver.page_source
    # logger.warning("html:")
    # logger.warning(html_string)

    logger.warning("html_string to json")

    with open('ozon_1.json', 'w', encoding='utf-8') as file:
        json.dump(html_string, file, ensure_ascii=False)
        # html_string = json.loads(html_string )
        # logger.warning(html_string)
    return html_string

def get_product_info(result):
    product = {}
    widgets = result["widgetStates"]
    for widget_name, widget_value in widgets.items():
        widget_value = json.loads(widget_value)
        if "webSale" in widget_name:
            product_info = widget_value["cellTrackingInfo"]["product"]
            product["title"] = product_info["title"]
            product["id"] = product_info["id"]
            product["price"] = product_info["price"]
            product["final_price"] = product_info["finalPrice"]

    with open('ozon.csv', 'a', encoding='utf-8') as filecsv:
        csv.DictWriter(filecsv, fieldnames=["title", "id", "price", "final_price"]).writerow(product)

def main():
    driver = init_driver()
     
    get_json(driver)

    with open('ozon.csv', 'w', encoding='utf-8') as filecsv:
        csv.DictWriter(filecsv, fieldnames=["title", "id", "price", "final_price"]).writeheader()

    with open('ozon_1.json', 'r', encoding='utf-8') as file:
        result = json.load(file)
        get_product_info(result)


if __name__ == '__main__':
    main()