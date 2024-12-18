import json
import re
import requests
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys
from datetime import datetime , timedelta

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db
golfers_collection = db.golfers

# Selenium setup
options = Options()
options.add_argument('--no-sandbox')
options.headless = True
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

# Define the 6-hour time limit
six_hours_ago = datetime.now() - timedelta(hours=6)

# Load page
driver.get("https://www.espn.com/golf/stats/player/_/table/general/sort/cupPoints/dir/desc")

# Function to check if 'Load More' button is present and clickable
def check_condition_met():
    try:
        footer_link_wrapper = driver.find_element(By.CSS_SELECTOR, "div.tc.mv5.loadMore.footer__statsBorder.bb.pb5")
        load_more_link = footer_link_wrapper.find_element(By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")
        return load_more_link.is_enabled()
    except NoSuchElementException:
        return False

# Click 'Load More' button if available
# Click the button until it is no longer on the page
# Effectively loading all players possible.
condition_met = True
while condition_met:
    try:
        footer_link_wrapper = driver.find_element(By.CSS_SELECTOR, "div.tc.mv5.loadMore.footer__statsBorder.bb.pb5")
        load_more_link = footer_link_wrapper.find_element(By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")
        actions = ActionChains(driver)
        actions.move_to_element(load_more_link).perform()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")))
        load_more_link.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "td.Table__TD")))
        condition_met = check_condition_met()
    except:
        print("An error occurred while clicking the load more link.")

# Grab the table data
table = driver.find_element(By.CSS_SELECTOR, "div.ResponsiveTable")
left_side_table = table.find_element(By.CSS_SELECTOR, "table.Table.Table--align-right")
left_side_rows = left_side_table.find_elements(By.CSS_SELECTOR, "tr.Table__TR")
right_side_table = table.find_element(By.CSS_SELECTOR, "div.Table__Scroller")
right_side_rows = right_side_table.find_elements(By.CSS_SELECTOR, "tr.Table__TR")

# Parse players and update database
players = []
for left_row, right_row in zip(left_side_rows[1:], right_side_rows[1:]):
    name = (left_row.find_element(By.CSS_SELECTOR, "a.AnchorLink").text).split(' ')
    first_name, last_name = name[0], ' '.join(name[1:])
    age = left_row.find_element(By.CSS_SELECTOR, "div.age").text
    rank = left_row.find_element(By.CSS_SELECTOR, "td.Table__TD").text
    country = left_row.find_element(By.CSS_SELECTOR, "img.Image").get_attribute("alt")
        
    values = re.split(r'\s+|(?<=\d)(?=\$)', right_row.text)
    values = [rank, first_name, last_name, age] + values
    earnings = int(''.join(re.findall(r'(\d+)', values[4])))

    # Define a helper function for safe conversion
    def safe_convert(value, to_type, default=None):
        try:
            return to_type(value)
        except (ValueError, TypeError):
            return default

    updated = datetime.utcnow()

    # Define player data with safe conversion
    player = {
        "Rank": safe_convert(values[0], int),
        "FirstName": values[1],
        "LastName": values[2],
        "Age": safe_convert(values[3], int),
        "Earnings": earnings,
        "FedexPts": safe_convert(values[5], int),
        "Events": safe_convert(values[6], int),
        "Rounds": safe_convert(values[7], int),
        "Cuts": safe_convert(values[8], int),
        "Top10s": safe_convert(values[9], int),
        "Wins": safe_convert(values[10], int),
        "AvgScore": safe_convert(values[11], float),
        "updated_at": updated
    }

    # Check if the golfer exists and if it has been updated within the last 6 hours
    golfer = golfers_collection.find_one({
        "FirstName": first_name,
        "LastName": last_name,
        "$or": [
            {"updated_at": {"$lt": six_hours_ago}},  # Updated more than 6 hours ago
            {"updated_at": {"$exists": False}}  
        ]
    })
    if golfer:
        # Update existing golfer's data
        golfers_collection.update_one(
            {"_id": golfer["_id"]},
            {"$set": player}
        )
        print(f"Updated data for {first_name} {last_name}.")
    else:
        print(f"Could not find {first_name} {last_name}.")

    players.append(player)

# Clean up
driver.quit()
