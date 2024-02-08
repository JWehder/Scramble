import { useState } from 'react';
import Player from './Player';


export default function League({ league }) {
    const [showLeaguePreview, setShowLeaguePreview] = useState(false);


    return (
            <div 
            className='flex p-2 hover:bg-gray-700 rounded-xl'
            onMouseEnter={() => setShowLeaguePreview(true)}
            onMouseLeave={() => setShowLeaguePreview(false)}
            >
                <div>
                    <div>
                        Team 1
                    </div>
                    <div>
                        League 1
                    </div>
                </div>

                    {showLeaguePreview ?
                    <div className='flex my-1 align-center justify-center'>
                        <Player 
                            imgUrl={""}        
                            name="Justin Thomas" 
                            size="14"
                            score={-2}
                        />
                        <Player 
                            imgUrl={""} 
                            name="Scottie Scheffler" 
                            size="14"
                        />
                        <Player
                            imgUrl={""} 
                            name="Scottie Scheffler" 
                            size="14"
                            score={2}
                        />
                        <Player 
                            imgUrl={""} 
                            name="Scottie Scheffler" 
                            size="14"
                        />
                    </div>
                    :
                    ""}
                <span>108.08</span>
            </div>
    )
}