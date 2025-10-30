from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # Optional, for automatic driver management
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv, re
from datetime import datetime
# Initialize Chrome WebDriver (using webdriver_manager for convenience)
service = Service(ChromeDriverManager().install())

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--blink-settings=imagesEnabled=false")  # don’t load images
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.vgchartz.com/games/games.php?name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre=&boxart=Both&banner=Both&ownership=Both&showmultiplat=No&results=50&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&shownasales=1&showdeveloper=0&showdeveloper=1&showcriticscore=0&showcriticscore=1&showpalsales=0&showpalsales=1&showreleasedate=0&showreleasedate=1&showuserscore=0&showuserscore=1&showjapansales=0&showjapansales=1&showlastupdate=0&showlastupdate=1&showothersales=0&showothersales=1&showshipped=0&showshipped=1")

element = driver.find_element(By.ID, "generalBody")

def convert_date(date_str):
    if not date_str or date_str.strip().upper() == "N/A":
        return ""  # or return "N/A" if you prefer keeping it visible

    # remove suffix like st, nd, rd, th (e.g., "01st" → "01")
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str.strip())

    try:
        # parse format like "27 Feb 20"
        dt = datetime.strptime(date_str, "%d %b %y")
        return dt.strftime("%#d/%#m/%Y")  # Windows format
    except Exception as e:
        print("Error parsing date:", date_str, e)
        return date_str


with open('vgsales.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Rank","img", "Name", "Platform", "Publisher", "Developer","VGChartz Score",
        "Critic_Score", "User_Score","Total Shipped", "Total_Sales",
        "NA_Sales", "PAL_Sales", "JP_Sales", "Other_Sales", "Release_Date", "Last Update"
    ])

while True:
    print("Scraping:", driver.current_url)

    try:
        general_body = driver.find_element(By.ID, "generalBody")
        table = general_body.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    except NoSuchElementException:
        print("Table not found on page, skipping.")
        break
    with open('vgsales.csv', 'a', newline='', encoding='utf-8') as file:
        for row in rows:
            cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            if cols:
                cols[-1] = convert_date(cols[-1])
                cols[-2] = convert_date(cols[-2])       
                writer = csv.writer(file)
                writer.writerow(cols)

    try:
        current_page = general_body.find_element(By.CSS_SELECTOR, "a.selected").text.strip()
        print("Current page:", current_page)
    except NoSuchElementException:
        print("No current page number found.")
        break

    try:

        pagination_links = general_body.find_elements(By.CSS_SELECTOR, "th span a")
        next_page = None

        for i, link in enumerate(pagination_links):
            if link.text.strip() == current_page:
                if i + 1 < len(pagination_links):
                    next_page = pagination_links[i + 1]
                break

        # If there’s no next page, break
        if not next_page or ">>" in next_page.text:
            print("Reached last page.")
            break

        driver.get(next_page.get_attribute("href"))

    except Exception as e:
        print("Pagination ended or error:", e)

driver.quit()
