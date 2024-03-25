export default function Event({ event, even }) {
    const brightness = even ? 'brightness-125' : '';

    return (
        <div className={`bg-middle w-full ${brightness} p-4 text-light flex h-16 text-xs lg:text-sm md:text-xs sm:text-xs`}>
            <div className="flex items-center">
                {event.date} - 
                <img 
                className="w-6 h-6 mx-2"
                src="https://flagsapi.com/US/flat/64.png" />
            </div>
            <div className="flex items-center">
                {event.tournamentName}
            </div>
            <div className="text-right flex items-center justify-end flex-grow">
                {event.leagueName}
            </div>
        </div>
    )
}