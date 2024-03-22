import PlayerData from "./PlayerData";

export default function Players() {

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
        <div className="w-full h-full overflow-auto text-light font-PTSans">
            <h1 className="text-4xl">Available Players</h1>
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