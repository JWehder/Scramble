export default function LeagueInfo() {
    return (
        <div>
            <div className='flex-row h-16 w-11/12 mb-5 pl-14 flex text-light font-PTSans'>
                <div className="flex-1 flex items-center">   
                    <h1 className='text-4xl'>Overall Standings</h1>
                </div>
                <div className="flex-1 text-right">
                    <p>Next Tournament: Masters, April 20th-24th</p>
                    <p>Next Draft: April 20th-24th</p>
                </div>
            </div>
        </div>
    )
}