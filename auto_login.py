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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B988FC22DD482A5008AEAFAA50CE8DB5E9F3915DF4A03D6FAA0C0B9D59BE8112D35EFD05ECF6F01504C65E341B2CD6AC82E5C9BE306F40B7856650977C4C1483B1D668578D766B17735ABADC37C2A1835EC88B864983A90EB38FB86BC4B35D6E98F71443771FCFA05986A09C5376102661A3CCBE8D88732681F7D5C4910887AF3BEB593E30ADC4F9AE01CEE9DF77B33EE48147DA6C768AB9C55EF4E0C9AF7DD4A797D2ECE822EBB0E22F3614B51C40E03E3483EBC8E1F07F4C8DE446CAB2807540FAF20EC4B7EBC790ABC0423FA5665090C85A80C6A016C40811716A9C638DE954E22C3EF246E5FDB57A820AEE786BCFB743AD5DD4481EFD2CF1D87CE96074497C0331AF76262BCFB18EACF7FA2222EC6EE28B0F1D2DCC22535597E9601BB896919D84A77085E11EE04DB0A8C91BAED8A123526F17ECDC23E9FC341B06D81A879C61407787A7211F3963CE6B3C9F27A295B0CB10BA27B6FFEB67531D3B13D1B2"})
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
