import Starters from "../../../Utils/components/Starters";
import Avatar from "../../../Utils/components/Avatar";

export default function TeamData({ team, even, rank }) {

    const brightness = even ? 'brightness-125' : '';

    return (
        <div className={`w-full flex bg-middle h-20 justify-center items-center hover:z-20 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} text-sm md:text-sm lg:text-md sm:text-sm truncate hover:b-1 my-1 overflow-visible `}>
        <div className="text-center flex w-3/6 items-center">
            <div className="w-1/6">
                {rank}
            </div>
            <div className="w-5/6 text-left flex items-center pl-6">
                <div className="flex-1 flex">
                    <div className="pl-3 flex-col flex items-center justify-center flex-1">
                        <div className="flex items-center">
                            <Avatar 
                                imgUrl=""
                                team="team"
                                size={'10'}
                            /> 
                            {team.teamName}
                        </div>
                    </div>

                    <div className="flex-1 flex justify-center items-center">
                        <Starters />
                    </div>
                </div>
            </div>
        </div>
        <div className="flex w-3/6 flex-row items-center">
            <div className="flex flex-col w-1/3 items-center justify-center">
                {team.score}
            </div>
            <div className="flex flex-col w-1/3 items-center justify-center">
                {team.top10}
            </div>
            <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                {team.missedCuts}
            </div>
            <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                {team.wins}
            </div>
        </div>
    </div>
    )
}