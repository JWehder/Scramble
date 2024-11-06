import React from "react"

export default function TableHeaders({ headers }) {
    return (
        <div className="w-full flex font-bold p-1 items-center text-sm">
            <div className="text-center flex w-1/2">
                <div className="w-1/6 sm:w-1/8 lg:w-1/6 overflow-hidden text-ellipsis whitespace-nowrap">
                    {headers[0]}
                </div>
                <div className="w-5/6 sm:w-3/4 lg:w-5/6 overflow-hidden text-ellipsis whitespace-nowrap">
                    {headers[1]}
                </div>
            </div>
            <div className="flex w-1/2 flex-row">
                {headers?.slice(2).map((header: string, idx: number) => (
                    <div 
                        key={`${header}-${idx}`}
                        className="flex flex-col w-6 sm:w-4 lg:w-6 flex-grow px-1 items-center justify-center overflow-hidden text-ellipsis whitespace-nowrap"
                    >
                        {header}
                    </div>
                ))}
            </div>
        </div>
    );
}
