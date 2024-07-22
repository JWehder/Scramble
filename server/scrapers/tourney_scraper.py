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
from selenium.common.exceptions import NoSuchElementException
import pytz

def check_data_exists(parent_element: str, query_element: str) -> bool:
    try:
        data = parent_element.find_element(By.CSS_SELECTOR, query_element)
        return True if data else False
    except NoSuchElementException:
        return False

def save_tournament(tournament_name: str, tournament_details: object) -> None:
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
    # {
    #     "EndDate": "2024-07-21T00:00:00",
    #     "StartDate": "2024-07-18T00:00:00",
    #     "Name": "The Open",
    #     "Venue": [
    #         "Royal Troon Golf Course"
    #     ],
    #     "City": "Troon",
    #     "State": "Scotland",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580360",
    #         "https://www.espn.com/golf/player/_/id/1225/brian-harman"
    #     ]
    # },
    # {
    #     "EndDate": "2024-07-21T00:00:00",
    #     "StartDate": "2024-07-18T00:00:00",
    #     "Name": "Barracuda Championship",
    #     "Venue": [
    #         "Tahoe Mountain Club (Old Greenwood)"
    #     ],
    #     "City": "Truckee",
    #     "State": "CA",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580361",
    #         "https://www.espn.com/golf/player/_/id/4419142/akshay-bhatia"
    #     ]
    # },
    # {
    #     "EndDate": "2024-07-28T00:00:00",
    #     "StartDate": "2024-07-25T00:00:00",
    #     "Name": "3M Open",
    #     "Venue": [
    #         "TPC Twin Cities"
    #     ],
    #     "City": "Blaine",
    #     "State": "MN",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580362",
    #         "https://www.espn.com/golf/player/_/id/4404991/lee-hodges"
    #     ]
    # },
    # {
    #     "EndDate": "2024-08-11T00:00:00",
    #     "StartDate": "2024-08-08T00:00:00",
    #     "Name": "Wyndham Championship",
    #     "Venue": [
    #         "Sedgefield Country Club"
    #     ],
    #     "City": "Greensboro",
    #     "State": "NC",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580363",
    #         "https://www.espn.com/golf/player/_/id/676/lucas-glover"
    #     ]
    # },
    # {
    #     "EndDate": "2024-08-18T00:00:00",
    #     "StartDate": "2024-08-15T00:00:00",
    #     "Name": "FedEx St. Jude Championship",
    #     "Venue": [
    #         "TPC Southwind"
    #     ],
    #     "City": "Memphis",
    #     "State": "TN",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580364",
    #         "https://www.espn.com/golf/player/_/id/676/lucas-glover"
    #     ]
    # },
    # {
    #     "EndDate": "2024-08-25T00:00:00",
    #     "StartDate": "2024-08-22T00:00:00",
    #     "Name": "BMW Championship",
    #     "Venue": [
    #         "Castle Pines Golf Club"
    #     ],
    #     "City": "Castle Rock",
    #     "State": "CO",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580365",
    #         "https://www.espn.com/golf/player/_/id/4364873/viktor-hovland"
    #     ]
    # },
    # {
    #     "EndDate": "2024-09-01T00:00:00",
    #     "StartDate": "2024-08-22T00:00:00",
    #     "Name": "TOUR Championship",
    #     "Venue": [
    #         "East Lake Golf Club"
    #     ],
    #     "City": "Atlanta",
    #     "State": "GA",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580366",
    #         "https://www.espn.com/golf/player/_/id/4364873/viktor-hovland"
    #     ]
    # },
    # {
    #     "EndDate": "2024-09-15T00:00:00",
    #     "StartDate": "2024-09-12T00:00:00",
    #     "Name": "Napa Valley Golf Championship",
    #     "Venue": [
    #         "Silverado Resort and Spa (North Course)"
    #     ],
    #     "City": "Napa",
    #     "State": "CA",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693936",
    #         "https://www.espn.com/golf/player/_/id/10980/sahith-theegala"
    #     ]
    # },
    # {
    #     "EndDate": "2024-09-29T00:00:00",
    #     "StartDate": "2024-09-26T00:00:00",
    #     "Name": "Presidents Cup",
    #     "Venue": [
    #         "The Royal Montreal Golf Club"
    #     ],
    #     "City": "Ile Bizard",
    #     "State": "PQ",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401656722"
    #     ]
    # },
    # {
    #     "EndDate": "2024-10-06T00:00:00",
    #     "StartDate": "2024-10-03T00:00:00",
    #     "Name": "Sanderson Farms Championship",
    #     "Venue": [
    #         "Country Club of Jackson"
    #     ],
    #     "City": "Jackson",
    #     "State": "MS",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693937",
    #         "https://www.espn.com/golf/player/_/id/1059/luke-list"
    #     ]
    # },
    # {
    #     "EndDate": "2024-10-13T00:00:00",
    #     "StartDate": "2024-10-10T00:00:00",
    #     "Name": "Black Desert Championship",
    #     "Venue": [
    #         "Black Desert Resort Golf Course"
    #     ],
    #     "City": "Ivins",
    #     "State": "UT",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693938"
    #     ]
    # },
    # {
    #     "EndDate": "2024-10-20T00:00:00",
    #     "StartDate": "2024-10-17T00:00:00",
    #     "Name": "Shriners Children's Open",
    #     "Venue": [
    #         "TPC Summerlin"
    #     ],
    #     "City": "Las Vegas",
    #     "State": "NV",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693939",
    #         "https://www.espn.com/golf/player/_/id/4602673/tom-kim"
    #     ]
    # },
    # {
    #     "EndDate": "2024-10-27T00:00:00",
    #     "StartDate": "2024-10-24T00:00:00",
    #     "Name": "ZOZO CHAMPIONSHIP",
    #     "Venue": [
    #         "Accordia Golf Narashino CC"
    #     ],
    #     "City": "Chiba",
    #     "State": "Japan",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693940",
    #         "https://www.espn.com/golf/player/_/id/10592/collin-morikawa"
    #     ]
    # },
    # {
    #     "EndDate": "2024-11-10T00:00:00",
    #     "StartDate": "2024-11-07T00:00:00",
    #     "Name": "World Wide Technology Championship",
    #     "Venue": [
    #         "El Cardonal at Diamante"
    #     ],
    #     "City": "Cabo San Lucas",
    #     "State": "Mexico",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693941",
    #         "https://www.espn.com/golf/player/_/id/9364/erik-van-rooyen"
    #     ]
    # },
    # {
    #     "EndDate": "2024-11-17T00:00:00",
    #     "StartDate": "2024-11-14T00:00:00",
    #     "Name": "Butterfield Bermuda Championship",
    #     "Venue": [
    #         "Port Royal Golf Course"
    #     ],
    #     "City": "Southampton Parish",
    #     "State": "Bermuda",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693942",
    #         "https://www.espn.com/golf/player/_/id/1264/camilo-villegas"
    #     ]
    # },
    # {
    #     "EndDate": "2024-11-24T00:00:00",
    #     "StartDate": "2024-11-21T00:00:00",
    #     "Name": "The RSM Classic",
    #     "Venue": [
    #         "Sea Island Resort (Seaside Course)"
    #     ],
    #     "City": "Saint Simons Island",
    #     "State": "GA",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693943",
    #         "https://www.espn.com/golf/player/_/id/4375972/ludvig-aberg"
    #     ]
    # },
    # {
    #     "EndDate": "2024-12-08T00:00:00",
    #     "StartDate": "2024-12-05T00:00:00",
    #     "Name": "Hero World Challenge",
    #     "Venue": [
    #         "Albany"
    #     ],
    #     "City": "New Providence",
    #     "State": "Bahamas",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693956",
    #         "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
    #     ]
    # },
    # {
    #     "EndDate": "2024-12-15T00:00:00",
    #     "StartDate": "2024-12-12T00:00:00",
    #     "Name": "Grant Thornton Invitational",
    #     "Venue": [
    #         "Tiburón Golf Club"
    #     ],
    #     "City": "Naples",
    #     "State": "FL",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401618459"
    #     ]
    # },
    # {
    #     "EndDate": "2024-12-15T00:00:00",
    #     "StartDate": "2024-12-12T00:00:00",
    #     "Name": "PGA TOUR Q-School presented by Korn Ferry",
    #     "Venue": [
    #         "TPC Sawgrass (Dye's Valley Course)"
    #     ],
    #     "City": "Ponte Vedra Beach",
    #     "State": "FL",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401693957",
    #         "https://www.espn.com/golf/player/_/id/11342/harrison-endycott"
    #     ]
    # },
    # {
    #     "EndDate": "2024-03-10T00:00:00",
    #     "StartDate": "2024-03-07T00:00:00",
    #     "Name": "Puerto Rico Open",
    #     "Venue": [
    #         "Grand Reserve Country Club"
    #     ],
    #     "City": "Rio Grande",
    #     "State": "Puerto Rico",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580339",
    #         "https://www.espn.com/golf/player/_/id/2283/brice-garnett"
    #     ]
    # },
    # {
    #     "EndDate": "2024-05-05T00:00:00",
    #     "StartDate": "2024-05-02T00:00:00",
    #     "Name": "THE CJ CUP Byron Nelson",
    #     "Venue": [
    #         "TPC Craig Ranch"
    #     ],
    #     "City": "McKinney",
    #     "State": "TX",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580348",
    #         "https://www.espn.com/golf/player/_/id/9658/taylor-pendrith"
    #     ]
    # },
    # {
    #     "EndDate": "2024-05-12T00:00:00",
    #     "StartDate": "2024-05-09T00:00:00",
    #     "Name": "Wells Fargo Championship",
    #     "Venue": [
    #         "Quail Hollow Club"
    #     ],
    #     "City": "Charlotte",
    #     "State": "NC",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580349",
    #         "https://www.espn.com/golf/player/_/id/3470/rory-mcilroy"
    #     ]
    # },
    # {
    #     "EndDate": "2024-05-12T00:00:00",
    #     "StartDate": "2024-05-09T00:00:00",
    #     "Name": "Myrtle Beach Classic",
    #     "Venue": [
    #         "Dunes Golf & Beach Club"
    #     ],
    #     "City": "Myrtle Beach",
    #     "State": "SC",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580350",
    #         "https://www.espn.com/golf/player/_/id/4690755/chris-gotterup"
    #     ]
    # },
    # {
    #     "EndDate": "2024-05-19T00:00:00",
    #     "StartDate": "2024-05-16T00:00:00",
    #     "Name": "PGA Championship",
    #     "Venue": [
    #         "Valhalla Golf Club"
    #     ],
    #     "City": "Louisville",
    #     "State": "KY",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580351",
    #         "https://www.espn.com/golf/player/_/id/10140/xander-schauffele"
    #     ]
    # },
    # {
    #     "EndDate": "2024-05-26T00:00:00",
    #     "StartDate": "2024-05-23T00:00:00",
    #     "Name": "Charles Schwab Challenge",
    #     "Venue": [
    #         "Colonial Country Club"
    #     ],
    #     "City": "Fort Worth",
    #     "State": "TX",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580352",
    #         "https://www.espn.com/golf/player/_/id/10058/davis-riley"
    #     ]
    # },
    # {
    #     "EndDate": "2024-06-02T00:00:00",
    #     "StartDate": "2024-05-23T00:00:00",
    #     "Name": "RBC Canadian Open",
    #     "Venue": [
    #         "Hamilton Golf & Country Club"
    #     ],
    #     "City": "Hamilton",
    #     "State": "ON",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580353",
    #         "https://www.espn.com/golf/player/_/id/11378/robert-macintyre"
    #     ]
    # },
    # {
    #     "EndDate": "2024-06-09T00:00:00",
    #     "StartDate": "2024-06-06T00:00:00",
    #     "Name": "the Memorial Tournament pres. by Workday",
    #     "Venue": [
    #         "Muirfield Village Golf Club"
    #     ],
    #     "City": "Dublin",
    #     "State": "OH",
    #     "Links": [
    #         "https://www.espn.com/golf/leaderboard?tournamentId=401580354",
    #         "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
    #     ]
    # },
    {
        "EndDate": "2024-06-16T00:00:00",
        "StartDate": "2024-06-13T00:00:00",
        "Name": "U.S. Open",
        "Venue": [
            "Pinehurst No. 2"
        ],
        "City": "Pinehurst",
        "State": "NC",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580355",
            "https://www.espn.com/golf/player/_/id/10046/bryson-dechambeau"
        ]
    },
    {
        "EndDate": "2024-06-23T00:00:00",
        "StartDate": "2024-06-20T00:00:00",
        "Name": "Travelers Championship",
        "Venue": [
            "TPC River Highlands"
        ],
        "City": "Cromwell",
        "State": "CT",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580356",
            "https://www.espn.com/golf/player/_/id/9478/scottie-scheffler"
        ]
    },
    {
        "EndDate": "2024-06-30T00:00:00",
        "StartDate": "2024-06-27T00:00:00",
        "Name": "Rocket Mortgage Classic",
        "Venue": [
            "Detroit Golf Club"
        ],
        "City": "Detroit",
        "State": "MI",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580357",
            "https://www.espn.com/golf/player/_/id/10863/cam-davis"
        ]
    },
    {
        "EndDate": "2024-07-07T00:00:00",
        "StartDate": "2024-07-04T00:00:00",
        "Name": "John Deere Classic",
        "Venue": [
            "TPC Deere Run"
        ],
        "City": "Silvis",
        "State": "IL",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580358",
            "https://www.espn.com/golf/player/_/id/4602218/davis-thompson"
        ]
    },
    {
        "EndDate": "2024-07-14T00:00:00",
        "StartDate": "2024-07-11T00:00:00",
        "Name": "Genesis Scottish Open",
        "Venue": [
            "The Renaissance Club"
        ],
        "City": "North Berwick",
        "State": "Scotland",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401580359",
            "https://www.espn.com/golf/player/_/id/11378/robert-macintyre"
        ]
    },
    {
        "EndDate": "2024-07-14T00:00:00",
        "StartDate": "2024-07-11T00:00:00",
        "Name": "ISCO Championship",
        "Venue": [
            "Keene Trace Golf Club (Champions Course)"
        ],
        "City": "Nicholasville",
        "State": "KY",
        "Links": [
            "https://www.espn.com/golf/leaderboard?tournamentId=401634279",
            "https://www.espn.com/golf/player/_/id/4589438/harry-hall"
        ]
    }
]

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
    player_detail = WebDriverWait(driver, 2).until(
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

      golfer_tournament_results['Rounds'] = []
      golfer_tournament_results['Rounds'].append(round_detail)

    golfers.append(golfer_tournament_results)

  return golfers

import re
from datetime import datetime

def print_children(element):
    divs = element.find_elements(By.CSS_SELECTOR, "div")
    for div in divs:
        print(div.get_attribute("class"), div.text)

def parse_tournament_header(webpage_data):
  # grab the tournament info from the header
  header = webpage_data.find_element(By.CSS_SELECTOR, "div.Leaderboard__Header")

  par, yardage = None, None

  if check_data_exists(header, "div.Leaderboard__Course__Location__Detail"):
    # grab the par and yardage
    par_yardage = webpage_data.find_element(By.CSS_SELECTOR, "div.Leaderboard__Course__Location__Detail")
    par, yardage = re.findall(r'(\d+)', str(par_yardage.text))

  # what's the status of the tournament? In progress, finished?
  status = webpage_data.find_element(By.CSS_SELECTOR, "div.status")

  # grab the specific element with the text that discloses the tournament status
  status_text = status.find_element(By.CSS_SELECTOR, "span").text

  # grab the tournament info from the header
  purse_previous_winner_text = webpage_data.find_element(By.CSS_SELECTOR, "div.n7").text
  print(purse_previous_winner_text)

  # Split the string based on the expected patterns
  split_values = re.findall(r'[A-Z][^A-Z]*', purse_previous_winner_text)

  purse = None
  previous_winner = None

  # Handle the different possible cases
  if len(split_values) >= 1:

      # Case 1: Only the purse value
      if "Purse" in split_values[0]:
          purse = re.findall(r'(\d+)', split_values[0])
          purse = int(''.join(purse)) if purse else None

      # Case 2: Both purse and previous winner
      if len(split_values) > 1:
          previous_winner = ''.join(split_values[-2:]).strip()
        
      # Case 3: Only previous winner
      if "Purse" not in split_values[0] and len(split_values) > 1:
          previous_winner = ' '.join(split_values[-2:]).strip()

  return {
      "Purse": purse,
      "PreviousWinner": previous_winner,
      "Par": par,
      "Yardage": yardage
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

def get_tournament_status(start_date_str, end_date_str):
    # Define the local timezone
    local_timezone = pytz.timezone('US/Eastern')
    
    # Get the current local time
    current_local_time = datetime.now(local_timezone)
    
    # Parse the start and end date strings into datetime objects
    start_date = datetime.fromisoformat(start_date_str).replace(tzinfo=local_timezone)
    end_date = datetime.fromisoformat(end_date_str).replace(tzinfo=local_timezone)
    
    # Determine if the tournament is in progress or completed
    tournament_info = {
        "isInProgress": start_date <= current_local_time < end_date,
        "isCompleted": current_local_time >= end_date
    }
    
    return tournament_info

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

        item.update(get_tournament_status(item["StartDate"], item["EndDate"]))

        # Load page
        driver.get(item['Links'][0])

        # retrieve purse, previous winner, par, and yardage
        item.update(parse_tournament_header(driver))

        if check_data_exists(driver, "div.leaderboard_no_data"):
            print("here")
            parsed_tournaments.append(item)
            name = item['Name'].split(' ')
            name = '-'.join(name)
            save_tournament(name, item)
            continue

        competitors_table = driver.find_element(By.CSS_SELECTOR, "div.competitors")

        responsive_tables = competitors_table.find_elements(By.CSS_SELECTOR, "div.ResponsiveTable")

        # determine the amount of headers within the responsive table
        table_headers = responsive_tables[-1].find_elements(By.CSS_SELECTOR, "th")

        # test if it's a legit scoreboard if it's before the tourney and they are just showing tee times.
        if len(table_headers) <= 3:
          # record the tee times
          data = responsive_tables[-1].find_elements(By.CSS_SELECTOR, "tr.Table__TR")
          item["Golfers"] = []
          for datap in data[1:]:
              tee_times = datap.text.split('\n')  # Split the text into lines
              name = tee_times[0]
              tee_time_str = tee_times[1]
              tee_time = datetime.strptime(tee_time_str, "%I:%M %p")
              # Convert datetime to string before appending
              tee_time_str = tee_time.strftime("%Y-%m-%d %H:%M:%S")
              item["Golfers"].append({"name": name, "tee_time": tee_time_str})
          parsed_tournaments.append(item)
          continue

        # determine if playoff holes took place
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
