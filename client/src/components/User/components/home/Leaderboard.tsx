import Tourney from "./Tourney";
import React, { useEffect, useState } from "react";
import GolferTournamentDetailsTable from "./GolferTournamentDetailsTable";
import TournamentScheduleTable from "./TournamentScheduleTable";
import { Tournament } from "../../../../types/tournaments";

export default function Leaderboard() {

    const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);

    return (
        <div className="w-full h-full overflow-hidden text-light font-PTSans p-4 bg-middle shadow-xl">
            <div className="p-4 overflow-auto rounded-xl w-full h-auto min-h-[300px] max-h-[600px]">
                { selectedTournament ?
                    <>
                        <Tourney 
                        tournament={selectedTournament}
                        />
                        <GolferTournamentDetailsTable 
                        tournamentId={selectedTournament.id}
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
        </div>
    )
}