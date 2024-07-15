import TableHeaders from "../home/TableHeaders";
import TournamentTd from "./TournamentTd";
import { useSelector } from 'react-redux';
import PlayerPageHeader from "./PlayerPageHeader";

export default function PlayerPage() {

    console.log(useSelector((state) => state.users.holeByHoleComparisonChart))

    // data will be filed in, this is just an example

    const tournamentHeaders = ["date", "tournament name", "r1", "r2", "r3", "r4", "total", "score", "place", "leader"]

    const tournament = {
        date: "12/01/2024",
        name: "Arnold Palmer Invitational",
        player: {
            madeCut: true,
            r1: 65,
            r2: 70,
            r3: 67,
            r4: 71,
            total: 273,
            score: -15,
            place: "4th",
            leader: -18
        }
    }

    return (
        <div className="w-full h-[600px] p-2 overflow-auto">
            <PlayerPageHeader />
            <div className="bg-middle h-2/3 rounded-b-xl text-light overflow-auto">
                <TableHeaders 
                headers={tournamentHeaders}
                />
                <TournamentTd 
                tournament={tournament} 
                player={tournament.player}
                even={true}
                />
            </div>
        </div>
    )
}