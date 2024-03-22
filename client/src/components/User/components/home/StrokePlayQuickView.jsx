import TeamData from "./TeamData";
import { Link } from "react-router-dom";

export default function StrokePlayQuickView({ league }) {

    const myTeam = league.myTeam;

    // const teams = sortedArray.map((team, idx) => {
    //     if (idx % 2 === 0) {
    //         return <TeamData
    //         team={team}
    //         rank = {team.rank}
    //         even
    //         />
    //       } else {
    //         return <TeamData
    //         rank = {team.rank}
    //         team={team}
    //         />
    //       }
    // })

    return (
        <div className="w-full font-PTSans text-light flex-col flex justify-center items-center my-2">
            <div className="flex-row">
                <h1 className="text-2xl">{league.name}</h1>
                <h1 className="text-md">{league.type}</h1>
            </div>
            <div className="max-h-max w-3/4 bg-dark rounded-xl hover:shadow-xl shadow-dark p-4">
                <Link to="/leagues/4" className="w-full">
                    <div className="w-full">
                        <div className="w-full flex md:text-lg text-md py-3">
                            <div className="text-center flex w-3/6">
                                <div className="w-1/6">
                                    Place
                                </div>
                                <div className="w-5/6">
                                    Team
                                </div>
                            </div>
                            <div className="flex w-3/6 flex-row items-center">
                                <div className="flex flex-col w-1/3 items-center justify-center">
                                    Score
                                </div>
                                <div className="flex flex-col w-1/3 items-center justify-center">
                                    Top 10s
                                </div>
                                <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                                    Missed Cuts
                                </div>
                                <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                                    Wins
                                </div>
                            </div>
                        </div>
                        <TeamData
                            team={myTeam}
                            rank = {myTeam.rank}
                        />
                    </div>
                </Link>
            </div>
        </div>
    )
}