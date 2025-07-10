import os
import csv
import requests
from bs4 import BeautifulSoup
from loguru import logger
from app.scraping.constants import *


def scrape_ipo_info():
    try:
        os.makedirs(FOLDER_PATH, exist_ok=True)
        file_path = os.path.join(FOLDER_PATH, IPO_INFO_FILE_NAME)

        response = requests.get(BASE_URL + IPO_INFO_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        announcements = soup.find('div', id='ctl00_ContentPlaceHolder1_divData') \
                            .find('div', class_="announcement-list") \
                            .find_all('div', class_="media")

        data_list = []
        for item in announcements:
            link_tag = item.find('div', class_="media-body").find('a')
            if not link_tag or 'href' not in link_tag.attrs:
                continue
            link = link_tag['href']
            details = extract_announcement_details(link)
            if details:
                filtered_details = {k: v for k, v in details.items() if k not in EXCLUDE_KEYS}
                data_list.append(filtered_details)

        if data_list:
            keys = sorted({k for d in data_list for k in d.keys()})
            file_path = os.path.join(FOLDER_PATH, IPO_INFO_FILE_NAME)
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data_list)
            logger.success(f"Saved IPO info to {file_path}")
        else:
            logger.warning("No data extracted to save.")

    except requests.RequestException as e:
        logger.exception(f"Network error occurred: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error during scraping: {e}")


def extract_announcement_details(EXTRACTION_URL):
    try:
        response = requests.get(BASE_URL + EXTRACTION_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("table")
        if not table:
            return None

        data = {}
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2:
                continue

            key = cols[0].text.strip().replace(":", "")
            value_td = cols[1]

            if key == "Symbol":
                symbol_input = value_td.find('input', {'id': 'StockSymbol'})
                symbol = symbol_input['value'] if symbol_input else ""
                company_link = value_td.find('a')
                company_name = company_link['title'] if company_link and 'title' in company_link.attrs else ""
                data["Symbol"] = symbol
                data["Company Name"] = company_name

            elif key == "Tags":
                tags = [a['title'] for a in value_td.find_all('a') if 'title' in a.attrs]
                data[key] = ', '.join(tags)

            else:
                value = value_td.text.strip()
                data[key] = value

        return data
    except Exception as e:
        logger.error(f"Failed to extract details from {link}: {e}")
        return None