import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../User/components/home/TableHeaders"
import { useParams } from "react-router-dom";
import React from "react";
import { useInfiniteQuery } from "@tanstack/react-query";
import axios from "axios";

interface Golfer {
    id?: string;  // String instead of ObjectId since it comes from API
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
    OWGR?: string;
    created_at?: Date;
    updated_at?: Date;
}

interface GolfersResponse {
    golfers: Golfer[];
    nextPage?: number | null; // Handle the optional nextPage
}

// Fetch golfers with pagination
const fetchAvailableGolfers = async ({ pageParam = 0, leagueId }: { pageParam?: number; leagueId: string }): Promise<GolfersResponse> => {
    const response = await axios.get<GolfersResponse>(`/api/golfers/available_golfers/leagues/${leagueId}?page=${pageParam}`);
    console.log(response.data)
    return response.data;
};

export default function Golfers() {
    // Retrieve the league ID from the URL
    const { leagueId } = useParams<{ leagueId: string }>();

    // Use React Query for infinite pagination
    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetching,
        isFetchingNextPage,
        isError,
        error,
    } = useInfiniteQuery<GolfersResponse>({
        queryKey: ['golfers', leagueId],
        queryFn: ({ pageParam }) => fetchAvailableGolfers({ pageParam: pageParam as number, leagueId: leagueId! }),
        initialPageParam: 0,
        getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    });

    const headers = ["Place", "Golfer", "R1", "Thru", "Total", "Projected Place"];

    // Render error message if there's an error
    if (isError) {
        return <div>Error: {error instanceof Error ? error.message : 'An unexpected error occurred.'}</div>;
    }

    return (
        <div className="w-full h-full overflow-auto text-light font-PTSans break-all">
            <div>
                <DashboardTitle title="Golfers" />
                <TableHeaders headers={headers} />
            </div>
            {data?.pages.map((page, pageIndex) => (
                <div key={pageIndex + (page.nextPage || 0)}>
                    {page.golfers.map((golfer, idx) => (
                        <PlayerData
                            key={golfer.id}
                            name={`${golfer.FirstName} ${golfer.LastName}`}
                            rank={String(golfer.Rank)}
                            age={golfer.Age}
                            even={idx % 2 === 0}
                        />
                    ))}
                </div>
            ))}
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
