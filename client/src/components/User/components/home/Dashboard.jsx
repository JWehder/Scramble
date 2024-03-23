import React from 'react';
import { useState } from 'react';
import SquigglyUnderline from "../../../Utils/components/SquigglyLine"
import Schedule from './Schedule';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import LeaguesList from './LeaguesList';
import Button from '../../../Utils/components/Button';

export default function Dashboard() {
    const { leagueId } = useParams();

    const [activeComponent, setActiveComponent] = useState("Schedule");

    const signedIn = useSelector((state) => state.users.user);

    // code to be implemented when we have data

    return (
        <>
            <div className='flex-row h-16 w-11/12 mb-5 flex items-center text-light font-PTSans'>
                <div className='w-1/3 flex items-center justify-center'>
                    <h1 className='text-4xl'>
                        Your Leagues
                    </h1>
                </div>

                <div className='p-5 flex items-center justify-center w-1/3'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Leagues"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                </div>
                <div className='w-1/3 flex items-center justify-center'>
                    <Button
                    size="md"
                    variant="secondary"
                    >
                        Settings
                    </Button>
                </div>

            </div>
                <div className='w-10/12 bg-middle rounded-lg overflow-auto min-h-[500px] h-[600px] py-3'> 


                    { activeComponent === "Schedule" && 
                        <div className='flex items-center justify-center'>
                            <Schedule />
                        </div>
                    }
                    { activeComponent === "Leagues" && 
                        <div className='flex items-center justify-center'>
                            <LeaguesList />
                        </div>
                    }
                </div>
        </>
    );
  }