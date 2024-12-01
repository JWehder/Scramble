import React from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../../../store";
import { League } from "../../../types/leagues";
import { Team } from "../../../types/teams";
import { cn } from "../lib/utils";
import AnimatedTooltipStarters from "../../Utils/components/StartersNew";
 
export const BentoGrid = ({
  className,
  children,
}: {
  className?: string;
  children?: React.ReactNode;
}) => {
  return (
    <div
      className={cn(
        "grid md:auto-rows-[18rem] grid-cols-1 md:grid-cols-3 gap-4 max-w-7xl mx-auto ",
        className
      )}
    >
      {children}
    </div>
  );
};
 
export const BentoGridItem = ({
  className,
  title,
  description,
  header,
  icon,
}: {
  className?: string;
  title?: string | React.ReactNode;
  description?: string | React.ReactNode;
  header?: React.ReactNode;
  icon?: React.ReactNode;
}) => {
  return (
    <div
      className={cn(
        "row-span-1 rounded-xl group/bento hover:shadow-xl transition duration-200 shadow-input dark:shadow-none p-4 dark:bg-black dark:border-white/[0.2] bg-white border border-transparent justify-between flex flex-col space-y-4",
        className
      )}
    >
      {header}
      <div className="group-hover/bento:translate-x-2 transition duration-200">
        {icon}
        <div className="font-sans font-bold text-neutral-600 dark:text-neutral-200 mb-2 mt-2">
          {title}
        </div>
        <div className="font-sans font-normal text-neutral-600 text-xs dark:text-neutral-300">
          {description}
        </div>
      </div>
    </div>
  );
};

const Headers: React.FC<{ headers: string[] }> = ({ headers }) => (
  <div className="flex justify-between text-light bg-middle rounded-md font-semibold text-xs md:text-sm lg:text-sm overflow-x-auto">
    {headers.map((header, idx) => (
      <span key={idx} className="w-1/5 text-center">
        {header}
      </span>
    ))}
  </div>
);

const TeamData: React.FC<{ team: Team | undefined; rank: number | undefined }> = ({ team, rank }) => (
  <div className="flex justify-between items-center p-2 text-light bg-dark rounded-md mt-2 text-sm lg:text-md md:text-sm overflow-x-auto">
    <span className="w-1/5 text-center font-bold">{rank}</span>
    <span className="w-1/5 text-center">{team?.TeamStats.TotalUnderPar}</span>
    <span className="w-1/5 text-center">{team?.Points}</span>
    <span className="w-1/5 text-center">{team?.TeamStats.Top10s || 0}</span>
    <span className="w-1/5 text-center">{team?.TeamStats.MissedCuts}</span>
  </div>
);

const MatchPlayQuickView: React.FC<{ league: League }> = ({ league }) => (
  <div className="w-full max-w-screen-md font-PTSans text-light flex-col flex justify-center items-center p-4 bg-middle rounded-xl shadow-md m-0">
    <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">{league.Name}</h1>
    <h2 className="text-sm md:text-lg lg:text-xl text-light/80">{league.ScoreType}</h2>
    <div className="flex justify-center items-center mt-4 bg-dark shadow-inner p-4 rounded-xl">
      <Link to="/leagues/4" className="flex w-full items-center">
        <div className="flex-1 flex flex-col text-center items-center p-4 bg-middle rounded-xl">
          <h1 className="text-sm md:text-lg lg:text-xl font-bold">Team 1</h1>
          <p className="text-xs md:text-sm lg:text-base">Details</p>
        </div>
        <div className="flex justify-center items-center mx-4">
          <img alt="versus" className="w-8 h-8" />
        </div>
        <div className="flex-1 flex flex-col text-center items-center p-4 bg-middle rounded-xl">
          <h1 className="text-sm md:text-lg lg:text-xl font-bold">Team 2</h1>
          <p className="text-xs md:text-sm lg:text-base">Details</p>
        </div>
      </Link>
    </div>
  </div>
);

const StrokePlayQuickView: React.FC<{ league: League; myTeam: Team | undefined, className?: string }> = ({ league, myTeam, className }) => {
  const headers = ["place", "total", "points", "top 10s", "missed cuts"];

  return (
    <Link to={`/leagues/${league.id}`} className="cursor-pointer">
      <div       
      className={cn(
        "row-span-1 rounded-xl group/bento hover:shadow-xl transition duration-200 shadow-input dark:shadow-none p-4 bg-middle border border-transparent justify-between flex flex-col space-y-4",
        className
      )}>
        <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold group-hover/bento:translate-x-2 transition duration-200 font-PTSans text-light">{league.Name}</h1>
        <h2 className="text-sm md:text-lg lg:text-xl text-light/80 mb-1 group-hover/bento:translate-x-2 transition duration-200">{league.ScoreType}</h2>
        <AnimatedTooltipStarters players={myTeam?.Golfers} />
        <h2 className="text-sm md:text-lg lg:text-xl text-light">{myTeam?.TeamName}</h2>
        <div className="w-full bg-middle p-4 rounded-xl m-0">
            <Headers headers={headers} />
            <TeamData team={myTeam} rank={myTeam?.Placement} />
        </div>
      </div>
    </Link>
  );
};

const LeaguesList: React.FC = () => {
  const leagues = useSelector((state: RootState) => state.leagues.leagues);
  const teams = useSelector((state: RootState) => state.teams.userTeams);

  return (
    <div className="flex flex-col items-center gap-4 w-full p-2 bg-dark">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        {leagues.map((league, idx) => {
          const myTeam = teams.find((team) => team.LeagueId === league.id);

          return league.ScoreType === "Match Play" ? (
            <MatchPlayQuickView key={idx} league={league} />
          ) : (
            <StrokePlayQuickView key={idx} league={league} myTeam={myTeam} />
          );
        })}
      </div>
    </div>
  );
};

export default LeaguesList;
