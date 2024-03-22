import Starters from "./Utils/components/Starters";
import versus from "../assets/versus.png";
import { Link } from 'react-router-dom';

export default function MatchPlayQuickView({ league }) {
    return (
        <div className="w-full font-PTSans text-light flex-col flex justify-center items-center">
            <div className="flex-row ">
                <h1 className="text-2xl">{league.name}</h1>
                <h1 className="text-md">{league.type}</h1>
            </div>
            <div className="h-1/8 w-1/2 bg-dark rounded-xl hover:shadow-xl shadow-dark p-4 flex justify-center items-center">
                <Link to="/leagues/4" className="w-full">
                    <div className="flex w-full">
                        <div className="flex-1 flex flex-col text-center items-center justify-center">
                            <div className="flex-row">
                                <h1 className="text-xl">{league.team1Name} - {league.team1Rank}</h1>
                                <h1>{league.team2Score}</h1>
                                <Starters />
                            </div>
                        </div>
                        <img className="w-8 h-8" src={versus} alt="versus" />
                        <div className="flex-1 flex flex-col text-center items-center justify-center">
                            <div className="flex-row"> 
                                <h1 className="text-xl">{league.team2Name} - {league.team2Rank}</h1>
                                <h1>{league.team1Score}</h1>
                                <Starters />
                            </div>
                        </div>
                    </div>
                </Link>
            </div>
        </div>
    )
}