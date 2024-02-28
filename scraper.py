import json
import os
import re
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By

load_dotenv()
LINKEDIN_URL = os.getenv('LINKEDIN_URL')
SELENIUM_USER_DATA_DIR = os.getenv('SELENIUM_USER_DATA_DIR')


def get_recent_roles():
    options = Options()
    options.add_argument(f"user-data-dir={SELENIUM_USER_DATA_DIR}")
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options, service=ChromeService(executable_path="./chromedriver"))

    # Open LinkedIn URL
    driver.get(LINKEDIN_URL)
    time.sleep(5)

    # Need to scroll to load all the postings on the page
    header = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list__header")
    scroll_origin = ScrollOrigin.from_element(header, 50, 100)  # Offset: right/down
    for i in range(5):
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, 1000).perform()  # Scroll down
        time.sleep(1)
    for i in range(5):
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, -1000).perform()  # Scroll up
        time.sleep(1)

    # Get roles
    default_image_url = "https://img.freepik.com/free-vector/red-prohibited-sign-no-icon-warning-stop-symbol-safety-danger-isolated-vector-illustration_56104-912.jpg"  # URL of your default image
    roles = []
    # input("Press enter when done")
    positions = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
    for position in positions:
        is_promoted = False
        promoteds = position.find_elements(By.CSS_SELECTOR, ".job-card-container__footer-item")
        for promoted in promoteds:
            if promoted.text == "Promoted":
                is_promoted = True

        if is_promoted:
            continue
        # input("Press enter when done")
        position.click()
        time.sleep(1)
        company = position.find_element(By.CSS_SELECTOR, ".job-card-container__primary-description").text
        link = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute('href').split('?eBP')[0]
        title = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").text
        try:
            picture = position.find_element(By.CSS_SELECTOR, "img.ember-view").get_attribute('src')
        except NoSuchElementException:
            picture = default_image_url
        # input("Press enter when done")
        try:
            input_string = driver.find_element(By.CSS_SELECTOR,
                                               ".job-details-jobs-unified-top-card__job-insight").text
            values = ['Remote', 'Hybrid', 'On-site', 'Full-time', 'Internship', 'Contract', 'Entry level', 'Associate',
                      'Mid-Senior level', 'Director']
            found_values = [value for value in values if re.search(rf'\b{value}\b', input_string)]
            info = ' - '.join(found_values)
        except NoSuchElementException:
            info = ''
        roles.append((company, title, link, picture, info))

    driver.quit()
    return roles


if __name__ == "__main__":
    roles = get_recent_roles()
    print(json.dumps(roles, indent=1))
