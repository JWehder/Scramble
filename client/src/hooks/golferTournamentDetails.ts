import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { TournamentDetails } from "../types/golferTournamentDetails";

export interface TournamentDetailsResponse {
    details: TournamentDetails[];
}

const fetchGolferTournamentDetails = async (golferId: string) => {
    const response = await axios.get(`/api/golfers/${golferId}/tournament-details`);
    return response.data;
};

export const useFetchGolferTournamentDetails = (golferId?: string) => {
    return useQuery<TournamentDetailsResponse>({
        queryKey: ['golferTournamentDetails', golferId],
        queryFn: () => fetchGolferTournamentDetails(golferId!),
        enabled: !!golferId // Only enable query if golferId is valid
    });
};

