import { Event } from "../types/events";
import axios from "axios";
import { useInfiniteQuery } from "@tanstack/react-query";

export interface EventsResponse {
    events: Event[];
    nextPage?: number | null; // Handle the optional nextPage
}

// Fetch golfers with pagination
const fetchUpcomingPeriods = async ({ pageParam = 0, leagueId }: { pageParam?: number; leagueId: string }): Promise<EventsResponse> => {
    const response = await axios.post<EventsResponse>(`/api/periods/leagues/${leagueId}?page=${pageParam}`);
    return response.data;
};

// Custom hook for fetching golfers with infinite pagination
export const useFetchUpcomingPeriods = (leagueId: string ) => {
    return useInfiniteQuery<EventsResponse>({
        queryKey: ['periods', leagueId],
        queryFn: ({ pageParam }) => fetchUpcomingPeriods({ pageParam: pageParam as number, leagueId }),
        initialPageParam: 0,
        getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    });
};

// Fetch golfers with pagination
const fetchUpcomingUserPeriods = async ({ pageParam = 0 }: { pageParam?: number; }): Promise<EventsResponse> => {
    const response = await axios.post<EventsResponse>(`/api/periods/user_events?page=${pageParam}`);
    return response.data;
};

// Custom hook for fetching golfers with infinite pagination
export const useFetchUpcomingUserPeriods = () => {
    return useInfiniteQuery<EventsResponse>({
        queryKey: ['periods'],
        queryFn: ({ pageParam }) => fetchUpcomingUserPeriods({ pageParam: pageParam as number }),
        initialPageParam: 0,
        getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    });
};