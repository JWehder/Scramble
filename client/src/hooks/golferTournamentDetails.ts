import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { TournamentDetails } from "../types/golferTournamentDetails";

export interface GolferTournamentDetailsResponse {
    details: TournamentDetails[];
}

const fetchGolferTournamentDetails = async (golferId: string) => {
    const response = await axios.get(`/api/golfers/${golferId}/tournament-details`);
    return response.data;
};

export const useFetchGolferTournamentDetails = (golferId?: string) => {
    return useQuery<GolferTournamentDetailsResponse>({
        queryKey: ['golferTournamentDetails', golferId],
        queryFn: () => fetchGolferTournamentDetails(golferId!),
        enabled: !!golferId // Only enable query if golferId is valid
    });
};

const fetchAllGolfersTournamentDetails = async (tournamentId: string) => {
    const response = await axios.get(`/api/golfer_tournament_details/tournaments/${tournamentId}`);
    return response.data;
};

export const useFetchAllTournamentDetails = (tournamentId?: string) => {
    return useQuery<GolferTournamentDetailsResponse>({
        queryKey: ['golfersTournamentDetails', tournamentId],
        queryFn: () => fetchAllGolfersTournamentDetails(tournamentId!),
        enabled: !!tournamentId // Only enable query if tournamentId is valid
    });
};

