import DashboardTitle from "./DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "./TableHeaders"

export default function Golfers() {

    const golfers = [
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

    const displayRoster = golfers.map((player, idx) => {
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

    const headers = ["Place", "Golfer", "R1", "Thru", "Total", "Projected Place"]

    return (
        <div className="w-full h-full overflow-auto text-light font-PTSans break-all">
            <div>
                <DashboardTitle title="Golfers" />
                <TableHeaders headers={headers} />
            </div>
            {displayRoster}
        </div>
    )
}