import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
import os

def save_tournament(tournament_name, tournament_details):

    output_file_name = f"../results/{tournament_name}"

    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.abspath(__file__))

    try:
        # Construct the absolute path to the data file
        file_path = os.path.join(dir_path, '..', 'results', output_file_name)

        # Now, 'players' contains the summarized data for each player's rounds
        # Writing the results to a file
        with open(file_path, "w") as outfile:
            json.dump(tournament_details, outfile, indent=4)

        # Add the output file to .gitignore
        gitignore_file = "../.gitignore"
        with open(gitignore_file, "a") as gitignore:
            gitignore.write(f"\n{output_file_name}")

        print(f"Data written to {output_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

tournaments = [
    {
        "EndDate": "2024-01-07T00:00:00",
        "StartDate": "2024-01-04T00:00:00",
        "Name": "The Sentry",
        "Venue": [
            "Kapalua Resort (Plantation Course)"
        ],
        "City": "Kapalua",
        "State": "HI",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580329",
            "https://www.espn.com/golf/player/_/id/3449/chris-kirk"
        ]
    },
    {
        "EndDate": "2024-01-14T00:00:00",
        "StartDate": "2024-01-11T00:00:00",
        "Name": "Sony Open in Hawaii",
        "Venue": [
            "Waialae Country Club"
        ],
        "City": "Honolulu",
        "State": "HI",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580330",
            "https://www.espn.com/golf/player/_/id/5462/grayson-murray"
        ]
    },
    {
        "EndDate": "2024-01-21T00:00:00",
        "StartDate": "2024-01-18T00:00:00",
        "Name": "The American Express",
        "Venue": [
            "La Quinta Country Club"
        ],
        "City": "La Quinta",
        "State": "CA",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580331",
            "https://www.espn.com/golf/player/_/id/4832046/nick-dunlap"
        ]
    },
    {
        "EndDate": "2024-01-27T00:00:00",
        "StartDate": "2024-01-24T00:00:00",
        "Name": "Farmers Insurance Open",
        "Venue": [
            "Torrey Pines (North Course)"
        ],
        "City": "La Jolla",
        "State": "CA",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580332",
            "https://www.espn.com/golf/player/_/id/10596/matthieu-pavon"
        ]
    },
    {
        "EndDate": "2024-02-03T00:00:00",
        "StartDate": "2024-02-01T00:00:00",
        "Name": "AT&T Pebble Beach Pro-Am",
        "Venue": [
            "Spyglass Hill GC"
        ],
        "City": "Pebble Beach",
        "State": "CA",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580333",
            "https://www.espn.com/golf/player/_/id/11119/wyndham-clark"
        ]
    },
    {
        "EndDate": "2024-02-11T00:00:00",
        "StartDate": "2024-02-08T00:00:00",
        "Name": "WM Phoenix Open",
        "Venue": [
            "TPC Scottsdale (Stadium Course)"
        ],
        "City": "Scottsdale",
        "State": "AZ",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580334",
            "https://www.espn.com/golf/player/_/id/3792/nick-taylor"
        ]
    },
    {
        "EndDate": "2024-02-18T00:00:00",
        "StartDate": "2024-02-15T00:00:00",
        "Name": "The Genesis Invitational",
        "Venue": [
            "Riviera Country Club"
        ],
        "City": "Pacific Palisades",
        "State": "CA",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580335",
            "https://www.espn.com/golf/player/_/id/5860/hideki-matsuyama"
        ]
    },
    {
        "EndDate": "2024-02-25T00:00:00",
        "StartDate": "2024-02-22T00:00:00",
        "Name": "Mexico Open at Vidanta",
        "Venue": [
            "Vidanta Vallarta"
        ],
        "City": "Nuevo Vallarta",
        "State": "Mexico",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580336",
            "https://www.espn.com/golf/player/_/id/9843/jake-knapp"
        ]
    },
    {
        "EndDate": "2024-03-03T00:00:00",
        "StartDate": "2024-02-22T00:00:00",
        "Name": "Cognizant Classic",
        "Venue": [
            "PGA National Resort & Spa (The Champion)"
        ],
        "City": "Palm Beach Gardens",
        "State": "FL",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580337",
            "https://www.espn.com/golf/player/_/id/4425898/austin-eckroat"
        ]
    },
    {
        "EndDate": "2024-03-10T00:00:00",
        "StartDate": "2024-03-07T00:00:00",
        "Name": "Arnold Palmer Invitational pres. by Mastercard",
        "Venue": [
            "Arnold Palmer's Bay Hill Club & Lodge"
        ],
        "City": "Orlando",
        "State": "FL",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580338",
            "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
        ]
    },
    {
        "EndDate": "2024-03-10T00:00:00",
        "StartDate": "2024-03-07T00:00:00",
        "Name": "Puerto Rico Open",
        "Venue": [
            "Grand Reserve Country Club"
        ],
        "City": "Rio Grande",
        "State": "Puerto Rico",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580339",
            "https://www.espn.com/golf/player/_/id/2283/brice-garnett"
        ]
    },
    {
        "EndDate": "2024-03-17T00:00:00",
        "StartDate": "2024-03-14T00:00:00",
        "Name": "THE PLAYERS Championship",
        "Venue": [
            "TPC Sawgrass (THE PLAYERS Stadium Course)"
        ],
        "City": "Ponte Vedra Beach",
        "State": "FL",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580340",
            "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
        ]
    },
    {
        "EndDate": "2024-03-24T00:00:00",
        "StartDate": "2024-03-21T00:00:00",
        "Name": "Valspar Championship",
        "Venue": [
            "Innisbrook Resort (Copperhead Course)"
        ],
        "City": "Palm Harbor",
        "State": "FL",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580341",
            "https://www.espn.com/golf/player/_/id/5692/peter-malnati"
        ]
    },
    {
        "EndDate": "2024-03-31T00:00:00",
        "StartDate": "2024-03-28T00:00:00",
        "Name": "Texas Children's Houston Open",
        "Venue": [
            "Memorial Park Golf Course"
        ],
        "City": "Houston",
        "State": "TX",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580342",
            "https://www.espn.com/golf/player/_/id/6937/stephan-jaeger"
        ]
    },
    {
        "EndDate": "2024-04-07T00:00:00",
        "StartDate": "2024-04-04T00:00:00",
        "Name": "Valero Texas Open",
        "Venue": [
            "TPC San Antonio (Oaks Course)"
        ],
        "City": "San Antonio",
        "State": "TX",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580343",
            "https://www.espn.com/golf/player/_/id/4419142/akshay-bhatia"
        ]
    },
    {
        "EndDate": "2024-04-14T00:00:00",
        "StartDate": "2024-04-11T00:00:00",
        "Name": "Masters Tournament",
        "Venue": [
            "Augusta National Golf Club"
        ],
        "City": "Augusta",
        "State": "GA",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580344",
            "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
        ]
    },
    {
        "EndDate": "2024-04-22T00:00:00",
        "StartDate": "2024-04-18T00:00:00",
        "Name": "RBC Heritage",
        "Venue": [
            "Harbour Town Golf Links"
        ],
        "City": "Hilton Head Island",
        "State": "SC",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580345",
            "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
        ]
    },
    {
        "EndDate": "2024-04-21T00:00:00",
        "StartDate": "2024-04-18T00:00:00",
        "Name": "Corales Puntacana Championship",
        "Venue": [
            "Puntacana Resort & Club (Corales Golf Course)"
        ],
        "City": "Punta Cana",
        "State": "Dominican Republic",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580346",
            "https://www.espn.com/golf/player/_/id/1651/billy-horschel"
        ]
    }
]

