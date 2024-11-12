import React, {useState} from "react";
import TableHeaders from "./TableHeaders";
import { useFetchAllTournamentDetails } from "../../../../hooks/golferTournamentDetails";
import TableRow from "../../../Utils/components/TableRow";
import HolesComparisonChart from "../../../Golfers/components/player/HolesComparisonChart";

export default function GolferTournamentDetailsTable(
    { tournamentId } : 
    { tournamentId: string }) {

    const { data,
    isFetching,
    isSuccess,
    isError } = useFetchAllTournamentDetails(tournamentId);

    const tournamentHeaders = ["place", "golfer name", "position", "r1", "r2", "r3", "r4", "strokes", "score", "fedex pts"];

    // Set of keys to display with fallback support
    const desiredKeysSet = new Set(["Position", "R1", "R2", "R3", "R4", "TotalStrokes", "Score", "FedexPts"]);

    return (
        <div className="bg-middle rounded-xl text-light overflow-auto">
        <TableHeaders 
        headers={tournamentHeaders}
        />
        { isSuccess && data?.details.map((detail, idx) => {
            const [showHolesComparisonChart, setShowHolesComparisonChart] = useState<Boolean>(false);

            return (

                <>
                    <TableRow 
                    firstTwoDatapoints={[detail.Position, detail.Name]}
                    data={detail}
                    columns={desiredKeysSet}
                    brightness={idx % 2 === 0 ? 'brightness-125' : ''}
                    onClick={() => setShowHolesComparisonChart(!showHolesComparisonChart)}
                    />
                    {showHolesComparisonChart && (
                        <HolesComparisonChart
                            rounds={detail.Rounds}
                            holes={detail.HoleData}
                        />
                    )}
                </>

            )
            })
        }
        { isError && <div>Error loading tournament details.</div> }
        { isFetching && <div>Loading...</div> }
    </div>
    )
}