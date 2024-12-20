import React, { useEffect } from 'react';
import Roster from '../../Teams/components/Roster';
import { useState } from 'react';
import Leaderboard from '../../User/components/home/Leaderboard';
import Golfers from '../../Golfers/components/Golfers';
import SquigglyUnderline from "../../Utils/components/SquigglyLine"
import Schedule from '../../Periods/components/Schedule';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import Button from '../../Utils/components/Button';
import BackButton from '../../Utils/components/BackButton';
import NextButton from '../../Utils/components/NextButton';
import { AppDispatch, RootState } from '../../../store';
import Modal from '../../Utils/components/Modal';
import { resetSelectedGolfer } from '../../Golfers/state/golferSlice';
import { useQueryClient } from '@tanstack/react-query';
import PlayerPage from '../../Golfers/components/player/PlayerPage';
import { getLeague } from '../state/leagueSlice';
import NewStandings from "./NewStandings"
import { setSelectedTeam } from '../../Teams/state/teamsSlice';
import { Team } from '../../../types/teams';
import { useFetchUpcomingPeriods } from '../../../hooks/periods';

export default function LeagueDashboard() {
    const dispatch = useDispatch<AppDispatch>();
    const { leagueId } = useParams<string>();
    const queryClient = useQueryClient();
    const navigate = useNavigate();
    const location = useLocation();

    const [activeComponent, setActiveComponent] = useState<string>("Schedule");
    const [userSelectedTeam, setUserSelectedTeam] = useState<Team | null>(null);

    const selectedGolfer = useSelector((state: RootState) => state.golfers.selectedGolfer);
    const selectedLeague = useSelector((state: RootState) => state.leagues.selectedLeague);

    const user = useSelector((state: RootState) => state.users.user);
    const leagueTeams = useSelector((state: RootState) => state.teams.leaguesTeams)
    const userTeam = useSelector((state: RootState) => state.teams.userSelectedTeam)

    const onClose = () => {
        dispatch(resetSelectedGolfer());
        queryClient.invalidateQueries({ queryKey: ['golferTournamentDetails'] });
    };

    useEffect(() => {
        if (leagueId) {
            dispatch(getLeague(leagueId))
        };

    }, [leagueId]);

    useEffect(() => {
        if (leagueTeams) {
            dispatch(setSelectedTeam(leagueId))
        }
    }, [leagueTeams, user]);

    const goToSettings = () => {
        // Append "/settings" to the current path
        navigate(`${location.pathname}/settings`);
    };

    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        isError,
        error,
      } = useFetchUpcomingPeriods(leagueId!);

    return (
        <div className='flex justify-center items-center w-full flex-col min-w-[950px] bg-dark'>
            <div className='flex-row h-16 w-11/12 mb-5 flex items-center text-light font-PTSans pt-3 min-w-[850px]'>
                <div className='flex flex-col w-1/3'>
                    <div className='flex justify-center items-center flex-row'>
                        <h1 className='text-xl lg:text-4xl md:text-2xl sm:text-xl'>
                            {selectedLeague?.Name}
                        </h1>
                    </div>

                    <div className='flex justify-center items-center flex-row'>
                        <BackButton 
                        size="4" 
                        color={"stroke-light"} 
                        handleBackClick={() => console.log("Clicked me")}
                        />
                        <NextButton 
                        size="4" 
                        color={"stroke-light"} 
                        handleNextClick={() => console.log("Clicked me")}
                        />
                    </div>
                </div>

                <div className='p-5 flex items-center justify-center w-1/3'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Standings"}, {name:"Team"}, {name:"Tournaments"}, {name:"Golfers"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                </div>

                <div className='w-1/3 flex justify-center items-center'>
                    <Button
                    variant="secondary"
                    type="null"
                    disabled={false}
                    size="md"
                    onClick={goToSettings}
                    >
                        Settings
                    </Button>
                </div>

            </div>
            <div className='w-10/12 rounded-lg spy-3 flex-grow shrink flex-row h-full max-h-[calc(100vh-225px)] overflow-auto bg-grass-gradient'> 
                { activeComponent === "Standings" && 
                    <NewStandings 
                    changeUserSelectedTeam={(team: Team) => {
                        setUserSelectedTeam(team);
                        setActiveComponent("Team");
                    }}
                    />
                }
                { activeComponent === "Team" && 
                    <Roster 
                    team={userSelectedTeam || userTeam} 
                    resetUserSelectedTeam={() => setUserSelectedTeam(null)} 
                    userSelectedTeam={!!userSelectedTeam}
                    />
                } 
                { activeComponent === "Tournaments" && 
                    <Leaderboard />
                }
                { activeComponent === "Golfers" && 
                    <Golfers />
                }
                { activeComponent === "Schedule" && 
                    <Schedule
                    data={data}
                    fetchNextPage={fetchNextPage}
                    hasNextPage={hasNextPage}
                    isFetchingNextPage={isFetchingNextPage}
                    isError={isError}
                    error={error}
                    />
                }
            </div>
            { selectedGolfer ?
                <Modal 
                open={open} 
                onClose={onClose} 
                bgColor="dark-green"
                closeButtonColor={'light'}
                >
                <div className="w-full h-auto flex items-center justify-center min-w-[900px]">
                    <div className="w-[90%] p-4 bg-middle rounded-xl transition-all duration-300 ease-in-out">
                        <PlayerPage />
                    </div>
                </div>
                </Modal>
                :
                ""
            }

        </div>
    );
  }