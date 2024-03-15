import PlayerData from "./PlayerData";
import Team from "./Team";

export default function Roster() {

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

    return (
        <div className="w-full overflow-auto h-[250px] md:h-[400px] text-light font-PTSans">
            <Team />
            <div className="w-full flex md:text-lg text-md">
                <div className="text-center flex w-3/6 p-3">
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
            {displayRoster}
        </div>
    )
}