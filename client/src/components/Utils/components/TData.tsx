import React from "react";

export default function TData({ children }) {
    return (
        <div className="flex flex-col items-center justify-center w-8 flex-grow text-sm lg:text-md md:text-md sm:text-sm overflow-hidden text-ellipsis whitespace-nowrap">
            {children}
        </div>
    )
}