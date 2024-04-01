export default function THead({ datapoint, children }) {
    return (
        <div className="flex flex-col items-center justify-center p-0.5 flex-grow h-12 font-PTSans">
            <div className="font-bold text-md lg:text-lg md:text-lg sm:text-md">
                {datapoint}
            </div>
            <div className="font-normal flex justify-center items-center truncate p-1 brightness-125">
                {children}
            </div>

        </div>
    )
}