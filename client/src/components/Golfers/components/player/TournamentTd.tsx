import HolesComparisonChart from "./HolesComparisonChart";
import React, { useState } from "react";
import { TournamentDetails } from "../../../../types/golferTournamentDetails";
import TableRow from "../../../Utils/components/TableRow";

export default function TournamentTd({ 
    golferDetails, 
    even 
}: {
    golferDetails: TournamentDetails,
    even: boolean
}) {
    const [showHolesComparisonChart, setShowHolesComparisonChart] = useState(false);
   
    const brightness = even ? 'brightness-125' : '';

    // Set of keys to display with fallback support
    const desiredKeysSet = new Set(["Position", "R1", "R2", "R3", "R4", "TotalStrokes", "Score", "WinningScore"]);

    return (
        <>
            <TableRow 
            firstTwoDatapoints={[golferDetails.StartDate, golferDetails.TournamentName]}
            data={golferDetails}
            columns={desiredKeysSet}
            brightness={brightness}
            onClick={() => setShowHolesComparisonChart(!showHolesComparisonChart)}
            />
            {showHolesComparisonChart && (
                <HolesComparisonChart
                    rounds={golferDetails.Rounds}
                    holes={golferDetails.HoleData}
                />
            )}
        </>
    );
}