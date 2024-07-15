export default function PlayerInfoHead({ datapoint, children }) {
    return (
        <div className="flex flex-col items-center justify-center p-2 flex-grow h-14 font-PTSans w-auto">
            <div className="font-bold text-md lg:text-lg md:text-lg sm:text-md w-auto flex-grow flex justify-center items-center flex-row flex-shrink">
                {datapoint}
            </div>
            <div className="font-normal flex justify-center items-center p-1 brightness-125 w-auto flex-grow flex-row text-ellipsis">
                {children}
            </div>
        </div>
    )
}