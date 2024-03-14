export default function Tourney() {
    return (
        <div>
            <div className='flex-row h-16 w-11/12 mb-16 pl-14 flex'>
                <div className="flex-1 items-center pb-2">   
                    <h1 className='text-4xl'>Players Championship</h1>
                    <div className="mt-2">
                        <p>Date: March 14th - 17th</p>
                        <p>Course: Players Stadium Course</p>
                        <p>Purse: $25,000,000</p>
                    </div>
                </div>
                <div className="flex-1 text-right pb-2">
                    <h1>Location: Palm Valley, Florida</h1>
                    <p>Temperature: 75°F/ 24°C</p>
                    <p>Wind: 6MPH Wind/ 10MPH Gusts</p>
                    <p>Mostly Cloudy</p>
                    <p>Precipitation: 0%</p>
                </div>
            </div>
            <div class="p-4 text-center">
                <label for="inMyLeagueCheckbox">
                    <input 
                    type="checkbox" 
                    id="inMyLeagueCheckbox" 
                    value="In My League" 
                    class="text-middle"
                    />
                    In My League
                </label>
            </div>
        </div>

    )
}