import os
import sys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db
from scrapers.tourney_scraper import parse_leaderboard

def fix_golfer_total_scores():
    all_golfer_tournament_details = db.golfertournamentdetails.find()

    for golfer_details in all_golfer_tournament_details:
        tournament = db.tournaments.find_one({ "_id": golfer_details["TournamentId"] })

        golfer_dict = dict(golfer_details)

        if len(golfer_details['Rounds']) < 2:
            golfer_dict['WD'] = True
            golfer_dict['Cut'] = False
        elif len(golfer_details['Rounds']) == 2:
            golfer_dict['WD'] = False
            golfer_dict['Cut'] = True
        else:
            golfer_dict['WD'] = False
            golfer_dict['Cut'] = False

        score_total = 0

        for r in golfer_details["Rounds"]:
            curr_r = db.rounds.find({ "_id": r })

            score_total += curr_r["Score"] 

        {
}

def fix_golfer_scores_in_tournaments():
    pass

def fetch_golfer_name(golfer_tournament_details_id):
    golfer_tourney_details = db.golfertournamentdetails.find_one({ "_id": golfer_tournament_details_id })

    return golfer_tourney_details["Name"]

# Query to find rounds with less than 18 holes played
rounds_with_less_than_18_holes = db.rounds.find({"Holes": {"$exists": True, "$not": {"$size": 18}}})

tournament_details = {}

# Iterate and print the results
for r in rounds_with_less_than_18_holes:
    if r["TournamentId"] in tournament_details:
        tournament_details[r["TournamentId"]].append(r["GolferTournamentDetailsId"])
    else:
        tournament_details[r["TournamentId"]] = [r["GolferTournamentDetailsId"]]
print(tournament_details)

options = Options()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.headless = True

options.add_argument('--headless=new')

# Only pass options once when creating the WebDriver instance
wd = webdriver.Chrome(options=options)

driver = wd

for tournament_id, tournament_details_ids in tournament_details.items():
    tournament = db.tournaments.find_one({ "_id": tournament_id })
    golfer_names = [fetch_golfer_name(t_detail) for t_detail in tournament_details_ids]

    print(golfer_names)

    # Load page
    driver.get(tournament['Links'][0])

    competitors_table = driver.find_element(By.CSS_SELECTOR, "div.competitors")

    responsive_tables = competitors_table.find_elements(By.CSS_SELECTOR, "div.ResponsiveTable")

    golfers = parse_leaderboard(responsive_tables[-1], driver, golfer_names)

    for golfer in golfers:
        print({"Name": golfer["Name"], "Score": golfer["Score"], "TournamentId": tournament_id})

driver.quit()
