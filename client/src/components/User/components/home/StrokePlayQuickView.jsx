import TeamData from "./TeamData";
import { Link } from "react-router-dom";
import Headers from "../../../Utils/components/TableHeaders";

export default function StrokePlayQuickView({ league }) {

    const myTeam = league.myTeam;

    const headers = ["Place", "Team", "Score", "Top 10s", "Missed Cuts", "Wins"];

    return (
        <div className="w-full font-PTSans text-light flex-col flex justify-center items-center my-2">
            <div className="flex-row">
                <h1 className="text-2xl">{league.name}</h1>
                <h1 className="text-md">{league.type}</h1>
            </div>
            <div className="max-h-max w-3/4 bg-dark rounded-xl hover:shadow-xl shadow-dark p-4">
                <Link to="/leagues/4" className="w-full">
                        <Headers headers={headers} />
                        <TeamData
                            team={myTeam}
                            rank = {myTeam.rank}
                        />
                </Link>
            </div>
        </div>
    )
}