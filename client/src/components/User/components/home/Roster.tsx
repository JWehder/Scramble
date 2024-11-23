import PlayerData from "../../../Golfers/components/PlayerData";
import Headers from "../../../Utils/components/TableHeaders";
import DashboardTitle from "./DashboardTitle";
import Button from "../../../Utils/components/Button";
import { useSelector } from "react-redux";
import React from "react";
import { RootState } from "../../../../store";
import { Golfer } from "../../../../types/golfers";

export default function Roster() {

    const usersTeam = useSelector((state: RootState) => state.teams.userSelectedTeam)

    console.log(usersTeam);

    const players = [
        {
            rank: "1st",
            name: "Scottie Scheffler",
            age: 26
        },
        {
            rank: "3rd",
            name: "Wyndham Clark",
            age: 29
        },
        {
            rank: "8th",
            name: "Patrick Cantlay",
            age: 30
        }
    ]

    const displayRoster = usersTeam?.Golfers.map((player: Golfer, idx) => {
        if (idx % 2 === 0) {
            return <PlayerData
            name={`${player.FirstName} ${player.LastName}`}
            rank={player.Rank}
            age={player.Age}
            even
            />
        } else {
            return <PlayerData
            name={`${player.FirstName} ${player.LastName}`}
            rank={player.Rank}
            age={player.Age}
            />
        }
    })

    const headers = ["Rank", "Golfer", "Avg Score", "Top 10s", "Avg Placing", "Fedex Odds"]

    return (
        <div className="w-full overflow-auto h-full md:h-[400px] text-light font-PTSans">
            <DashboardTitle title={usersTeam?.TeamName}>
                <div className="flex-1 flex items-center justify-center">
                    <div className="mr-2">
                        <Button 
                            variant="secondary" 
                            size="md"
                            disabled={false}
                            onClick={null}
                            type={null}
                        >
                            Trade
                        </Button>
                    </div>


                    <Button 
                        variant="secondary" 
                        size="md"
                        disabled={false}
                        onClick={null}
                        type={null}
                    >
                        Waivers
                    </Button>
                </div>
            </DashboardTitle>
            <Headers headers={headers} />
            {displayRoster}

        </div>
    )
}