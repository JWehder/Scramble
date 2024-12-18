import PlayerInfoTd from "./PlayerInfoTd";
import PlayerInfoHead from "./PlayerInfoHead";
import { useSelector } from "react-redux";
import { RootState } from "../../../../store";
import React from "react";
import { Golfer } from "../../../../types/golfers";

export default function PlayerPageHeader() {
    // Mapping for human-readable headers to actual database keys
    const playerHeaders: { [key: string]: keyof Golfer } = {
        "Age": "Age",
        "Country": "Country",
        "FedEx Rank": "Rank",
        "Swing": "Swing",
        "Height & Weight": "HtWt",
        "College": "College",
        "Events": "Events",
        "Cuts": "Cuts",
        "Earnings": "Earnings",
        "OWGR": "OWGR",
        "FedEx Points": "FedexPts",
        "Turned Pro": "TurnedPro"
    };

    const playerInfo = useSelector((state: RootState) => state.golfers.selectedGolfer);

    return (
        <div className="bg-middle w-full h-1/3 rounded-t-xl flex">
            <div className="w-1/4">
                <div className="flex items-center justify-center flex-grow">
                    
                </div>
            </div>
            <div className="w-3/4">
                <div className="flex items-center justify-center font-PTSans p-2 text-light font-bold">
                    <h1 className="text-3xl">
                        {playerInfo?.FirstName} {playerInfo?.LastName}
                    </h1>
                </div>
                <div className="text-light font-PTSans flex-col p-2 space-y-4">
                    <div className="flex-row flex w-full space-x-2">
                        {playerInfo &&
                            Object.entries(playerHeaders)
                                .filter(([_, key]) => playerInfo[key] !== undefined && playerInfo[key] !== null && playerInfo[key] !== "")
                                .slice(0, 5)
                                .map(([displayName, key], idx) => (
                                    <PlayerInfoHead key={idx} datapoint={displayName}>
                                        <PlayerInfoTd 
                                            datapoint={key === "Earnings" ? `$${playerInfo[key]?.toLocaleString()}` : playerInfo[key]} 
                                        />
                                    </PlayerInfoHead>
                                ))
                        }
                    </div>
                    <div className="flex-row flex w-full space-x-2">
                        {playerInfo &&
                            Object.entries(playerHeaders)
                                .filter(([_, key]) => playerInfo[key] !== undefined && playerInfo[key] !== null && playerInfo[key] !== "")
                                .slice(5)
                                .map(([displayName, key], idx) => (
                                    <PlayerInfoHead key={idx} datapoint={displayName}>
                                        <PlayerInfoTd 
                                            datapoint={key === "Earnings" ? `$${playerInfo[key]?.toLocaleString()}` : playerInfo[key]} 
                                        />
                                    </PlayerInfoHead>
                                ))
                        }
                    </div>
                </div>
            </div>
        </div>
    );
}

