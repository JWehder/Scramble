import React from 'react';
import { useState } from 'react';
import SquigglyUnderline from "./Utils/components/SquigglyLine"
import Schedule from './Schedule';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';

export default function Dashboard() {
    const { leagueId } = useParams();

    const [activeComponent, setActiveComponent] = useState("Schedule");

    const signedIn = useSelector((state) => state.users.user);

    // code to be implemented when we have data

    return (
        <>
            <div className='flex-row h-16 w-11/12 mb-5 pl-14 flex items-center text-light font-PTSans'>
                <h1 className='text-4xl'>
                    Your Leagues
                </h1>
            </div>
                <div className='w-10/12 bg-middle rounded-lg overflow-auto min-h-[500px] h-[600px]'> 
                    <div className='p-5 flex items-center justify-center'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Leagues"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                    </div>

                    { activeComponent === "Schedule" && 
                        <div className='flex items-center justify-center'>
                            <Schedule />
                        </div>
                    }
                    { activeComponent === "Leagues" && 
                        <div className='flex items-center justify-center'>
                            <Schedule />
                        </div>
                    }
                </div>
        </>
    );
  }