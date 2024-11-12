import { Tournament } from '../../../../types/tournaments';
import Switch from '../../../Utils/components/Switch';
import React, { useState } from 'react';

export default function Tourney({ tournament } : { tournament: Tournament }) {

    const [checked, setChecked] = useState(false);

    // Call the useQuery hook, passing in tournament location and start date
    // const { data: weatherData, isLoading, error } = useFetchTournamentWeatherData(tournament)

    return (
        <div>
            <div className='flex-row h-16 w-11/12 mb-16 pl-14 flex text-light font-PTSans'>
                <div className="flex-1 items-center pb-2">   
                    <h1 className='text-3xl'>
                        {tournament.Name}
                    </h1>
                    <div className="mt-2">
                        <p>
                            {tournament.StartDate} - {tournament.EndDate}
                        </p>
                        <p>
                            {tournament.Venue ? 
                            <>
                                <div>
                                    {tournament.Venue[0]}
                                </div>
                            </>
                            :
                            null
                            }
                        </p>
                        <p>Purse: $25,000,000</p>
                    </div>
                </div>
                <div className="flex-1 text-right pb-2">
                {/* {isLoading ? (
                        <p>Loading weather...</p>
                    ) : error ? (
                        <p>Error loading weather</p>
                    ) : (
                        <>
                            <p>Temperature: {weatherData.temp}°F / {(weatherData.temp - 32) * 5/9}°C</p>
                            <p>Wind: {weatherData.windspeed} MPH / {weatherData.windgust} MPH Gusts</p>
                            <p>{weatherData.conditions}</p>
                            <p>Precipitation: {weatherData.precip}%</p>
                        </>
                )} */}
                </div>
            </div>
            <div className="p-4 text-center">
                <Switch checked={checked} setChecked={setChecked} />
            </div>
        </div>

    )
}