from services.Scoring_System import ScoringSystem
import os

os.getenv('SPORTS_API_KEY')

def main():
    scoring_system_1 = ScoringSystem(
        fedex_multiplier=0.05,
        birdie=2,
        eagle=5,
        double_eagle=8,
        par=1,
        bogey=-1,
        double_bogey=-3,
        low_round=10,
        second_lowest=5,
        bogey_free=3,
        worse_than_double_bogey=-5,
        hole_in_one=10
    )

    scoring_system_1.fetch_testing_data("WM.json", "WM.json")
    scoring_system_1.fetch_testing_data("Honda.json", "Honda.json")
    scoring_system_1.fetch_testing_data("Genesis.json", "Genesis.json")

    # Birdie is one and par is zero, fedex multiplier is 0.025
    scoring_system_2 = ScoringSystem(
        fedex_multiplier=0.025,
        birdie=1,
        eagle=5,
        double_eagle=8,
        par=0,
        bogey=-1,
        double_bogey=-3,
        low_round=10,
        second_lowest=5,
        bogey_free=3,
        worse_than_double_bogey=-5,
        hole_in_one=10
    )

    scoring_system_2.fetch_testing_data("WM.json", "WM_2.json")
    scoring_system_2.fetch_testing_data("Honda.json", "Honda_2.json")
    scoring_system_2.fetch_testing_data("Genesis.json", "Genesis_2.json")

    scoring_system_3 = ScoringSystem(
        fedex_multiplier=0,
        birdie=2,
        eagle=5,
        double_eagle=8,
        par=1,
        bogey=-1,
        double_bogey=-3,
        low_round=10,
        second_lowest=5,
        bogey_free=3,
        worse_than_double_bogey=-5,
        hole_in_one=10
    )

    scoring_system_3.fetch_testing_data("WM.json", "WM_3.json")
    scoring_system_3.fetch_testing_data("Honda.json", "Honda_3.json")
    scoring_system_3.fetch_testing_data("Genesis.json", "Genesis_3.json")

if __name__ == '__main__':
    main()