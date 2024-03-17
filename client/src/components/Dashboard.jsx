import React from 'react';
import Button from './Utils/components/Button';
import Standings from './Standings';
import Roster from './Roster';
import { useState } from 'react';
import Leaderboard from './Leaderboard';
import Players from './Players';
import SquigglyUnderline from "../components/Utils/components/SquigglyLine"

export default function Dashboard() {

    const [activeComponent, setActiveComponent] = useState("Standings");

    const [active, setActive] = useState(false);

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
                        {/* { activeComponent === "Standings" ? 
                        <Button 
                        size="spmd"
                        >
                            League
                        </Button>
                        :
                        <Button
                        onClick={() => setActiveComponent("Standings")}
                        variant="special" 
                        >
                            League
                        </Button>
                        }
                        { activeComponent === "Team" ? 
                        <Button 
                        size="spmd"
                        >
                            Team
                        </Button>
                        :
                        <Button
                        variant="special" 
                        onClick={() => setActiveComponent("Team")}
                        >
                            Team
                        </Button>
                        }
                        { activeComponent === "Leaderboard" ? 
                        <Button 
                        size="spmd"
                        >
                            Leaderboard
                        </Button>
                        :
                        <Button
                        onClick={() => setActiveComponent("Leaderboard")}
                        variant="special" 
                        >
                            Leaderboard
                        </Button>
                        }
                        { activeComponent === "Players" ? 
                        <Button 
                        size="spmd"
                        >
                            Players
                        </Button>
                        :
                        <Button
                        onClick={() => setActiveComponent("Players")}
                        variant="special" 
                        >
                            Players
                        </Button>
                        } */}
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
                    </div>
                </div>
            </div>
        </div>
    );
  }