import React from 'react';
import Button from './Utils/components/Button';
import Standings from './Standings';
import Roster from './Roster';
import { useState } from 'react';
import Leaderboard from './Leaderboard';

export default function Dashboard() {

    const [activeComponent, setActiveComponent] = useState("Standings");

    return (
      <div className="w-full h-screen pt-20 pb-16 px-4">
        <div>
          <div className='w-full flex justify-center items-center flex-col'>
            <div className='flex-row h-16 w-11/12 mb-5 pl-14 flex items-center'>
              <h1 className='text-4xl'>League Name</h1>
            </div>
            <div className='w-10/12 bg-light rounded-lg overflow-auto max-h-[500px]'> 
            <div className='border-b-black p-5 flex items-center justify-center'>
                { activeComponent === "Standings" ? 
                <Button 
                variant="primary" 
                size="md"
                >
                    League
                </Button>
                :
                <Button
                onClick={() => setActiveComponent("Standings")}
                >
                    League
                </Button>
                }
                { activeComponent === "Team" ? 
                <Button 
                variant="primary" 
                size="md"
                >
                    Team
                </Button>
                :
                <Button
                onClick={() => setActiveComponent("Team")}
                >
                    Team
                </Button>
                }
                { activeComponent === "Leaderboard" ? 
                <Button 
                variant="primary" 
                size="md"
                >
                    Leaderboard
                </Button>
                :
                <Button
                onClick={() => setActiveComponent("Leaderboard")}
                >
                    Leaderboard
                </Button>
                }
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
            </div>
          </div>
          <div>
            {/* ... */}
          </div>
        </div>
      </div>
    );
  }