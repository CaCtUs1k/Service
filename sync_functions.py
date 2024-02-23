import json
import re
import shutil

from selenium.webdriver.chrome.webdriver import WebDriver

import csv
import os

from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError, NewConnectionError

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)  # Set user agent string to mimic a browser

with open("config.json", "r") as file:
    config = json.load(file)
    PROCESSED_FILES_DIR = config["PROCESSED_FILES_DIR"]


def open_web_driver() -> WebDriver:
    """
    Open a Chrome WebDriver instance with specified options.
    """
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def close_web_driver(driver: WebDriver) -> None:
    """
    Close the given WebDriver instance.
    """
    driver.quit()


def get_filenames_in_directory(directory: str) -> list:
    """
    Get a list of filenames in the specified directory.

    Returns:
        list: List of filenames in the directory.
    """
    filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filenames.append(filename)
    return filenames


def check_facebook_and_email(filename: str, driver: WebDriver) -> None:
    """
    Check for Facebook links without associated email addresses in a CSV file,
    and attempt to find email addresses for those links.
    """
    updated_rows = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            facebook = row["Facebook"]
            email = row["Email"]
            if facebook and not email:
                url = facebook.split(",")[0]
                try:
                    match = find_email_on_facebook(url, driver)
                    if match:
                        email_address = match.group()
                        print(f'Found email for {row["Website"]}')
                        row["Email"] = (
                            email_address  # Update the email field in the row
                        )

                except (
                    InvalidArgumentException,
                    MaxRetryError,
                    NewConnectionError,
                ) as e:
                    # If there's an error, close and reopen the WebDriver
                    close_web_driver(driver)
                    driver = open_web_driver()
            updated_rows.append(row)

    if not os.path.exists(PROCESSED_FILES_DIR):
        os.makedirs(PROCESSED_FILES_DIR)
    processed_filename = os.path.join(
        PROCESSED_FILES_DIR, filename.split("/")[-1]
    )

    with open(
        processed_filename, "w", newline="", encoding="utf-8"
    ) as csvfile:
        try:
            fieldnames = updated_rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        except IndexError:
            print(f"File {filename} is empty")


def find_email_on_facebook(url: str, driver: WebDriver) -> re.Match:
    """
    Find email addresses on a Facebook page.

    Returns:
        re.Match: A match object containing the email address found on the page.
    """
    driver.get(url)
    try:
        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '[role="button"][tabindex="0"] > [data-visualcompletion="css-img"]',
                )
            )
        )
        button.click()
    except Exception:
        pass

    WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    emails = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        driver.page_source,
    )
    return emails


def clean_folder(path: str) -> None:
    """
    Clean a folder by removing all its contents.
    """
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
