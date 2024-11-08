import PlayerData from "../../../Golfers/components/PlayerData";
import Tourney from "./Tourney";
import TableHeaders from "./TableHeaders";
import React from "react";
import { useParams } from "react-router-dom";

export default function Leaderboard() {
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
        },
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
        },
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

    const { leagueId } = useParams();

    // const tournaments = useFetchTournaments()

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

    const headers = ["Place", "Golfer", "R1", "Thru", "Total", "Projected Place"];

    return (
        <div className="w-full h-full overflow-auto text-light font-PTSans p-3 bg-dark shadow-xl">
            <Tourney />
            <TableHeaders headers={headers} />
            {displayRoster}
        </div>
    )
}