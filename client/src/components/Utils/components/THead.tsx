import React from "react"

export default function THead({ datapoint }: { datapoint: number | string }) {
    return (
        <div className="flex flex-col items-center justify-center p-2 flex-grow min-h-[3.5rem] font-PTSans w-full">
            <div className="font-bold text-xs sm:text-sm md:text-sm lg:text-sm w-8 flex-grow flex justify-center items-center flex-row flex-shrink">
                {datapoint}
            </div>
        </div>
    );
}