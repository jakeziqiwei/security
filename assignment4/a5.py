# be sure to run the following first:
# python3 -m pip install selenium
# python3 -m pip install webdriver-manager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disk-cache-size=0")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument(
    "--disable-component-extensions-with-background-pages")
chrome_options.add_argument("--no-default-browser-check")

pageofinterest = "https://blase.courses/"
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.get(pageofinterest)
time.sleep(10)
browser.close()
browser.quit()
