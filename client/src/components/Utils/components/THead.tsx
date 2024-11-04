import React from "react"

export default function THead({ datapoint }: { datapoint: number | string }) {
    return (
        <div className="flex flex-col items-center justify-center p-2 flex-grow h-14 font-PTSans w-auto">
            <div className="font-bold text-sm lg:text-md md:text-md sm:text-sm w-8 flex-grow flex justify-center items-center flex-row flex-shrink">
                {datapoint}
            </div>
        </div>
    );
}