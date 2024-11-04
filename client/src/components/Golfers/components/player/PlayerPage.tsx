import TableHeaders from "../../../User/components/home/TableHeaders";
import TournamentTd from "./TournamentTd";
import PlayerPageHeader from "./PlayerPageHeader";
import React from "react";
import { useFetchGolferTournamentDetails } from "../../../../hooks/golferTournamentDetails";
import { useSelector } from "react-redux";
import { RootState } from "../../../../store";

export default function PlayerPage() {

    const selectedGolfer = useSelector((state: RootState) => state.golfers.selectedGolfer);

    const { data,
        isFetching,
        isSuccess,
        isError, 
        error } = useFetchGolferTournamentDetails(selectedGolfer?.id);
    
    // data will be filed in, this is just an example

    const tournamentHeaders = ["date", "tournament name", "position", "r1", "r2", "r3", "r4", "score", "strokes", "leader"]

    return (
        <div className="w-full h-[600px] p-2 overflow-auto">
            <PlayerPageHeader />
            <div className="bg-middle h-2/3 rounded-b-xl text-light overflow-auto">
                <TableHeaders 
                headers={tournamentHeaders}
                />
                { isSuccess && data?.details.map((detail, idx) => {
                    return (
                        <TournamentTd 
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