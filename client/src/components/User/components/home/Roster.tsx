import PlayerData from "../../../Golfers/components/PlayerData";
import Headers from "./TableHeaders";
import DashboardTitle from "./DashboardTitle";
import Button from "../../../Utils/components/Button";
import { useSelector } from "react-redux";
import { RootState } from "../../../../store";
import React from "react";

export default function Roster() {

    const user = useSelector((state: RootState) => state.users.user);

    console.log(user);

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

    const displayRoster = players.map((player, idx) => {
        if (idx % 2 === 0) {
            return <PlayerData
            name={player.name}
            rank={player.rank}
            age={player.age}
            even
            />
        } else {
            return <PlayerData
            name={player.name}
            rank={player.rank}
            age={player.age}
            />
        }
    })

    const headers = ["Rank", "Golfer", "Avg Score", "Top 10s", "Avg Placing", "Fedex Odds"]

    return (
        <div className="w-full overflow-auto h-full md:h-[400px] text-light font-PTSans">
            <DashboardTitle title="Team Name">
                <div className="flex-1 flex items-center justify-center">
                    <div className="mr-2">
                        <Button 
                            variant="secondary" 
                            size="md"
                        >
                            Trade
                        </Button>
                    </div>


                    <Button 
                        variant="secondary" 
                        size="md"
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