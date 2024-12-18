import axios from 'axios';
import { Tournament } from '../types/tournaments';
import { useQuery } from '@tanstack/react-query';

interface ImportMetaEnv {
    readonly VITE_API_KEY: string;
    readonly VITE_API_URL: string;
    // Add more env variables here as needed
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }

const formatDate = (dateStr) => {
    const [month, day, year] = dateStr.split('/');
    return `${year}-${month}-${day}`;
};

// const fetchWeatherData = async (location, startDate, endDate) => {
//     // Format the start and end dates
//     const formattedStartDate = formatDate(startDate);
//     const formattedEndDate = formatDate(endDate);   
    
//     console.log(location, formattedStartDate, formattedEndDate)

//     // const apiKey = import.meta.env.VITE_VISUAL_CROSSING_API_KEY;
//     const baseURL = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${location}/${formattedStartDate}/${formattedEndDate}`;

//     const response = await axios.get(baseURL, {
//         params: {
//             unitGroup: 'us',
//             include: 'days',
//             key: apiKey,
//             contentType: 'json',
//         },
//     });
//     return response.data.days[0];  // Return weather for the specific day
// };

// // Call the useQuery hook, passing in tournament location and start date
// export const useFetchTournamentWeatherData = (tournament: Tournament) => {
//     return useQuery({
//         queryKey: ['weatherData', tournament.City, tournament.StartDate],
//         queryFn: () => fetchWeatherData(`${tournament.City}, ${tournament.State}`, tournament.StartDate, tournament.EndDate),
//         enabled: !!tournament.City && !!tournament.StartDate, // Run only if data is available
//     });
// } 
