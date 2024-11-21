import React from 'react';
import { useState } from 'react';
import SquigglyUnderline from "../../../Utils/components/SquigglyLine"
import Schedule from './Schedule';
import LeaguesList from "./LeaguesList"
import Button from '../../../Utils/components/Button';
import { useSelector } from 'react-redux';

export default function Dashboard() {

    const [activeComponent, setActiveComponent] = useState("Schedule");

    // code to be implemented when we have data

    const user = useSelector((state) => state.users.user);
    console.log(user);

    return (
        <div className='flex justify-center items-center w-full flex-col min-w-[700px]'>
            <div className='flex-row h-16 w-11/12 mb-5 flex items-center text-light font-PTSans'>
                <div className='w-1/3 flex items-center justify-center'>
                    <h1 className='text-xl lg:text-4xl md:text-2xl sm:text-xl'>
                        Dashboard
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
                <div className='w-10/12 rounded-lg overflow-auto spy-3 flex-grow shrink flex-row h-full max-h-[calc(100vh-225px)]'> 

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
        </div>
    );
  }