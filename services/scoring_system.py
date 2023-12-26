from .Base import Base
import json
import os

class ScoringSystem(Base):
    def __init__(self, **kwargs):
        # Initialization code
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def build_temp_player_dict(player: dict) -> dict[str, int]:
        player_dict = {
                'player_name': player['Name'],
                'player_id': player['PlayerID'],
                'fedex_points': player['FedExPoints'],
                'birdies': 0,
                'pars': 0,
                'bogeys': 0,
                'score': 0,
                'double_bogeys': 0,
                'hole_in_ones': 0,
                'double_eagles': 0,
                'eagles': 0,
                'worse_than_double_bogeys': 0,
                'round_1_score': 0,
                'round_2_score': 0,
                'round_3_score': 0,
                'round_4_score': 0
        }

        return player_dict

    # build a summary of a tournament and the stats for each player    
    def fetch_testing_data(self, read_file, write_file):
        # read from the json files located in the data directory
        data = self.r_or_w_to_file('r', read_file)

        # get the tournament info
        tournament = data["Tournament"]

        # can use tournament objs when we have a db up and running
        tournament_results = {
            'tournament_name': tournament["Name"],
            'Location': tournament["Location"],
            'players': [] 
        }
 
        # Iterate over each player in the 'Players' array
        # when we come up with a db, we can use actual player objects
        for player in data['Players']:

            # build the dict for holding all the player's info
            player_dict = self.build_temp_player_dict(player)

            if self.fedex_multiplier and player_dict['fedex_points']:
                score = int((player_dict['fedex_points'] * self.fedex_multiplier))
                player_dict['score'] += score

            # Iterate over each round in the player's 'Rounds' array
            for round in player['Rounds']:
                for hole in round['Holes']:
                    round_number = round['Number']
                    if hole["Birdie"]:
                        player_dict['birdies'] += 1
                        player_dict['score'] += self.birdie
                        player_dict[f'round_{round_number}_score'] -= 1
                    elif hole["IsPar"]:
                        player_dict['pars'] += 1
                        player_dict['score'] += self.par
                    elif hole["Bogey"]:
                        player_dict['bogeys'] += 1
                        player_dict['score'] += self.bogey
                        player_dict[f'round_{round_number}_score'] += 1
                    elif hole["DoubleBogey"]:
                        player_dict['double_bogeys'] += 1
                        player_dict['score'] += self.double_bogey
                        player_dict[f'round_{round_number}_score'] += 2
                    elif hole["HoleInOne"]:
                        player_dict['hole_in_ones'] += 1
                        player_dict['score'] += self.hole_in_one
                        score = 0
                        score -= (hole['Par'] - 1)
                        player_dict[f'round_{round_number}_score'] -= score
                    elif hole["DoubleEagle"]:
                        player_dict['double_eagles'] += 1
                        player_dict['score'] += self.double_eagle
                        player_dict[f'round_{round_number}_score'] -= 3
                    elif hole["Eagle"]:
                        player_dict['eagles'] += 1
                        player_dict['score'] += self.eagle
                        player_dict[f'round_{round_number}_score'] -= 2
                    else:
                        # Handle the case for WorseThanDoubleBogey or other scenarios
                        player_dict['worse_than_double_bogeys'] += 1
                        player_dict['score'] += self.worse_than_double_bogey
                        player_dict[f'round_{round_number}_score'] += 3

                    # what edge case does this handle?
                    if not player_dict['bogeys'] and not player_dict['double_bogeys'] and not player_dict['worse_than_double_bogeys']:
                        player_dict['score'] += 3

            tournament_results['players'].append(player_dict)

        
        # Sort the players based on their round_1_score in descending order without modifying the original list
        sorted_players = sorted(tournament_results['players'], key=lambda player: player['round_1_score'], reverse=True)

        # Get the player with the highest score on day 1 from the sorted list and add 10 points
        sorted_players[0]['score'] += 10

        # Sort the players based on their round_1_score in descending order without modifying the original list
        sorted_players_2 = sorted(tournament_results['players'], key=lambda player: player['round_2_score'], reverse=True)

        # Get the player with the highest score on day 1 from the sorted list and add 10 points
        sorted_players_2[0]['score'] += 10
        
        # Sort the players based on their round_1_score in descending order without modifying the original list
        sorted_players_3 = sorted(tournament_results['players'], key=lambda player: player['round_3_score'], reverse=True)

        # Get the player with the highest score on day 1 from the sorted list and add 10 points
        sorted_players_3[0]['score'] += 10
        
        # Sort the players based on their round_1_score in descending order without modifying the original list
        sorted_players_4 = sorted(tournament_results['players'], key=lambda player: player['round_4_score'], reverse=True)

        # Get the player with the highest score on day 1 from the sorted list and add 10 points
        sorted_players_4[0]['score'] += 10

        # write the results for each round a player plays in the tournament to 
        # a json file
        self.r_or_w_to_file('w', write_file, tournament_results)

    def r_or_w_to_file(self, r_or_w, file_name, tournament_results=None):
        # Get the absolute path of the current script
        dir_path = os.path.dirname(os.path.abspath(__file__))

        if r_or_w == "r":
            try:
                # Construct the absolute path to the data file
                file_path = os.path.join(dir_path, '..', 'data', file_name)

                # read the file and return its response
                with open(file_path, "r") as file:
                    data = json.load(file)
                    return data
            except Exception as e:
                print(f"An error ocurred: {e}")

        elif r_or_w == 'w':
            output_file_name = f"../results/{file_name}"


            try:
                # Construct the absolute path to the data file
                file_path = os.path.join(dir_path, '..', 'results', output_file_name)

                # Now, 'players' contains the summarized data for each player's rounds
                # Writing the results to a file
                with open(file_path, "w") as outfile:
                    json.dump(tournament_results, outfile, indent=4)

                # Add the output file to .gitignore
                gitignore_file = "../.gitignore"
                with open(gitignore_file, "a") as gitignore:
                    gitignore.write(f"\n{output_file_name}")

                print(f"Data written to {output_file_name}")

            except Exception as e:
                print(f"An error occurred: {e}")


    def fetch_data(self, url):
        response = super().fetch_data(url)
        # Additional processing specific to ScoringSystem
        # processed_data = self.process_data(response)
        # return processed_data
        return response

    @staticmethod
    def process_data(self, response):
        # Process the response and return processed data
        # determine how the scores should be calculated
        # make a call to the present summary method to present the data in some fashion
        pass

    @staticmethod
    def calculate_scores(self, data):
        # Code to calculate scores based on the data
        pass
        

    @staticmethod
    def present_summary(self, scores):
        # Code to format and present the summary of scores
        pass

