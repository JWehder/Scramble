import React from "react";
import Starters from "../../Utils/components/Starters";
import AnimatedTooltipStarters from "../../Utils/components/StartersNew";
import Avatar from "../../Utils/components/Avatar";
import TData from "../../Utils/components/TData";
import { Team } from "../../../types/teams";

export default function TeamData(
    { team, even, onClick }:
    { 
        team: Team,
        even: boolean,
        onClick: () => void
    }
    ) {

    const brightness = even ? 'brightness-125' : '';
    const space = even ? 'my-2' : '';

    const desiredData = [team.Points, team.TeamStats.Top10s, team.TeamStats.MissedCuts, team.TeamStats.Wins]

    return (
        <div 
        className={`w-full flex bg-middle h-auto justify-center items-center 
        cursor-pointer hover:shadow-lg shadow-middle flex-row 
        border-box ${brightness} text-sm md:text-sm lg:text-md sm:text-sm 
        truncate hover:border-1 ${space} overflow-visible rounded-lg transition-all group/team p-2`}
        onClick={onClick}
        >
            {/* Left side: Start date and tournament name */}
            <div className="flex w-1/2 items-center">
                <div className="w-1/6 text-center px-2">
                    {team.Placement}
                </div>
                <div className="w-5/6 text-left flex items-center pl-6">
                    <div className="flex w-full">
                        <div className="flex items-center">
                            {/* Avatar and Team Name */}
                            <Avatar imgUrl="" size="12" />
                            <div className="flex flex-col group-hover/team:translate-x-2 transition duration-200">
                                <span className="font-semibold text-lg">
                                    {team.TeamName}
                                </span>
                                <span className="text-light text-xs">
                                    Avg Score: {team.TeamStats.AvgScore}
                                </span>
                            </div>
                                <div className="px-2 group-hover/team:translate-x-2 transition duration-20 mx-2">
                                    <AnimatedTooltipStarters players={team.Golfers}/>
                                </div>
                        </div>

                    </div>
                </div>
            </div>

            {/* Stats Section */}
            <div className="flex w-1/2 flex-row items-center">
                {desiredData.map((dp, index) => (
                <TData key={index}>
                    {dp}
                </TData>
                ))}
            </div>
        </div>
    )
}