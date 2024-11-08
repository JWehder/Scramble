import { setHolesComparisonChart } from "../../../User/state/userSlice";
import HolesComparisonChart from "./HolesComparisonChart";
import React, { useState } from "react";
import { TournamentDetails } from "../../../../types/golferTournamentDetails";
import TData from "../../../Utils/components/TData";

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
            <div 
                onClick={() => setShowHolesComparisonChart(!showHolesComparisonChart)}
                className={`w-full flex bg-middle h-10 justify-center items-center hover:z-20 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} text-sm md:text-sm lg:text-md sm:text-sm truncate hover:b-1 my-1 overflow-visible border-x-2 border-middle`}
            >
                <div className="text-center flex w-3/6 items-center">
                    <div className="w-1/6 text-left px-2 overflow-hidden text-ellipsis whitespace-nowrap">
                        {golferDetails.StartDate}
                    </div>
                    <div className="w-5/6 text-left flex items-center pl-6">
                        <div className="flex justify-center overflow-hidden text-ellipsis whitespace-nowrap">
                            {golferDetails.TournamentName || "--"}
                        </div>
                    </div>
                </div>
                <div className="flex w-3/6 flex-row items-center">
                    {
                        Array.from(desiredKeysSet).map((key) => (
                            <TData key={key}>
                                {(golferDetails[key as keyof TournamentDetails] ?? "--") as React.ReactNode}
                            </TData>
                        ))
                    }
                </div>
            </div>
            {showHolesComparisonChart && (
                <HolesComparisonChart
                    rounds={golferDetails.Rounds}
                    holes={golferDetails.HoleData}
                />
            )}
        </>
    );
}