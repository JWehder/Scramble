import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { TournamentDetailsResponse } from "./golferTournamentDetails";

const fetchTournamentDetails = async (leagueId) => {
    const response = await axios.get(`/api/tournaments/leagues/${leagueId}`);
    return response.data;
};

export const useFetchTournamentDetails = (leagueId?: string) => {
    return useQuery<TournamentDetailsResponse>({
        queryKey: ['golferTournamentDetails', leagueId],
        queryFn: () => fetchTournamentDetails(leagueId!),
        enabled: !!leagueId // Only enable query if golferId is valid
    });
};