import React from 'react';
import Button from './Utils/components/Button';
import Standings from './Standings';
import Roster from './Roster';
import { useState } from 'react';
import Leaderboard from './Leaderboard';
import Players from './Players';
import SquigglyUnderline from "../components/Utils/components/SquigglyLine"
import Schedule from './Schedule';

export default function Dashboard() {

    const [activeComponent, setActiveComponent] = useState("Schedule");

    return (
      <div className="w-full h-full pt-20 pb-16">
        <div>
          <div className='w-full flex justify-center items-center flex-col'>
            <div className='flex-row h-16 w-11/12 mb-5 pl-14 flex items-center'>
                <h1 className='text-4xl'>
                    League Name
                </h1>
            </div>
                <div className='w-10/12 bg-middle rounded-lg overflow-auto min-h-[500px] h-[600px]'> 
                    <div className='p-5 flex items-center justify-center'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Standings"}, {name:"Team"}, {name:"Leaderboard"}, {name:"Players"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                    </div>
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
                </div>
            </div>
        </div>
    );
  }