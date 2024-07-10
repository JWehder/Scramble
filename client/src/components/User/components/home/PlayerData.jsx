import Avatar  from "../../../Utils/components/Avatar";

export default function PlayerData({ rank, name, age, even }) {

    const brightness = even ? 'brightness-125' : '';

    return (
        <div className={`w-full flex bg-middle h-20 justify-center items-center hover:z-30 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} break-all hover:b-1 my-1 lg:text-md md:text-sm sm:text-xs text-xs truncate`}>
            <div className="text-center flex w-3/6 items-center">
                <div className="w-1/6">
                    {rank}
                </div>
                <div className="w-5/6 text-left flex items-center pl-6">
                    <div className="flex-1 flex">
                        <div className="flex-col">
                            <Avatar 
                            imgUrl={""}
                            name={name}
                            size={"12"}
                            />
                        </div>

                        <div className="pl-3 flex-col flex justify-center">
                            <div>
                                {name}
                            </div>
                            <span>
                                Dallas, TX, {age}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div className="w-3/6 flex flex-row items-center">
                <div className="flex flex-col w-1/3 items-center justify-center">
                    -3.2
                </div>
                <div className="flex flex-col w-1/3 items-center justify-center">
                    Top 10s
                </div>
                <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                    Avg Placing
                </div>
                <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                    Fedex Odds
                </div>
            </div>
        </div>
    )
}