tournamentInfo = {
    # espnTournamentLink: 'https://www.espn.com/golf/leaderboard?tournamentId=401580344',
    # completed: true or false,
    # ongoing: true or false,
    # "Name": "The Sentry",
    # "StartDate": "2024-01-04T00:00:00",
    # "EndDate": "2024-01-07T00:00:00",
    # "IsOver": true,
    # "IsInProgress": false,
    # winner: null
    # "Venue": "Plantation Course at Kapalua",
    # "Location": "Kapalua, Maui, HI",
    # "Par": 73,
    # "Yards": 7596,
    # "Purse": 20000000,
    # "StartDateTime": "2024-01-04T12:45:00",
    # "Canceled": false,
    # "City": "Kapalua, Maui",
    # "State": "HI",
    # "ZipCode": null,
    # "Country": "USA",
    # "Format": "Stroke",
    # winner
    # "Rounds": []
}

def parse_leaderboard(leaderboard, driver):

  competitors_table = leaderboard

  golfers = []

  table_rows = competitors_table.find_elements(By.CSS_SELECTOR, "tr.PlayerRow__Overview")

  for row in table_rows:

    golfer_tournament_results = {
      "Position": None,
      "Name": None,
      "Score": None,
      "R1": 0,
      "R2": 0,
      "R3": 0,
      "R4": 0,
      "TotalStrokes": None,
      "Earnings": None,
      "FedexPts": None,
      "Rounds": []
    }

    # Assuming table_rows[0] is the desired table row to click
    element_to_click = row

    # grab specifically the position element and assign it to the position key
    golfer_tournament_results["Position"] = element_to_click.find_element(By.CSS_SELECTOR, "td.tl").text

    # grab specifically the golfers name element and assign it to the name key
    golfer_full_name = element_to_click.find_element(By.CSS_SELECTOR, "a.AnchorLink")
    golfer_full_name = golfer_full_name.text.split(' ')
    golfer_tournament_results["FirstName"] = golfer_full_name[0]
    golfer_tournament_results["LastName"] = " ".join(golfer_full_name[1:])

    # grab the remaining elements
    remaining = element_to_click.find_elements(By.CSS_SELECTOR, "td.Table__TD")

    for key, element in zip(golfer_tournament_results.keys(), remaining[1:]):
      golfer_tournament_results[key] = element.text

    golfer_tournament_results['Earnings'] = ''.join(re.findall(r'(\d+)', golfer_tournament_results['Earnings']))

    # Scroll to the element
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).perform()

    # Now click the element
    element_to_click.click()

    # wait for player detail element to be active so I can get hole by hole scoring
    player_detail = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.Leaderboard__Player__Detail"))
    )

    # Find the select button element
    select_button = player_detail.find_element(By.CSS_SELECTOR, "select.dropdown__select")

    # create an instance of the select object
    select = Select(select_button)

    # all of the keys for their subsequent values passed down almost like headers in a table

    # select by the round name
    for round in select.options:

      round_detail = {
          "Round": round.text,
          "Birdies": 0,
          "Eagles": 0,
          "Pars": 0,
          "Albatross": 0,
          "Bogeys": 0,
          "DoubleBogeys": 0,
          "WorseThanDoubleBogeys": 0,
          "Score": 0,
          "Holes": []
      }

      # query the page for the table displaying the golfer's scorecard
      table = player_detail.find_element(By.CSS_SELECTOR, "table.Table")

      # query the headers which are the holes
      holes = table.find_elements(By.CSS_SELECTOR, "thead.Table__header-group")

      # query the par and score for the golfer
      par_scores = table.find_element(By.CSS_SELECTOR, "tbody.Table__TBODY")

      # select the value by the current round
      select.select_by_visible_text(round.text)

      # wait for the page to change
      # WebDriverWait(player_detail, 3)

      # Extract integers less than or equal to six
      par_score = (par_scores.text).split('\n')
      par = par_score[0]
      score = par_score[1]
      par_matches = re.findall(r'\b[1-6]\b', str(par))
      score_matches = re.findall(r'\b[1-6]\b', str(score))

      # Convert string arrays to integer arrays
      hole_strokes = [int(match) for match in score_matches]
      par_scores = [int(match) for match in par_matches]

      # Calculate total score
      round_detail["StrokesPlayed"] = int(score[-2:])

      # enter in total par for the course/ round
      round_detail["TotalPar"] = int(par[-2:])

      # Calculate under par score
      round_detail["Score"] = round_detail["StrokesPlayed"] - round_detail["TotalPar"]

      hole = 1

      for strokes, par in zip(hole_strokes, par_scores):
        score = strokes - par
        # Determine whether each score is albatross, birdie, par, bogey, double bogey, or worse
        # Assuming albatross = -3, birdie = -2, par = -1, bogey = 1, double bogey = 2, worse = 3
        score_types = {
            'albatross': score == -3,
            'eagle': score == -2,
            'birdie': score == -1,
            'par': score == 0,
            'bogey': score == 1,
            'double_bogey': score == 2,
            'worse_than_double_bogey': score > 2
        }

        # Add calculated information to the object
        hole_result = {
            'Strokes': strokes,
            'Par': par,
            'NetScore': score,
            "HoleNumber": hole,
            'Birdie': score_types['birdie'],
            'Bogey': score_types['bogey'],
            'Par': score_types['par'],
            'Eagle': score_types['eagle'],
            'Albatross': score_types['albatross'],
            'DoubleBogey': score_types['double_bogey'],
            'WorseThanDoubleBogey': score_types['worse_than_double_bogey']
        }

        round_detail["Holes"].append(hole_result)

        hole += 1

        # Increment counts based on score type
        if score_types['albatross']:
            round_detail['Albatross'] += 1
        elif score_types['eagle']:
            round_detail['Eagles'] += 1
        elif score_types['birdie']:
            round_detail['Birdies'] += 1
        elif score_types['par']:
            round_detail['Pars'] += 1
        elif score_types['bogey']:
            round_detail['Bogeys'] += 1
        elif score_types['double_bogey']:
            round_detail['DoubleBogeys'] += 1
        elif score_types['worse_than_double_bogey']:
            round_detail['WorseThanDoubleBogeys'] += 1

      golfer_tournament_results['Rounds'].append(round_detail)

    golfers.append(golfer_tournament_results)

  return golfers

