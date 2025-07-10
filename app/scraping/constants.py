FOLDER_PATH = "data"
BASE_URL = "https://merolagani.com"

STOCK_INFO_URL = "/LatestMarket.aspx"
STOCK_INFO_FILE_NAME = "stock_info.csv"

IPO_INFO_URL = "/Ipo.aspx?type=past"
IPO_INFO_FILE_NAME = "ipo_info.csv"

EXCLUDE_KEYS = {
    "Bookclose Date", "% Cash Dividend", "% Bonus Share", 
    "Right Share Ratio", "Venue", "Time", "Agenda"
}