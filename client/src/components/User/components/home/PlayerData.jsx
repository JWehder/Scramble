import Avatar  from "../../../Utils/components/Avatar";

export default function PlayerData({ rank, name, age, even }) {

    const brightness = even ? 'brightness-125' : '';

    const exampleData = ["-3.2", "Top 10s", "Avg Placing", "Fedex Odds"];

    return (
        <div className={`w-full flex bg-middle h-20 justify-center items-center hover:z-30 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} break-all hover:b-1 my-1 lg:text-md md:text-sm sm:text-xs text-xs truncate p-2`}>
            <div className="text-center flex w-1/2 items-center">
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
            <div className="w-1/2 flex flex-row items-center space-x-5">
                {
                    exampleData.map((data) => {
                        return (
                            <div className="flex flex-col w-6 flex-grow items-center justify-center">
                                {data}
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}