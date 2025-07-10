import os
import csv
import requests
from bs4 import BeautifulSoup
from loguru import logger
from app.scraping.constants import *


def scrape_stock_info():
    try:
        os.makedirs(FOLDER_PATH, exist_ok=True)
        file_path = os.path.join(FOLDER_PATH, STOCK_INFO_FILE_NAME)

        response = requests.get(STOCK_INFO_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find("table")
        header = table.find("thead")

        titles = [th.text.strip() for th in header.find_all("th")]
        while titles and titles[-1] == '':
            titles.pop()

        body_rows = table.find_all("tr")[1:]
        data = []
        for row in body_rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if cols:
                while cols and cols[-1] == '':
                    cols.pop()
                data.append(cols)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(titles)
            writer.writerows(data)

        logger.success(f"Scraped {len(data)} rows and saved to {file_path}")

    except requests.RequestException as e:
        logger.exception(f"Network error occurred: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during scraping: {e}")
