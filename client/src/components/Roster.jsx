import RosterSpot from "./RosterSpot"
import Avatar from "./Utils/components/Avatar"

export default function Roster({ golferName, AvgScore, }) {

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

    const displayRoster = players.map((player) => {
        return <RosterSpot
                name={player.name}
                rank={player.rank}
                age={player.age}
                />
    })

    return (
        <div className="p-4 w-full overflow-auto h-[250px] md:h-[400px]">
            <div className="w-full flex md:text-lg text-md">
                <div className="text-center flex w-3/6">
                    <div className="w-1/6">
                        Rank
                    </div>
                    <div className="w-5/6">
                        Golfer
                    </div>
                </div>
                <div className="flex w-3/6 flex-row items-center">
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        Avg Score
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        Top 10s
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Avg Placing
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Fedex Odds
                    </div>
                </div>
            </div>

        </div>
    )
}