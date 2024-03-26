export default function TableHeaders({ headers }) {

    return (
        <div className="w-full flex lg:text-md md:text-md sm:text-md text-md truncate">
            <div className="text-center flex w-3/6">
                <div className="w-1/6">
                    {headers[0]}
                </div>
                <div className="w-5/6">
                    {headers[1]}
                </div>
            </div>
            <div className="flex w-3/6 flex-row items-center">
                {headers.slice(2).map((header) => {
                    return <div className="flex flex-col w-1/3 items-center justify-center">
                        {header}
                    </div>
                })}
            </div>
        </div>
    )
}