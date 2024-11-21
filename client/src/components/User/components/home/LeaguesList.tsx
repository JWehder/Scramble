import React from "react";
import { Link } from "react-router-dom";
import Starters from "../../../Utils/components/Starters";

interface Team {
  teamName: string;
  teamScore: number;
  top10?: number;
  rank: number;
}

interface League {
  name: string;
  type: string;
  myCurrentPlace?: string;
  teamAhead?: Team;
  teamBehind?: Team;
  myTeam?: Team;
  team1Name?: string;
  team2Name?: string;
  team1Rank?: string;
  team2Rank?: string;
  team1Players?: string[];
  team2Players?: string[];
  team1Score?: number;
  team2Score?: number;
}

const leagues: League[] = [
  {
    name: "Stroke Play League",
    type: "Stroke Play",
    myCurrentPlace: "6th",
    teamAhead: {
      teamName: "Team 4",
      teamScore: -11,
      top10: 2,
      rank: 4,
    },
    teamBehind: {
      teamName: "Team 6",
      teamScore: -8,
      top10: 1,
      rank: 2,
    },
    myTeam: {
      teamName: "Team 5",
      teamScore: -10,
      top10: 2,
      rank: 6,
    },
  },
  {
    name: "Match Play League",
    type: "Match Play",
    team1Name: "Team 1",
    team2Name: "Team 2",
    team1Rank: "6th",
    team2Rank: "4th",
    team1Players: ["Player 1", "Player 2", "Player 3"],
    team2Players: ["Player 4", "Player 5", "Player 6"],
    team1Score: -11,
    team2Score: -5,
  },
  {
    name: "Best Ball League",
    type: "Best Ball",
    myCurrentPlace: "6th",
    teamAhead: {
      teamName: "Team 4",
      teamScore: -11,
      top10: 2,
      rank: 4,
    },
    teamBehind: {
      teamName: "Team 6",
      teamScore: -8,
      top10: 1,
      rank: 2,
    },
    myTeam: {
      teamName: "Team 5",
      teamScore: -10,
      top10: 2,
      rank: 6,
    },
  },
];

const Headers: React.FC<{ headers: string[] }> = ({ headers }) => (
  <div className="flex justify-between text-light bg-middle p-2 rounded-md font-semibold text-xs md:text-sm lg:text-base">
    {headers.map((header, idx) => (
      <span key={idx} className="w-1/5 text-center">
        {header}
      </span>
    ))}
  </div>
);

const TeamData: React.FC<{ team: Team; rank: number }> = ({ team, rank }) => (
  <div className="flex justify-between items-center p-2 text-light bg-dark rounded-md mt-2">
    <span className="w-1/5 text-center font-bold">{rank}</span>
    <span className="w-1/5 text-center">{team.teamName}</span>
    <span className="w-1/5 text-center">{team.teamScore}</span>
    <span className="w-1/5 text-center">{team.top10 || 0}</span>
    <span className="w-1/5 text-center">-</span>
  </div>
);

const MatchPlayQuickView: React.FC<{ league: League }> = ({ league }) => (
  <div className="w-full font-PTSans text-light flex-col flex justify-center items-center p-4 bg-middle rounded-xl shadow-md m-0">
    <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">{league.name}</h1>
    <h2 className="text-sm md:text-lg lg:text-xl text-light/80">{league.type}</h2>
    <div className="flex justify-center items-center mt-4 bg-dark shadow-inner p-4 rounded-xl">
      <Link to="/leagues/4" className="flex w-full items-center">
        <div className="flex-1 flex flex-col text-center items-center p-4 bg-middle rounded-xl">
          <h1 className="text-sm md:text-lg lg:text-xl font-bold">
            {league.team1Name} - {league.team1Rank}
          </h1>
          <p className="text-xs md:text-sm lg:text-base">{league.team1Score}</p>
        </div>
        <div className="flex justify-center items-center mx-4">
          <img alt="versus" className="w-8 h-8" />
        </div>
        <div className="flex-1 flex flex-col text-center items-center p-4 bg-middle rounded-xl">
          <h1 className="text-sm md:text-lg lg:text-xl font-bold">
            {league.team2Name} - {league.team2Rank}
          </h1>
          <p className="text-xs md:text-sm lg:text-base">{league.team2Score}</p>
        </div>
      </Link>
    </div>
  </div>
);


const StrokePlayQuickView: React.FC<{ league: League }> = ({ league }) => {
  const myTeam = league.myTeam!;
  const headers = ["Place", "Team", "Score", "Top 10s", "Missed Cuts"];

  return (
    <div className="w-full font-PTSans text-light flex-col flex justify-center items-center p-4 bg-middle rounded-xl shadow-md">
      <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">{league.name}</h1>
      <h2 className="text-sm md:text-lg lg:text-xl text-light/80 mb-1">{league.type}</h2>
      <Starters />
      <div className="w-full bg-middle p-4 rounded-xl m-0">
        <Link to="/leagues/4">
          <Headers headers={headers} />
          <TeamData team={myTeam} rank={myTeam.rank} />
        </Link>
      </div>
    </div>
  );
};


const LeaguesList: React.FC = () => (
  <div className="flex flex-col items-center gap-4 w-full p-2 bg-dark">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
      {leagues.map((league, idx) =>
        league.type === "Match Play" ? (
          <MatchPlayQuickView key={idx} league={league} />
        ) : (
          <StrokePlayQuickView key={idx} league={league} />
        )
      )}
    </div>
  </div>
);

export default LeaguesList;
