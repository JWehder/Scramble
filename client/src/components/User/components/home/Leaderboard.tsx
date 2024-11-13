import Tourney from "./Tourney";
import React, { useState } from "react";
import GolferTournamentDetailsTable from "./GolferTournamentDetailsTable";
import TournamentScheduleTable from "./TournamentScheduleTable";
import { Tournament } from "../../../../types/tournaments";
import BackButton from "../../../Utils/components/BackButton";

export default function Leaderboard() {

    const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);

    return (
        <div className="w-full h-full text-light font-PTSans p-4 bg-middle shadow-xl">
                { selectedTournament ?
                    <>
                        <span className='inline-flex items-center'>
                            <BackButton 
                                size="8" 
                                color={"stroke-light"} 
                                handleBackClick={() => setSelectedTournament(null)}
                            />
                        </span>
                        <Tourney 
                        tournament={selectedTournament}
                        />
                        <GolferTournamentDetailsTable 
                        tournamentId={selectedTournament.id}
                        holeData={selectedTournament.Holes}
                        />
                    </>
                :
                    <>
                        <TournamentScheduleTable 
                        setSelectedTournament={setSelectedTournament}
                        />
                    </>

                }
        </div>
    )
}