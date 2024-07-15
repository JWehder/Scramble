import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.action_chains import ActionChains
import requests
from selenium.common.exceptions import NoSuchElementException

options = Options()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.headless = True

options.add_argument('--headless=new')

# Only pass options once when creating the WebDriver instance
wd = webdriver.Chrome(options=options)

driver = wd

# Load page
driver.get("https://www.espn.com/golf/stats/player/_/table/general/sort/cupPoints/dir/desc")

def check_condition_met():
    try:
        # Find the element
        footer_link_wrapper = driver.find_element(By.CSS_SELECTOR, "div.tc.mv5.loadMore.footer__statsBorder.bb.pb5")
        load_more_link = footer_link_wrapper.find_element(By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")
        # If the element is found and clickable, return True
        return load_more_link.is_enabled()
    except NoSuchElementException:
        # If the element is not found, return False
        return False

# Define your condition to stop clicking
condition_met = True

while condition_met:
    try:
        footer_link_wrapper = driver.find_element(By.CSS_SELECTOR, "div.tc.mv5.loadMore.footer__statsBorder.bb.pb5")
        load_more_link = footer_link_wrapper.find_element(By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")

        # Scroll to the element
        actions = ActionChains(driver)
        actions.move_to_element(load_more_link).perform()

        # Wait until the load more link is clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AnchorLink.loadMore__link")))

        # Now click the element
        load_more_link.click()

        # Wait for the additional data to load
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "td.Table__TD")))

        # Your logic to check if the condition is met
        # For example, check if a certain element is present
        # If the condition is met, set condition_met to True
        condition_met = check_condition_met()
    except:
        # Handle exceptions if necessary
        print("An error occurred while clicking the load more link.")

# grab the entire OWGR table
table = driver.find_element(By.CSS_SELECTOR, "div.ResponsiveTable")

# attempt to retrieve the left side of the OWGR table
left_side_table = table.find_element(By.CSS_SELECTOR, "table.Table.Table--align-right")

# grabs names and position in the rankings
left_side_rows = left_side_table.find_elements(By.CSS_SELECTOR, "tr.Table__TR")

# attempt to retrieve the right side of the OWGR table
right_side_table = table.find_element(By.CSS_SELECTOR, "div.Table__Scroller")

# grab the data that leads to the position results
right_side_rows = right_side_table.find_elements(By.CSS_SELECTOR, "tr.Table__TR")

players = []

for left_row, right_row in zip(left_side_rows[1:], right_side_rows[1:]):

  name = (left_row.find_element(By.CSS_SELECTOR, "a.AnchorLink").text).split(' ')

  first_name = name[0]
  last_name = ''.join(name[1:])

  age = left_row.find_element(By.CSS_SELECTOR, "div.age").text

  rank = left_row.find_element(By.CSS_SELECTOR, "td.Table__TD").text

  left_row_data = [rank, first_name, last_name, age]

  # retrieve the country
  country = left_row.find_element(By.CSS_SELECTOR, "img.Image").get_attribute("alt")

  # get the flag of the country for the golfer
  response = requests.get(f'https://restcountries.com/v3.1/name/{country}?fields=flag')

  flag = None

  if response.status_code == 200:
      json_data = response.json()
      flag = json_data[0]["flag"]
  else:
      print("Error:", response.status_code)

  # Split the data by newline characters and whitespace
  values = re.split(r'\s+|(?<=\d)(?=\$)', right_row.text)

  values = left_row_data + values

  earnings = re.findall(r'(\d+)', values[4])
  earnings = int(''.join(earnings))

  if values[1] + " " + values[2] == "Kevin Yu":
    values[3] = "25"
  
  if values[1] + " " + values[2] == "Parker Coody":
    values[3] = "24"

  player = {
      "Rank": values[0],
      "FirstName": values[1],
      "LastName": values[2],
      "Age": int(values[3]),
      "Earnings": earnings,
      "FedexPts": values[5],
      "Events": values[6],
      "Rounds": values[7],
      "Country": country,
      "Flag": flag,
      "Cuts": values[8],
      "Top10s": values[9],
      "Wins": values[10],
      "AvgScore": values[11]
  }

  players.append(player)

# Print the parsed tournaments as JSON objects
import json
print(json.dumps(players, indent=4))

driver.quit()