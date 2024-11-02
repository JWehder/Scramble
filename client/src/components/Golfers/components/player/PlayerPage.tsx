import TableHeaders from "../../../User/components/home/TableHeaders";
import TournamentTd from "./TournamentTd";
import PlayerPageHeader from "./PlayerPageHeader";
import React from "react";
import { useFetchGolferTournamentDetails } from "../../../../hooks/golferTournamentDetails";

export default function PlayerPage({
    selectedGolferId,
}: {
    selectedGolferId: string | null;
}) {

    const {
        data,
        isFetching,
        isSuccess,
        isError,
        error
    } = useFetchGolferTournamentDetails(selectedGolferId!);

    // data will be filed in, this is just an example

    const tournamentHeaders = ["date", "tournament name", "r1", "r2", "r3", "r4", "total", "score", "place", "leader"]

    return (
        <div className="w-full h-[600px] p-2 overflow-auto">
            <PlayerPageHeader />
            <div className="bg-middle h-2/3 rounded-b-xl text-light overflow-auto">
                <TableHeaders 
                headers={tournamentHeaders}
                />
                { isSuccess && data?.details.map((detail) => {
                    return (
                        <TournamentTd 
                        golferDetails={detail} 
                        even={true}
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