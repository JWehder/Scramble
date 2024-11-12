import React from "react"

export default function TableHeaders({ headers }) {

    return (
        <div className="w-full flex lg:text-md md:text-md sm:text-sm text-sm truncate font-bold p-1 items-center text-clip">
            <div className="text-center flex w-1/2">
                <div className="w-1/6">
                    {headers[0]}
                </div>
                <div className="w-5/6">
                    {headers[1]}
                </div>
            </div>
            <div className="flex w-1/2 flex-row">
                {headers?.slice(2).map((header: string, idx: number) => {
                    return <div 
                    key={`${header}-${idx}`}
                    className="flex flex-col w-6 flex-grow px-1 items-center justify-center p-1">
                        {header}
                    </div>
                })}
            </div>
        </div>
    )
}