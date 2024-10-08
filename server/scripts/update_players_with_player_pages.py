import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble

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

tournament_links = ["https://www.espn.com/golf/leaderboard?tournamentId=401580338", "https://www.espn.com/golf/leaderboard?tournamentId=401580333", "https://www.espn.com/golf/leaderboard?tournamentId=401580337", "https://www.espn.com/golf/leaderboard?tournamentId=401580346", "https://www.espn.com/golf/leaderboard?tournamentId=401580332", "https://www.espn.com/golf/leaderboard?tournamentId=401580344", "https://www.espn.com/golf/leaderboard?tournamentId=401580336", "https://www.espn.com/golf/leaderboard?tournamentId=401580345", "https://www.espn.com/golf/leaderboard?tournamentId=401580330", "https://www.espn.com/golf/leaderboard?tournamentId=401580342", "https://www.espn.com/golf/leaderboard?tournamentId=401580331", "https://www.espn.com/golf/leaderboard?tournamentId=401580335", "https://www.espn.com/golf/leaderboard?tournamentId=401580340", "https://www.espn.com/golf/leaderboard?tournamentId=401580329", "https://www.espn.com/golf/leaderboard?tournamentId=401580343", "https://www.espn.com/golf/leaderboard?tournamentId=401580341", "https://www.espn.com/golf/leaderboard?tournamentId=401580334"]

for tournament_link in tournament_links:
    # Load page
    driver.get(tournament_link)

    golfers = driver.find_elements(By.CSS_SELECTOR, "a.AnchorLink.leaderboard_player_name")

    golfer_links = []

    for golfer in golfers:
        golfer_first_last = golfer.text.split(' ')
        first_name, last_name = golfer_first_last[0], ' '.join(golfer_first_last[1:])
        print(first_name, last_name)
        # Query the golfer collection for the first and last name
        query_golfer = golfers_collection.find_one({ "FirstName": first_name, "LastName": last_name })
        if query_golfer != None and "Swing" not in query_golfer:
            queried_golfer = {
                "FirstName": first_name, 
                "LastName": last_name,
                "Link": golfer.get_attribute('href')
            }
            golfer_links.append(queried_golfer)

    for golfer_link in golfer_links:
        driver.get(golfer_link["Link"])
        golfer_detail = {}
        player_header = driver.find_element(By.CSS_SELECTOR, "div.PlayerHeader__Container")
        right_side_data = player_header.find_element(By.CSS_SELECTOR, "div.flex.brdr-clr-gray-07.pl4.bl.bl--dotted.n8.brdr-clr-gray-07")
        keys = right_side_data.find_elements(By.CSS_SELECTOR, "div.ttu")
        values = right_side_data.find_elements(By.CSS_SELECTOR, "div.fw-medium.clr-black")
        for key, value in zip(keys, values):
            string_values = (re.findall('[A-Za-z]+', key.text))
            new_string_value = ''.join([value[0] + value[1:].lower() for value in string_values])
            golfer_detail[new_string_value] = value.text
            if new_string_value == "Birthdate":
                golfer_detail[new_string_value] = convert_to_date(value.text.split(' ')[0])
        update_golfer = golfers_collection.find_one({ 
            "FirstName": golfer_link["FirstName"], 
            "LastName": golfer_link["LastName"] 
        })
        print(update_golfer)
        print(golfer_detail)
        golfers_collection.update_one(
        {"_id": update_golfer["_id"]},  # Match the golfer by their ID
        {"$set": golfer_detail}  # Update the golfer's details
        )
        # Retrieve the updated golfer from the database
        print(update_golfer)

driver.quit()
client.close()