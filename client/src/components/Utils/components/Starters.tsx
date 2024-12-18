import React from "react";
import Player from "./Player";
import { Golfer } from "../../../types/golfers";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../../store";
import { setSelectedGolfer } from "../../Golfers/state/golferSlice";

const Starters: React.FC<{ players: Golfer[] | undefined }> = ({ players }) =>  {

    const dispatch = useDispatch<AppDispatch>();

    const handleGolferClick = (golfer: object) => {
        console.log(golfer)
        dispatch(setSelectedGolfer(golfer));
    };

    return (
        <div className='flex my-1 align-center justify-center max-w-max'>
            {
                players?.map((player) => {
                    return <Player
                        imgUrl={""}         
                        name={`${player.FirstName} ${player.LastName}`}
                        size="sm"
                        score={-2}
                        active={false}
                        handleClick={() => handleGolferClick(player)}
                    />
                })
            }
        </div>
    )
}

export default Starters;