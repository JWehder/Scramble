import React from "react";
import TableHeaders from "./TableHeaders";
import TournamentTd from "../../../Golfers/components/player/TournamentTd";
import { useFetchAllTournamentDetails } from "../../../../hooks/golferTournamentDetails";

export default function GolferTournamentDetailsTable(
    { tournamentId } : 
    { tournamentId: string }) {

    const { data,
    isFetching,
    isSuccess,
    isError } = useFetchAllTournamentDetails(tournamentId);

    const tournamentHeaders = ["date", "tournament name", "position", "r1", "r2", "r3", "r4", "score", "strokes", "leader"];

    // Set of keys to display with fallback support
    const desiredKeysSet = new Set(["Position", "R1", "R2", "R3", "R4", "TotalStrokes", "Score", "WinningScore"]);

    return (
        <div className="bg-middle rounded-xl text-light overflow-auto">
        <TableHeaders 
        headers={tournamentHeaders}
        />
        { isSuccess && data?.details.map((detail, idx) => {
            return (
                <TournamentTd 
                key={detail.id}
                golferDetails={detail} 
                desiredKeysSet={desiredKeysSet}
                even={idx % 2 == 0}
                />
            )
            })
        }
        { isError && <div>Error loading tournament details.</div> }
        { isFetching && <div>Loading...</div> }
    </div>
    )
}