import re
from datetime import datetime

def parse_tournament_header(webpage_data):
  # grab the tournament info from the header
  header = webpage_data.find_element(By.CSS_SELECTOR, "div.Leaderboard__Header")

  # grab the par and yardage
  par_yardage = webpage_data.find_element(By.CSS_SELECTOR, "div.Leaderboard__Course__Location__Detail")

  # what's the status of the tournament? In progress, finished?
  status = webpage_data.find_element(By.CSS_SELECTOR, "div.status")

  # grab the specific element with the text that discloses the tournament status
  status_text = status.find_element(By.CSS_SELECTOR, "span").text

  is_completed, in_progress = False, False

  if status_text == "Final":
    is_completed = True
  else:
    in_progress = True

  par, yardage = re.findall(r'(\d+)', str(par_yardage.text))

  # grab the tournament info from the header
  purse_previous_winner = webpage_data.find_element(By.CSS_SELECTOR, "div.n7")

  # Split the string by uppercase letters
  split_values = re.findall('[A-Z][^A-Z]*', str(purse_previous_winner.text))

  purse = re.findall(r'(\d+)', purse_previous_winner.text)

  if purse:
    purse = int(''.join(purse))

  previous_winner = ''.join(split_values[-2:])

  return {
      "Purse": purse,
      "PreviousWinner": previous_winner,
      "Par": par,
      "Yardage": yardage,
      "IsCompleted": is_completed,
      "InProgress": in_progress
      }

