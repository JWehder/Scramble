import React from "react"

export default function THead({ datapoint }: { datapoint: number | string }) {
    return (
        <div className="flex flex-col items-center justify-center p-2 flex-grow h-14 font-PTSans w-auto">
            <div className="font-bold text-md lg:text-lg md:text-lg sm:text-md w-8 flex-grow flex justify-center items-center flex-row flex-shrink">
                {datapoint}
            </div>
        </div>
    );
}