import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import sys
import os

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db

golfers_collection = db.golfers

def calculate_age(birth_date):
    
    # Get today's date
    today = datetime.today()
    
    # Calculate age
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    return age

def convert_to_date(date_string):
    # Convert birth date string to datetime object
    birth_date = datetime.strptime(date_string, "%m/%d/%Y")

    return birth_date

options = Options()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.headless = True

options.add_argument('--headless=new')

# Only pass options once when creating the WebDriver instance
wd = webdriver.Chrome(options=options)

driver = wd

def create_golfers_in_tournament(tournament_link: str) -> None:
  # Load page
  driver.get(tournament_link)

  golfers = driver.find_elements(By.CSS_SELECTOR, "a.AnchorLink.leaderboard_player_name")

  golfer_links = []

  for golfer in golfers:
    golfer_links.append(golfer.get_attribute('href'))

  for golfer_link in golfer_links:
    driver.get(golfer_link)

    # create a dict to hold all the info collected from the individual page
    golfer_detail = {}
    player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")
    player_name = player_header.find_element(By.CSS_SELECTOR, "h1.PlayerHeader__Name").text.split('\n')
    print(player_name)
    first_name, last_name = [name[0] + name[1:].lower() for name in player_name]
    # Query the golfer collection for the first and last name
    query_golfer = golfers_collection.find_one({"FirstName": first_name, "LastName": last_name})
    # if we do not have the golfer in the database
    if query_golfer == None:
        golfer_detail["FirstName"], golfer_detail["LastName"] = first_name, last_name
        right_side_data = player_header.find_element(By.CSS_SELECTOR, "div.flex.brdr-clr-gray-07.pl4.bl.bl--dotted.n8.brdr-clr-gray-07")
        keys = right_side_data.find_elements(By.CSS_SELECTOR, "div.ttu")
        values = right_side_data.find_elements(By.CSS_SELECTOR, "div.fw-medium.clr-black")
        golfer_detail["Country"] = player_header.find_element(By.CSS_SELECTOR, "ul.PlayerHeader__Team_Info").text
        for key, value in zip(keys, values):
          string_values = (re.findall('[A-Za-z]+', key.text))
          new_string_value = ''.join([value[0] + value[1:].lower() for value in string_values])
          golfer_detail[new_string_value] = value.text
          if new_string_value == "Birthdate":
            golfer_detail[new_string_value] = convert_to_date(value.text.split(' ')[0])
            golfer_detail["Age"] = calculate_age(golfer_detail[new_string_value])
        print(golfer_detail)
        inserted_golfer = golfers_collection.insert_one(golfer_detail)
        print(inserted_golfer)
    else:
      if "Swing" in query_golfer and not query_golfer["Swing"]:
        golfer_detail = {}
        player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")
        right_side_data = player_header.find_element(By.CSS_SELECTOR, "div.flex.brdr-clr-gray-07.pl4.bl.bl--dotted.n8.brdr-clr-gray-07")
        keys = right_side_data.find_elements(By.CSS_SELECTOR, "div.ttu")
        values = right_side_data.find_elements(By.CSS_SELECTOR, "div.fw-medium.clr-black")
        for key, value in zip(keys, values):
          string_values = (re.findall('[A-Za-z]+', key.text))
          new_string_value = ''.join([value[0] + value[1:].lower() for value in string_values])
          golfer_detail[new_string_value] = value
          if new_string_value == "Birthdate":
            golfer_detail[new_string_value] = convert_to_date(value.split(' '))

        golfers_collection.update_one(
        {"_id": query_golfer["_id"]},  # Match the golfer by their ID
        {"$set": golfer_detail}  # Update the golfer's details
        )
        # Retrieve the updated golfer from the database
        updated_golfer = db.golfers.find_one({"_id": query_golfer["_id"]})
        print(updated_golfer)
      else:
        continue

driver.quit()  
