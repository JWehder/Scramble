import React, { useEffect, useState, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../../store";
import { getLeague } from "../state/leagueSlice";
import { useParams, useNavigate } from "react-router-dom";
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
import { FantasyLeagueTournamentsResponse } from "../../../types/fantasyLeagueTournamentsResponse";

interface LeagueSettingsProps {
  saveLeagueSettings: (settings: LeagueSettings) => void;
}

const LeagueSettingsPage: React.FC<LeagueSettingsProps> = ({
    saveLeagueSettings
  }) => {
  const navigate = useNavigate();
  const { leagueId } = useParams<string>();
  const isEditMode = Boolean(leagueId);

  const [currentTab, setCurrentTab] = useState<string>("General");
  const [settings, setSettings] = useState<LeagueSettings | undefined>();
  const [isCommissioner, setIsCommissioner] = useState<boolean>(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const selectedLeague = useSelector((state: RootState) => state.leagues.selectedLeague);
  const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);
  const [tournaments, setTournaments] = useState<FantasyLeagueTournamentsResponse | Tournament[]>();

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
              `/api/fantasy_league_seasons/${selectedLeague.CurrentFantasyLeagueSeasonId}/pro_season/competition_schedule`
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
      const fetchData = async () => {
        try {
          const settingsResponse = isEditMode
            ? selectedLeague?.LeagueSettings
            : await axios.get('/default_league_settings').then((res) => res.data);
    
          const tournamentsResponse = await axios.get(
            isEditMode
              ? `/api/fantasy_league_seasons/${selectedLeague?.CurrentFantasyLeagueSeasonId}/pro_season/competition_schedule`
              : `/api/pro_seasons/${settingsResponse.ProSeasonId}/competition_schedule`
          );
    
          setSettings(settingsResponse);
          setTournaments(tournamentsResponse.data);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
    
      fetchData();
    }, [isEditMode, selectedLeague]);

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

  const displayStarters = useMemo(() => {
    const maxGolfers = settings?.MaxGolfersPerTeam ?? 0;
    const numBench = settings?.NumOfBenchGolfers ?? 0;
  
    return Array.from(
      { length: Math.max(0, maxGolfers - numBench - 2 + 1) },
      (_, i) => i + 2
    );
  }, [settings]);
  
  const displayBenchGolfers = useMemo(() => {
    const maxGolfers = settings?.MaxGolfersPerTeam ?? 0;
    const numStarters = settings?.NumOfStarters ?? 0;
  
    return Array.from(
      { length: Math.max(0, maxGolfers - numStarters - 1 + 1) },
      (_, i) => i + 1
    );
  }, [settings]);

  const renderInput = (label: string, name: keyof LeagueSettings, type: string, value: any, options: Array<string> | Array<number> | null, disabled = false, obj: Record<string, number> | undefined = undefined) => {
      if (options) {
        console.log(disabled)
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
                  } ${disabled ? "cursor-not-allowed opacity-50" : "hover:brightness-110"}`}
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

      <div className="flex flex-row items-center p-4 w-full">
        <div className="flex justify-start w-1/3">
          <BackButton
            size="8"
            color="stroke-light"
            handleBackClick={() => navigate(`/leagues/${leagueId}`)}
          />
        </div>
        <div className="flex justify-center w-1/3">
          <h1 className="text-3xl font-bold text-center text-light">
            league settings
          </h1>
        </div>
        <div className="w-1/3"></div>
      </div>


        {/* Tabs for Navigation */}
        <div className="flex justify-center mb-6 text-light space-x-2">
            {["General", "Draft", "Scoring", "Team Management", "Tournaments"].map((tab) => (
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
        {currentTab === "General" && (
            <div className="space-y-6">
                {renderInput(
                "Sport",
                "Sport",
                "text",
                settings?.Sport,
                ["Golf"],
                !isCommissioner
                )}
                { renderInput(
                "Pro Season",
                "ProSeason",
                "number",
                settings?.ProSeason,
                ["PGA Tour"],
                !isCommissioner
                )}
                {renderInput("Number of Teams", "NumberOfTeams", "number", settings?.NumberOfTeams, [8, 9, 10, 12, 14, 16], !isCommissioner)}
            </div>
        )}

        {/* Content */}
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
                  settings?.PointsPerScore &&
                  Object.keys(settings.PointsPerScore).length > 0 &&
                  Object.keys(settings.PointsPerScore).map((scoreType) =>
                    renderInput(
                      `Points for ${scoreType}`,
                      `PointsPerScore[${scoreType}]` as keyof LeagueSettings,
                      "number",
                      [1, 2, 3, 4, 5, 6],
                      null,
                      !isCommissioner
                    )
                  )}


                {renderInput("Game", "ScoreType", "text", settings?.DefaultPointsForNonPlacers, ["Match Play", "Standard", "Customized Scoring"], !isCommissioner)}
                {renderInput("Default Points for Non-Placers (Withdrawals or something else)", "DefaultPointsForNonPlacers", "number", settings?.DefaultPointsForNonPlacers, [0, 1, 2, 3, 4], !isCommissioner)}
                {renderInput("Cut Penalty", "CutPenalty", "text", settings?.CutPenalty, Object.keys(cutsObj), !isCommissioner, cutsObj)}
            </div>
            )}

            {currentTab === "Team Management" && (
            <div className="space-y-6 ">
                {renderInput("Cut Penalty (Strokes added for missing the cut)", "CutPenalty", "number", settings?.CutPenalty, [0, 1, 2, 3], !isCommissioner)}
                {renderInput("Number of Bench Golfers", "NumOfBenchGolfers", "number", settings?.NumOfBenchGolfers, displayBenchGolfers, !isCommissioner)}
                {renderInput("Number of Starters", "NumOfStarters", "number", settings?.NumOfStarters, displayStarters, !isCommissioner)}
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

            {currentTab === "Tournaments" && tournaments &&
            (
                
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
                tournaments ?
                <>
                    <SettingsProvider>
                        { !isEditMode ?
                          <TournamentScheduleTable
                          setSelectedTournament={setSelectedTournament}
                          tournaments={tournaments as Tournament[]}
                          />
                          :
                          <EditTournamentsButtons 
                          setTournaments={setTournaments}
                          fantasyLeagueSeasonId={selectedLeague?.CurrentFantasyLeagueSeasonId!}
                          />
                        }

                        {
                          tournaments && 
                          typeof tournaments === "object" && 
                          "pastFantasyLeagueTournaments" in tournaments &&
                          tournaments?.pastFantasyLeagueTournaments.length > 0 && (
                            // Render your tournamentScheduleTable here
                            <>
                              <h1 className="text-2xl font-bold p-4 text-center text-light">
                                past fantasy league events
                              </h1>
                              <TournamentScheduleTable 
                              setSelectedTournament={setSelectedTournament}
                              tournaments={tournaments?.pastFantasyLeagueTournaments}
                              />
                            </>
                          )
                        }
                        {
                          tournaments && 
                          typeof tournaments === "object" && 
                          "upcomingFantasyLeagueTournaments" in tournaments &&
                          tournaments?.upcomingFantasyLeagueTournaments.length > 0 && (
                            // Render your tournamentScheduleTable here
                            <>
                              <h1 className="text-2xl font-bold p-4 text-center text-light">
                                upcoming fantasy league events
                              </h1>
                              
                              <TournamentScheduleTable 
                              setSelectedTournament={setSelectedTournament}
                              tournaments={tournaments?.upcomingFantasyLeagueTournaments}
                              />
                            </>
                          )
                        }
                        {
                          tournaments && 
                          typeof tournaments === "object" && 
                          "upcomingProSeasonTournaments" in tournaments &&
                          tournaments?.upcomingProSeasonTournaments.length > 0 && (
                            // Render your tournamentScheduleTable here
                            <>
                              <h1 className="text-2xl font-bold p-4 text-center text-light">
                                upcoming pro events
                              </h1>
                              <TournamentScheduleTable 
                              setSelectedTournament={setSelectedTournament}
                              tournaments={tournaments?.upcomingProSeasonTournaments}
                              />
                            </>

                          )
                        }

                    </SettingsProvider>
                </>
                :
                <LoadingScreen />
                )
            )}
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
  );
};

export default LeagueSettingsPage;
