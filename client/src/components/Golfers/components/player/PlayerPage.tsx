import TableHeaders from "../../../User/components/home/TableHeaders";
import TournamentTd from "./TournamentTd";
import PlayerPageHeader from "./PlayerPageHeader";
import React from "react";
import { useFetchGolferTournamentDetails } from "../../../../hooks/golferTournamentDetails";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../../store";
import { unsetSelectedGolfer } from "../../state/golferSlice";
import { TournamentDetails } from "../../../../types/golferTournamentDetails";

// Mapping for human-readable headers to actual database keys
const tournamentDetailsHeaders: { [key: string]: keyof TournamentDetails } = {
    "Position": "Position",
    "R1": "R1",
    "R2": "R2",
    "R3": "R3",
    "R4": "R4",
    "Strokes": "TotalStrokes",
    "Score": "Score",
    "Winning Score": "WinningScore"
};

export default function PlayerPage() {
    const dispatch = useDispatch();

    const selectedGolfer = useSelector((state: RootState) => state.golfers.selectedGolfer);

    const { data,
    isFetching,
    isSuccess,
    isError, 
    error } = useFetchGolferTournamentDetails(selectedGolfer?.id);

    const desiredKeysSet = new Set(["Position", "R1", "R2", "R3", "R4", "TotalStrokes", "Score", "WinningScore"]);
    
    // data will be filed in, this is just an example

    if (!selectedGolfer) {
        dispatch(unsetSelectedGolfer());
    };

    const tournamentHeaders = ["date", "tournament name", "position", "r1", "r2", "r3", "r4", "score", "strokes", "leader"]

    return (
        <div className="p-2 overflow-auto rounded-xl h-auto min-h-[300px] max-h-[600px] ">
            <PlayerPageHeader />
            <div className="bg-middle rounded-xl text-light overflow-auto">
                <TableHeaders 
                headers={tournamentHeaders}
                />
                { isSuccess && data?.details.map((detail, idx) => {
                    return (
                        <TournamentTd 
                        desiredKeys={desiredKeysSet}
                        key={detail.id}
                        golferDetails={detail} 
                        even={idx % 2 == 0}
                        />
                    )
                    })
                }
                { isError && <div>Error loading tournament details.</div> }
                { isFetching && <div>Loading...</div> }
            </div>
        </div>
    )
}