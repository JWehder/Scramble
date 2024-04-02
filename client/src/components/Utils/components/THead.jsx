export default function THead({ datapoint, children }) {
    return (
        <div className="flex flex-col items-center justify-center p-1 flex-grow h-12 font-PTSans">
            <div className="font-bold text-md lg:text-lg md:text-lg sm:text-md">
                {datapoint}
            </div>
            <div className="font-normal flex justify-center items-center p-1 brightness-125 w-full flex-grow">
                {children}
            </div>
        </div>
    )
}