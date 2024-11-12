import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { Tournament } from "../types/tournaments";

export interface TournamentDetailsResponse {
    tournaments: Tournament[];
}

const fetchTournamentScheudule = async (fantasy_league_season_id: string) => {
    const response = await axios.get(`/api/fantasy_league_seasons/${fantasy_league_season_id}/tournaments/tournament_schedule`);
    return response.data;
};

export const useFetchTournamentDetails = (fantasy_league_season_id?: string) => {
    return useQuery<TournamentDetailsResponse>({
        queryKey: ['golferTournamentDetails', fantasy_league_season_id],
        queryFn: () => fetchTournamentScheudule(fantasy_league_season_id!),
        enabled: !!fantasy_league_season_id // Only enable query if golferId is valid
    });
};