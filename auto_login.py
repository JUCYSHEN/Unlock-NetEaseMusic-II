# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005D4210F2C4B53EA88306FFBD797330FC70FD7D8C66ADE68A314AF1B039DBE06603528F36970951EC1E41D6742B4B3C28F1B612DDD436432534590F1A4EA1F2851F40C976882C2B3D1BE845651794737A3A0199ACDB0B6AD96335AE2B1B319D84337BF33C322BB8D87139DA2833687307A6A2C27F70EF731C0913E255DADFEDF97AE672FDD9C20CF678DEC7B8C592E06A1CCCDCDCA18DBFB18235A4586D79221A51310F2DD5C8545E6347E751676863E00DB3790919A8001328581A00D1B98B0DF204DB6DC4B01B00EBFE1045109FEFF5C529E517D5DF8B7E0FBEE2F0B2BF7EB4BB331A7807CA91E17E16696AC2FED2847F0E44D8F3F03D45D3BF9603D27DC9A32B789F8C4894FBD68E01CE61AEB36806F87A5A808F080F4525C2B0BBE850348D5C5B620276EB171A665D09C3387C9DA1E8B9F3091EAA3123C03AC5B1F36162B987183D3CC3A43320245B9AC6BB3F2E7A5DCE33B201E7D28232D38A3C0A83E5EB"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
