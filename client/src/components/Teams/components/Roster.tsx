import PlayerData from "../../Golfers/components/PlayerData";
import Headers from "../../Utils/components/TableHeaders";
import DashboardTitle from "../../User/components/home/DashboardTitle";
import Button from "../../Utils/components/Button";
import React from "react";
import { Golfer } from "../../../types/golfers";
import { Team } from "../../../types/teams";

export default function Roster({ team } : { team: Team | null }) {
    console.log(team)

    const displayRoster = team?.Golfers.map((player: Golfer, idx) => {
        return <PlayerData
        player={player}
        even={idx % 2 === 0}
        />
    })

    const headers = ["Rank", "Golfer", "Avg Score", "Top 10s", "Avg Placing", "Fedex Odds"]

    return (
        <div className="w-full overflow-auto h-full md:h-[400px] text-light font-PTSans">
            <DashboardTitle title={`${team?.TeamName} - ${team?.Placement}`}>
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