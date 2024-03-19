import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv()
SELENIUM_USER_DATA_DIR = os.getenv('SELENIUM_USER_DATA_DIR')

options = Options()
options.add_argument(f"user-data-dir={SELENIUM_USER_DATA_DIR}")
driver = webdriver.Chrome(options=options, service=ChromeService(executable_path="./chromedriver"))

driver.get("https://www.linkedin.com/login")
input("Press enter when done")
driver.quit()