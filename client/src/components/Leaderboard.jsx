import PlayerData from "./PlayerData";
import Team from "./Team";
import Tourney from "./Tourney";

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

    const displayRoster = players.map((player) => {
        return <PlayerData
                name={player.name}
                rank={player.rank}
                age={player.age}
                />
    })

    return (
        <div className="p-4 w-full h-[250px] md:h-[400px] overflow-auto">
            <Tourney />
            <div className="w-full flex md:text-lg text-md p-3">
                <div className="text-center flex w-3/6">
                    <div className="w-1/6">
                        Place
                    </div>
                    <div className="w-5/6">
                        Golfer
                    </div>
                </div>
                <div className="flex w-3/6 flex-row items-center">
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        R1
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        Thru
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Total
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Projected Place
                    </div>
                </div>
            </div>
            {displayRoster}
        </div>
    )
}