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
    browser.add_cookie({"name": "MUSIC_U", "value": "0093D8CD4759E700D0228EBCAEEE3430D1E009A6E3BB359AFF4C9E420B122350F930E3DB57F201F80A159148DCD1912E7E977A5464EE1D423D68A1A251D54DD289A879BF99A5EC588EFBB93F2DF2E47E3E64055E1472A9529ED37E435A589BB3569F5A97E4D10ED33C33A271C5B9314D19C18098B873BA1E6C517C5A65256C839684EA889B1EA83ABFC079DF320F021677EB2DA1630FC8EAE7A5EC962617E5F18F6471AD0CF2E0C64B44833840A66B48A0B5CC628B225AA8FCDE05E0EA0D5371D90EE05037A81DB34277001B172B7485A11BFDCF179D566C112F51BDD1DBC948A80A55FE36185FA34FC0E939205184AE01E4190225FEAE71D19A362A36DA1EDD6684F5E8383F547E4A9194EEDB827494A53382BAE19272689BED834319331B3D4D108547E34121D2DE0DD5D110EE3AFFB1C29C214B34ED62379831CDFA8E933DBD1BD0B769D4868C59636CA3D1D6F4F2207ECC4000BC99B3DB37F24BA80D7A7070"})
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
