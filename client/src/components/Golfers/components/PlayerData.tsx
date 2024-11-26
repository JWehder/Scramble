import Avatar  from "../../Utils/components/Avatar";
import React from "react";
import { Golfer } from "../../../types/golfers";

interface PlayerDataProps {
    player: Golfer;
    even: Boolean;
    onClick?: () => void; // Add onClick as an optional prop
}

export default function PlayerData({ 
    player,
    even,
    onClick
}: PlayerDataProps) {

    const brightness = even ? 'brightness-125' : '';

    return (
        <div 
        className={`w-full flex bg-middle h-14 justify-center items-center hover:z-30 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} break-all hover:b-1 my-1 lg:text-md md:text-sm sm:text-xs text-xs truncate p-2`}
        onClick={onClick}
        >
            <div className="text-center flex w-1/2 items-center">
                <div className="w-1/6">
                    {player.Rank}
                </div>
                <div className="w-5/6 text-left flex items-center pl-6">
                    <div className="flex-1 flex">
                        <div className="flex-col">
                            <Avatar 
                            imgUrl={""}
                            name={`${player.FirstName } ${player.LastName}`}
                            size={"10"}
                            />
                        </div>

                        <div className="pl-3 flex-col flex justify-center">
                            <div>
                                {`${player.FirstName } ${player.LastName}`} {player.Flag ? player.Flag : null}
                            </div>
                            <span>
                                {player.Country ? player.Country : null} Age: {player.Age}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div className="w-1/2 flex flex-row items-center space-x-5">
                {
                    exampleData.map((data, idx) => {
                        return (
                            <div 
                            key={`${data}-${idx}`}
                            className="flex flex-col w-6 flex-grow items-center justify-center">
                                {data}
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}