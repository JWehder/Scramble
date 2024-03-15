import Avatar  from "./Utils/components/Avatar";

export default function PlayerData({ rank, name, age, even }) {

    const brightness = even ? 'brightness-125' : '';

    return (
        <div className={`w-full flex bg-middle h-20 justify-center items-center opacity-90 hover:z-30 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} md:text-md text-sm hover:b-1 my-1`}>
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
                            size={"14"}
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
            <div className="flex w-3/6 flex-row items-center">
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