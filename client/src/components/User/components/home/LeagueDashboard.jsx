import React from 'react';
import Standings from './Standings';
import Roster from './Roster';
import { useState } from 'react';
import Leaderboard from './Leaderboard';
import Players from './Players';
import SquigglyUnderline from "../../../Utils/components/SquigglyLine"
import Schedule from './Schedule';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Button from '../../../Utils/components/Button';
import BackButton from '../../../Utils/components/BackButton';
import NextButton from '../../../Utils/components/NextButton';

export default function LeagueDashboard() {
    const { leagueId } = useParams();

    const [activeComponent, setActiveComponent] = useState("Schedule");

    const signedIn = useSelector((state) => state.users.user);

    // code to be implemented when we have data

    console.log(leagueId);

    return (
        <>
            <div className='flex-row h-16 w-11/12 mb-5 flex items-center text-light font-PTSans pt-3 min-h-min'>

                <div className='flex flex-col w-1/3'>
                    <div className='flex justify-center items-center flex-row'>
                        <h1 className='lg:text-4xl md:text-2xl sm:text-xl'>
                            League Name
                        </h1>
                    </div>

                    <div className='flex justify-center items-center flex-row'>
                        <BackButton size={"4"} color={"stroke-light"} />
                        <NextButton size={"4"} color={"stroke-light"} />
                    </div>

                    <div>
                        <p className='text-xs'></p>
                    </div>
                </div>

                <div className='p-5 flex items-center justify-center w-1/3'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Standings"}, {name:"Team"}, {name:"Leaderboard"}, {name:"Players"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                </div>

                <div className='w-1/3 flex justify-center items-center'>
                    <Button
                    variant="secondary"
                    size="md"
                    >
                        Settings
                    </Button>
                </div>

            </div>
            <div className='w-10/12 bg-middle rounded-lg overflow-auto min-h-[400px] h-[600px] py-3'> 

                { activeComponent === "Standings" && 
                    <div className='flex items-center justify-center'>
                        <Standings />
                    </div>
                }
                { activeComponent === "Team" && 
                    <div className='flex items-center justify-center'>
                        <Roster />
                    </div>
                } 
                { activeComponent === "Leaderboard" && 
                    <div className='flex items-center justify-center'>
                        <Leaderboard />
                    </div>
                }
                { activeComponent === "Players" && 
                    <div className='flex items-center justify-center'>
                        <Players />
                    </div>
                }
                { activeComponent === "Schedule" && 
                    <div className='flex items-center justify-center'>
                        <Schedule />
                    </div>
                }
            </div>
        </>
    );
  }