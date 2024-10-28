import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../User/components/home/TableHeaders"
import { useParams } from "react-router-dom";
import React, { useEffect } from "react";
import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { ObjectId } from 'mongodb';

interface GolferTournamentDetails {
    id?: ObjectId;  // Optional, maps to '_id'
    GolferId: ObjectId;
    Position: string;
    Name: string;
    Score: string;
    R1?: string;
    R2?: string;
    R3?: string;
    R4?: string;
    TotalStrokes?: string;
    Earnings?: string;
    FedexPts?: string;
    TournamentId: ObjectId;
    Rounds: ObjectId[];
    created_at?: Date;
    updated_at?: Date;
}

interface Golfer {
    id?: ObjectId;  // Optional, maps to '_id'
    Rank?: string;
    FirstName: string;
    LastName: string;
    Age?: number;
    Earnings?: number;
    FedexPts?: number;
    Events?: number;
    Rounds?: number;
    Flag?: string;
    Cuts?: number;
    Top10s?: number;
    Wins?: number;
    AvgScore?: number;
    GolferPageLink?: string;
    Birthdate?: Date;
    Birthplace?: string;
    HtWt?: string;
    College?: string;
    Swing?: string;
    TurnedPro?: string;
    TournamentDetails?: GolferTournamentDetails[];
    OWGR?: string;
    created_at?: Date;
    updated_at?: Date;
}

interface GolfersResponse {
    golfers: Golfer[];
    nextPage?: number; // For pagination
}

// Fetch golfers with pagination
const fetchAvailableGolfers = async ({ pageParam = 0, leagueId }: { pageParam?: number; leagueId: string }): Promise<GolfersResponse> => {
    try {
        const response = await axios.get<GolfersResponse>(`/api/golfers/available_golfers/leagues/${leagueId}?page=${pageParam}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching available golfers:', error);
        // You can also throw a specific error or return a fallback value if needed
        throw error; // Rethrow the error to be handled by React Query
    }
};

export default function Golfers() {
    // Retrieve the league ID from the URL
    const { leagueId: leagueId } = useParams<{ leagueId: string }>();

    // Use React Query for infinite pagination
    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetching,
        isFetchingNextPage,
        isError, // Check for errors
        error,   // Access the error object
    } = useInfiniteQuery({
        queryKey: ['golfers', leagueId],
        queryFn: ({ pageParam }) => fetchAvailableGolfers({ pageParam, leagueId: leagueId! }),
        initialPageParam: 0,
        getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined, // Ensure it returns undefined if no `nextPage`
    });

    const allGolfers = data?.pages.flatMap(page => page.golfers) || [];

    const displayRoster = allGolfers.map((golfer, idx) => (
        <PlayerData
            key={String(golfer.id)}
            name={golfer.FirstName + " " + golfer.LastName}
            rank={String(golfer.Rank)}
            age={golfer.Age}
            even={idx % 2 === 0}
        />
    ));

    // Render error message if there's an error
    if (isError) {
        return <div>Error: {error instanceof Error ? error.message : 'An unexpected error occurred.'}</div>;
    }

    const headers = ["Place", "Golfer", "R1", "Thru", "Total", "Projected Place"];

    return (
        <div className="w-full h-full overflow-auto text-light font-PTSans break-all">
            <div>
                <DashboardTitle title="Golfers" />
                <TableHeaders headers={headers} />
            </div>
            {displayRoster}
            <div className="flex justify-center p-4">
                {hasNextPage && !isFetchingNextPage && (
                    <button onClick={() => fetchNextPage()} className="btn-primary">
                        Load More
                    </button>
                )}
                {isFetching && <p>Loading...</p>}
            </div>
        </div>
    );
}