import TableHeaders from "../../../User/components/home/TableHeaders";
import TournamentTd from "./TournamentTd";
import PlayerPageHeader from "./PlayerPageHeader";
import React from "react";
import { useFetchGolferTournamentDetails } from "../../../../hooks/golferTournamentDetails";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../../store";
import { resetSelectedGolfer } from "../../state/golferSlice";

export default function PlayerPage() {
    const dispatch = useDispatch();

    const selectedGolfer = useSelector((state: RootState) => state.golfers.selectedGolfer);

    const { data,
    isFetching,
    isSuccess,
    isError, 
    error } = useFetchGolferTournamentDetails(selectedGolfer?.id);

    if (!selectedGolfer) {
        dispatch(resetSelectedGolfer());
    };

    const tournamentHeaders = ["date", "tournament name", "position", "r1", "r2", "r3", "r4", "score", "strokes", "leader"];

    // Set of keys to display with fallback support
    const desiredKeysSet = new Set(["Position", "R1", "R2", "R3", "R4", "TotalStrokes", "Score", "WinningScore"]);

    return (
        <div className="p-2 overflow-auto rounded-xl h-auto min-h-[300px] max-h-[600px]">
            <PlayerPageHeader />
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
        </div>
    )
}