import asyncio
import datetime
import json
import httpx

from async_functions import organizing_excel_data
from sync_functions import (
    open_web_driver,
    get_filenames_in_directory,
    check_facebook_and_email,
    close_web_driver,
    clean_folder,
)

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)
    # Extract configuration parameters
    PROCESSED_FILES_DIR = config["PROCESSED_FILES_DIR"]
    SEMIFINISHED_FILES_DIR = config["SEMIFINISHED_FILES_DIR"]
    RAW_DATA_PATH = config["RAW_DATA_PATH"]
    CLEAN_SEMIFINISHED_FILES_DIR = bool(config["CLEAN_SEMIFINISHED_FILES_DIR"])
    ADDITIONAL_FACEBOOK_PARSING = bool(config["ADDITIONAL_FACEBOOK_PARSING"])
    CLEAN_PROCESSED_FILES_DIR = bool(config["CLEAN_PROCESSED_FILES_DIR"])


async def async_part_main():
    """
    Asynchronous main function for parsing Excel files.
    """

    # Set user agent for HTTP requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    # Set user agent for HTTP requests
    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        # Organize data parsing from Excel files asynchronously
        await organizing_excel_data(RAW_DATA_PATH, client)


def sync_part_main():
    """
    Synchronous main function for additional Facebook parsing.
    """

    # Open WebDriver instance
    _driver = open_web_driver()

    # Get list of filenames in SEMIFINISHED_FILES_DIR
    filenames_list = get_filenames_in_directory(SEMIFINISHED_FILES_DIR)

    # Iterate through files and perform Facebook and email checking
    for file in filenames_list:
        try:
            check_facebook_and_email(
                f"{SEMIFINISHED_FILES_DIR}/{file}", _driver
            )
        finally:
            # Close WebDriver instance
            close_web_driver(_driver)


if __name__ == "__main__":
    start = datetime.datetime.now()

    # Clean PROCESSED_FILES_DIR if specified in config
    if CLEAN_PROCESSED_FILES_DIR:
        clean_folder(PROCESSED_FILES_DIR)

    # Clean SEMIFINISHED_FILES_DIR if specified in config
    if CLEAN_SEMIFINISHED_FILES_DIR:
        clean_folder(SEMIFINISHED_FILES_DIR)

    # Run asynchronous parsing from Excel
    asyncio.run(async_part_main())

    # Run additional Facebook parsing if specified in config
    if ADDITIONAL_FACEBOOK_PARSING:
        sync_part_main()

    print("Total time is: ", datetime.datetime.now() - start)
