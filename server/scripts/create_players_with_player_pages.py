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
import requests

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db
from flask_app.models import Golfer

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

def convert_html_key_to_attribute(key):
    words = re.findall('[A-Za-z]+', key)
    return ''.join(word.capitalize() for word in words)

def create_golfers_in_tournament(tournament_link: str) -> None:

  # Establish a connection
  options = Options()

  options = webdriver.ChromeOptions()
  options.add_argument('--no-sandbox')
  options.headless = True

  options.add_argument('--headless=new')

  # Only pass options once when creating the WebDriver instance
  wd = webdriver.Chrome(options=options)

  driver = wd

  # Load page
  driver.get(tournament_link)

  golfers = driver.find_elements(By.CSS_SELECTOR, "a.AnchorLink.leaderboard_player_name")

  golfer_links = []

  for golfer in golfers:
    golfer_link = {golfer.text: golfer.get_attribute('href')}
    print(golfer_link)
    golfer_links.append(golfer_link)
  
  dummy_golfer = Golfer(FirstName="Dummy", LastName="Golfer")
  # Get all attribute names in lowercase
  golfer_attributes = dummy_golfer.dict().keys()

  for golfer in golfer_links:
    golfer_link, player_name = None, None
    for key, value in golfer.items():
      golfer_link = value
      player_name = key
    driver.get(golfer_link)

    # create a dict to hold all the info collected from the individual page
    player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")

    # Split player_name into first name and last name
    name_parts = player_name.split()
    first_name = name_parts[0]
    last_name = ' '.join(name_parts[1:])

    if "(a)" in last_name:
      # Remove "(a)" and surrounding whitespace from the string
      last_name = re.sub(r'\s*\([^)]*\)', '', last_name).strip()

    # query the database for names case insensitively 
    query_golfer = db.golfers.find_one({
        "FirstName": {"$regex": f"^{first_name}$", "$options": "i"},
        "LastName": {"$regex": f"^{last_name}$", "$options": "i"}
    })

    # if we do not have the golfer in the database
    if query_golfer == None:
      player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")
      right_side_data = player_header.find_element(By.CSS_SELECTOR, "div.flex.brdr-clr-gray-07.pl4.bl.bl--dotted.n8.brdr-clr-gray-07")
      keys = right_side_data.find_elements(By.CSS_SELECTOR, "div.ttu")
      values = right_side_data.find_elements(By.CSS_SELECTOR, "div.fw-medium.clr-black")
      
      # Create Golfer instance
      golfer_detail = Golfer(
          FirstName=first_name,
          LastName=last_name,
          Country=player_header.find_element(By.CSS_SELECTOR, "ul.PlayerHeader__Team_Info").text,
          GolferPageLink=golfer_link
      )

      # retrieve the country
      country = player_header.find_element(By.CSS_SELECTOR, "img.Image.Logo").get_attribute("alt")

      # get the flag of the country for the golfer
      response = requests.get(f'https://restcountries.com/v3.1/name/{country}?fields=flag')

      if response.status_code == 200:
          json_data = response.json()
          golfer_detail.Flag = json_data[0]["flag"]
      else:
          print("Error:", response.status_code)
      
      for key, value in zip(keys, values):
        new_string_value = convert_html_key_to_attribute(key.text)
        if new_string_value in golfer_attributes:
          setattr(golfer_detail, new_string_value, value.text)
        elif new_string_value == "Birthdate":
          golfer_detail.Birthdate = convert_to_date(value.text.split(' ')[0])
          golfer_detail.Age = calculate_age(golfer_detail.Birthdate)
        else:
          # Log or handle unrecognized attributes if necessary
          print(f"Unrecognized attribute: {new_string_value} with value: {value.text}")

      golfer_detail.save()
      print(f"Inserted new golfer: {golfer_detail}")

    else:
      # the golfer was most likely created elsewhere than the player page
      # add the values that are available for the golfer on their ESPN player page
      if "Swing" in query_golfer and not query_golfer["Swing"]:
        player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")
        right_side_data = player_header.find_element(By.CSS_SELECTOR, "div.flex.brdr-clr-gray-07.pl4.bl.bl--dotted.n8.brdr-clr-gray-07")
        keys = right_side_data.find_elements(By.CSS_SELECTOR, "div.ttu")
        values = right_side_data.find_elements(By.CSS_SELECTOR, "div.fw-medium.clr-black")
        
        golfer_detail = {}
        for key, value in zip(keys, values):
            string_values = re.findall('[A-Za-z]+', key.text)
            new_string_value = ''.join([value[0] + value[1:].lower() for value in string_values])
            if new_string_value == "Birthdate":
                golfer_detail[new_string_value] = convert_to_date(value.text.split(' ')[0])
            else:
                golfer_detail[new_string_value] = value.text
        
        db.golfers.update_one(
            {"_id": query_golfer["_id"]},  # Match the golfer by their ID
            {"$set": golfer_detail}  # Update the golfer's details
        )
        updated_golfer = db.golfers.find_one({"_id": query_golfer["_id"]})
        print(updated_golfer)
      else:
        continue

  driver.quit()  
