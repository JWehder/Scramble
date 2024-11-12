import HolesComparisonChart from "./HolesComparisonChart";
import React, { useState } from "react";
import { TournamentDetails } from "../../../../types/golferTournamentDetails";
import TableRow from "../../../Utils/components/TableRow";

export default function TournamentTd({ 
    golferDetails, 
    even,
    desiredKeysSet
}: {
    golferDetails: TournamentDetails,
    even: boolean,
    desiredKeysSet: Set<string>
}) {
    const [showHolesComparisonChart, setShowHolesComparisonChart] = useState(false);

    return (
        <>
            <TableRow 
            firstTwoDatapoints={[golferDetails.StartDate, golferDetails.TournamentName]}
            data={golferDetails}
            columns={desiredKeysSet}
            brightness={even ? 'brightness-125' : ''}
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