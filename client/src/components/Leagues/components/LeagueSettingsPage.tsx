import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../../store";
import { getLeague } from "../state/leagueSlice";
import { useParams } from "react-router-dom";
import { LeagueSettings } from "../../../types/leagueSettings";
import TournamentScheduleTable from "../../User/components/home/TournamentScheduleTable";
import { Tournament } from "../../../types/tournaments";
import Tourney from "../../User/components/home/Tourney";
import BackButton from "../../Utils/components/BackButton";
import GolferTournamentDetailsTable from "../../Golfers/components/GolferTournamentDetailsTable";
import { SettingsProvider } from "../settingsContext";
import LoadingScreen from "../../Utils/components/LoadingScreen";
import axios from "axios";
import EditTournamentsButtons from "./EditTournamentsButtons";

interface LeagueSettingsProps {
  saveLeagueSettings: (settings: LeagueSettings) => void;
}

interface FantasyLeagueTournamentsResponse {
    pastFantasyLeagueTournaments: Tournament[],
    upcomingFantasyLeagueTournaments: Tournament[],
    upcomingProSeasonTournaments: Tournament[]
}

const LeagueSettingsPage: React.FC<LeagueSettingsProps> = ({
    saveLeagueSettings
  }) => {
    const { leagueId } = useParams<string>();
    const isEditMode = Boolean(leagueId);
  
    const [currentTab, setCurrentTab] = useState<string>("Draft");
    const [settings, setSettings] = useState<LeagueSettings | undefined>();
    const [isCommissioner, setIsCommissioner] = useState<boolean>(false);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});
    const selectedLeague = useSelector((state: RootState) => state.leagues.selectedLeague);
    const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);
    const [tournaments, setTournaments] = useState<FantasyLeagueTournamentsResponse | []>();

    const dispatch = useDispatch<AppDispatch>();
  
    useEffect(() => {
        if (isEditMode && !selectedLeague) {
          dispatch(getLeague(leagueId!));
        }
      }, [leagueId, isEditMode, dispatch, selectedLeague]);
      
      useEffect(() => {
        if (isEditMode && selectedLeague) {
          setSettings(selectedLeague.LeagueSettings);
      
          // Fetch associated tournaments
          const fetchTournaments = async () => {
            try {
              const response = await axios.get(
                `/fantasy_league_seasons/${selectedLeague.CurrentFantasyLeagueSeasonId}/pro_season/competition_schedule`
              );
              setTournaments(response.data); // Assuming `setTournaments` exists for tournament state
            } catch (error) {
              console.error("Error fetching tournaments:", error);
            }
          };
          fetchTournaments();
        } 
      }, [isEditMode, selectedLeague]);
      
      useEffect(() => {
        if (!isEditMode) {
          const fetchInitialSettings = async () => {
            try {
              const response = await axios.get('/default_league_settings');
              setSettings(response.data);
              const tournamentsResponse = await axios.get()
            } catch (error) {
              console.error("Error fetching default settings:", error);
            }
          };
          fetchInitialSettings();
        }
      }, [isEditMode]);

    const handleInputChange = (field: keyof LeagueSettings, value: any) => {
        if (!settings) return;
    
        // Validation logic
        let errorMessage = "";
        if (field === "NumOfStarters" && value > settings.MaxGolfersPerTeam) {
          errorMessage = "Number of starters cannot exceed max golfers per team.";
        } else if (field === "NumOfBenchGolfers" && value > settings.MaxGolfersPerTeam) {
            errorMessage = "Number of bench golfers cannot exceed max golfers per team.";
        } else if (field === "NumberOfTeams" && value % 2 !== 0 && settings.ScoreType === "Match Play") {
            errorMessage
        }
    
        // Set error if validation fails
        if (errorMessage) {
          setErrors((prev) => ({ ...prev, [field]: errorMessage }));
          return;
        }
    
        // Clear error for valid input and update state
        setErrors((prev) => ({ ...prev, [field]: "" }));
        setSettings((prev) => ({ ...prev!, [field]: value }));
    };

    const handleSave = () => {
        if (settings) saveLeagueSettings(settings);
    };

    const timePerDraftPickObj = {
        "30 secs": 30, 
        "1 min": 60, 
        "1 min 30 secs": 90, 
        "2 mins": 120, 
        "1 hour": 3600, 
        "3 hours": 10800, 
        "6 hours": 21600
    }

    const cutsObj = {
        "+1": 1,
        "+2": 2,
        "+3": 3,
        "+4": 4
    }

    const displayStarters = () => {
        const maxGolfers = settings?.MaxGolfersPerTeam ?? 0;
        const numBench = settings?.NumOfBenchGolfers ?? 0;

        return  Array.from(
            { length: Math.max(0, maxGolfers - numBench - 2 + 1) }, 
            (_, i) => i + 2
        );
    }

    const displayBenchGolfers = () => {
        const maxGolfers = settings?.MaxGolfersPerTeam ?? 0;
        const numStarters = settings?.NumOfStarters ?? 0;

        return  Array.from(
            { length: Math.max(0, (maxGolfers - numStarters) - 1 + 1) }, 
            (_, i) => i + 1
        );
    }

    const renderInput = (label, name, type, value, options: Array<string> | Array<number> | null, disabled = false, obj: Object | undefined = undefined) => {
        if (options) {
          return (
            <div className="space-y-2">
              <label className="text-sm font-semibold">{label}</label>
              <div className="flex flex-wrap gap-2">
                {options.map((option) => ( 
                  <button
                    key={option}
                    onClick={() => handleInputChange(name, (obj ? obj[option] : option))}
                    className={`px-4 py-2 rounded ${
                      value === (obj ? obj[option] : option) ? "bg-highlightBlue text-light" : "bg-light text-dark"
                    } ${isCommissioner ? "cursor-not-allowed opacity-50" : "hover:brightness-110"}`}
                    disabled={disabled}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          );
        }
    
        return (
          <div className="space-y-2">
            <label className="text-sm font-semibold">{label}</label>
            <input
              type={type}
              value={value}
              onChange={(e) => handleInputChange(name, type === "number" ? parseInt(e.target.value) : e.target.value)}
              className="w-full p-2 rounded bg-light text-dark focus:ring focus:ring-highlightBlue"
              disabled={disabled}
            />
          </div>
        );
    };

    if (!settings) {
        return <LoadingScreen />
    };
    
    return (
    <div className="w-full min-h-screen bg-gradient-to-b from-dark to-middle text-light flex flex-col items-center px-6 py-10 shadow-2xl font-PTSans min-w-[750px]">
        <div className="w-full max-w-4xl bg-middle p-6 rounded-lg shadow-xl font-PTSans">

        <h1 className="text-3xl font-bold mb-6 text-center text-light">League Settings</h1>

        {/* Tabs for Navigation */}
        <div className="flex justify-center mb-6 text-light space-x-2">
            {["Draft", "Scoring", "Team Management", "Tournaments"].map((tab) => (
            <button
                key={tab}
                onClick={() => setCurrentTab(tab)}
                className={`px-6 py-2 rounded-t-lg ${
                currentTab === tab ? "bg-dark text-light" : "bg-light text-dark hover:brightness-125"
                }`}
            >
                {tab}
            </button>
            ))}
        </div>

        {/* Content */}
        <div className="bg-middle p-6 rounded-b-lg text-light">
        {currentTab === "General" && (
            <div className="space-y-6">
                {renderInput(
                "Sport",
                "Sport",
                "number",
                settings?.Sport,
                ["Golf"],
                !isCommissioner
                )}
                { renderInput(
                "Sport",
                "Pro Season",
                "number",
                settings?.SeasonId,
                ["PGA Tour"],
                !isCommissioner
                )}
            </div>
        )}
        </div>

        {/* Content */}
        <div className="bg-middle p-6 rounded-b-lg text-light">
            {currentTab === "Draft" && (
            <div className="space-y-6">
                {renderInput(
                "Draft Frequency (Free Agent Draft every X amount of tournaments after first draft)",
                "DraftingFrequency",
                "number",
                settings?.DraftingFrequency,
                [1, 2, 3, 4],
                !isCommissioner
                )}
                {renderInput(
                "Draft Start Day",
                "DraftStartDayOfWeek",
                "text",
                settings?.DraftStartDayOfWeek,
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                !isCommissioner
                )}
                 {renderInput(
                "Time Per Draft Pick",
                "SecondsPerDraftPick",
                "text",
                settings?.SecondsPerDraftPick,
                Object.keys(timePerDraftPickObj),
                !isCommissioner,
                timePerDraftPickObj
                )}
                {renderInput("Draft Time", "DraftStartTime", "time", settings?.DraftStartTime, null, !isCommissioner)}
                {renderInput("Snake Draft", "SnakeDraft", "checkbox", settings?.SnakeDraft, null, !isCommissioner)}
            </div>
            )}

            {currentTab === "Scoring" && (
            <div className="space-y-6">
                {renderInput(
                "Points Type",
                "PointsType",
                "text",
                settings?.PointsType,
                ["Strokes", "Points per Score", "Matchup Win"],
                !isCommissioner
                )}
                {settings?.PointsType === "Points per Score" &&
                Object.entries(settings?.PointsPerScore).map(([scoreType, points]) =>
                    renderInput(`Points for ${scoreType}`, `PointsPerScore.${scoreType}`, "number", points, null, !isCommissioner)
                )}

                {renderInput("Game", "ScoreType", "text", settings?.DefaultPointsForNonPlacers, ["Match Play", "Standard", "Customized Scoring"], !isCommissioner)}
                {renderInput("Default Points for Non-Placers (Withdrawals or something else)", "DefaultPointsForNonPlacers", "number", settings?.DefaultPointsForNonPlacers, [0, 1, 2, 3, 4], !isCommissioner)}
                {renderInput("Cut Penalty", "CutPenalty", "text", settings?.CutPenalty, Object.keys(cutsObj), !isCommissioner, cutsObj)}
            </div>
            )}

            {currentTab === "Team Management" && (
            <div className="space-y-6 ">
                {renderInput("Cut Penalty (Strokes added for missing the cut)", "CutPenalty", "number", settings?.CutPenalty, [0, 1, 2, 3], !isCommissioner)}
                {renderInput("Number of Teams", "NumberOfTeams", "number", settings?.NumberOfTeams, [8, 9, 10, 12, 14, 16], !isCommissioner)}
                {renderInput("Number of Bench Golfers", "NumOfBenchGolfers", "number", settings?.NumOfBenchGolfers, displayBenchGolfers(), !isCommissioner)}
                {renderInput("Number of Starters", "NumOfStarters", "number", settings?.NumOfStarters, displayStarters(), !isCommissioner)}
                {renderInput("Force Drops", 
                "ForceDrops", 
                "number", 
                settings?.ForceDrops, 
                Array.from(
                    { length: Math.max(0, settings!.MaxGolfersPerTeam - 1 + 1) }, 
                    (_, i) => i + 1
                ), 
                !isCommissioner)}
                {renderInput("Max Golfers Per Team", "MaxGolfersPerTeam", "number", settings?.MaxGolfersPerTeam, [2, 3, 4, 5, 6], !isCommissioner)}
                {renderInput(
                "Waiver Type",
                "WaiverType",
                "text",
                settings?.WaiverType,
                ["Reverse Standings", "Rolling Waivers"],
                !isCommissioner
                )}

                {renderInput(
                "Waiver Deadline",
                "WaiverDeadline",
                "text",
                settings?.WaiverDeadline,
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                !isCommissioner
                )}
            </div>
            )}

            <div className="bg-middle rounded-b-lg text-light">
                {currentTab === "Tournaments" && (
                    
                    selectedTournament ? (
                    <>
                        <span className="inline-flex items-center">
                        <BackButton
                            size="8"
                            color="stroke-light"
                            handleBackClick={() => setSelectedTournament(null)}
                        />
                        </span>
                        <Tourney tournament={selectedTournament} />
                        <GolferTournamentDetailsTable
                        tournamentId={selectedTournament.id}
                        holeData={selectedTournament.Holes}
                        />
                    </>
                    ) : (
                    <>
                        <SettingsProvider>
                            <EditTournamentsButtons 
                            setTournaments={setTournaments}
                            fantasyLeagueSeasonId={selectedLeague?.CurrentFantasyLeagueSeasonId}
                            />
                            <TournamentScheduleTable
                            setSelectedTournament={setSelectedTournament}
                            tournaments={tournaments}
                            />
                        </SettingsProvider>
                    </>
                    )
                )}
            </div>
        </div>


            {/* Save Button */}
            <div className="flex justify-center mt-6">
                <button
                onClick={handleSave}
                className="bg-light text-dark px-6 py-3 rounded-lg shadow-2xl"
                disabled={!isCommissioner}
                >
                Save Settings
                </button>
            </div>
        </div>
    </div>
    );
};

export default LeagueSettingsPage;