def parse_winner_score(score_str):
    # Use regular expressions to remove parentheses
    score_match = re.match(r'(\d+) \((-\d+)\)', score_str)
    if score_match:
        total_strokes = int(score_match.group(1))
        score_under_par = int(score_match.group(2))
        return {'winnerScoreUnderPar': -score_under_par, 'winnerTotalStrokes': total_strokes}
    else:
        return None

def parse_playoff_leaderboard(table):
  playoff = {
      "PlayoffHoles": None,
      "PlayoffWinningStrokes": 0,
      "PlayoffWinnerName": None,
      "Golfers": []
  }

  data = table.find_elements(By.CSS_SELECTOR, "tr.Table__TR")
  playoff_holes = re.findall(r'(\d+)', data[1].text)
  playoff["PlayoffHoles"] = playoff_holes
  for datap in data[2:]:
    golfer = {}
    data_split = datap.text.split(' ')
    golfer["FirstName"] = data_split[0]
    golfer["LastName"] = data_split[1]
    golfer["PlayoffHolesTotalStrokes"] = int(data_split[-1])
    if playoff["PlayoffWinningStrokes"] == 0 or playoff["PlayoffWinningStrokes"] > golfer["PlayoffHolesTotalStrokes"]:
      playoff["PlayoffWinningStrokes"] = golfer["PlayoffHolesTotalStrokes"]
      playoff["PlayoffWinnerName"] = golfer["FirstName"] + " " + golfer["LastName"]
    golfer["Holes"] = [{"PlayoffHoleNumber": idx + 1, "Strokes": int(strokes), "HoleNumber": playoff_holes[idx]} for idx, strokes in enumerate(data_split[2:-1])]
    playoff["Golfers"].append(golfer)

    return playoff

def parse_tournaments(tournaments):

    options = Options()

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.headless = True

    options.add_argument('--headless=new')

    # Only pass options once when creating the WebDriver instance
    wd = webdriver.Chrome(options=options)

    driver = wd

    parsed_tournaments = []

    for item in tournaments:
        if 'DATES' in item:
            continue

        # Load page
        driver.get(item['Links'][0])

        competitors_table = driver.find_element(By.CSS_SELECTOR, "div.competitors")

        responsive_tables = competitors_table.find_elements(By.CSS_SELECTOR, "div.ResponsiveTable")

        header = parse_tournament_header(driver)

        print(header)

        # retrieve purse, previous winner, par, and yardage
        item.update(header)

        print(item['Name'])

        if len(responsive_tables) > 1:
          item["Playoff"] = True
          item["PlayoffDetails"] = parse_playoff_leaderboard(responsive_tables[0])

        item['Golfers'] = parse_leaderboard(responsive_tables[-1], driver)

        first_place_golfer = item['Golfers'][0]

        print(first_place_golfer)

        item['WinnerScore'] = first_place_golfer['Score']
        item['WinnerStrokes'] = first_place_golfer['TotalStrokes']
        item['WinnerName'] = first_place_golfer['FirstName'] + " " + first_place_golfer['LastName']

        parsed_tournaments.append(item)

        name = item['Name'].split(' ')
        name = '-'.join(name)

        save_tournament(name, item)

    driver.quit()

    return parsed_tournaments

# Call the parsing method with the provided array
parsed_tournaments = parse_tournaments(tournaments)
