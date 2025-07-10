from .ipo_scraper import scrape_ipo_info
from .stock_scraper import scrape_stock_info

def scrape_data():
    scrape_ipo_info()
    scrape_stock_info()
    