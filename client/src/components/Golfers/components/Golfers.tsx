import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../User/components/home/TableHeaders"
import { useParams } from "react-router-dom";
import React, { useEffect } from "react";
import { useInfiniteQuery } from "@tanstack/react-query";
import axios from "axios";
import { useInView } from "react-intersection-observer";

interface Golfer {
    id?: string;  // String instead of ObjectId since it comes from API
    Rank?: number;
    FirstName: string;
    LastName: string;
    Age?: number;
    Country?: string;
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
    OWGR?: number | undefined;
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

    const { ref, inView } = useInView();

    useEffect(() => {
        if (inView && hasNextPage) {
            fetchNextPage();
        };
    }, [inView, fetchNextPage]);

    const headers = ["Fedex Rank", "Golfer", "Avg Score", "Wins", "Top 10s", "Fedex Pts"];

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
                            rank={golfer.Rank}
                            age={golfer.Age}
                            even={idx % 2 === 0}
                            country={golfer.Birthplace}
                            flag={golfer.Flag}
                            fedexPts={golfer.FedexPts}
                            top10s={golfer.Top10s}
                            wins={golfer.Wins}
                            avgScore={golfer.AvgScore}
                        />
                    ))}
                </div>
            ))}
            <div className="flex justify-center p-4">
                <div ref={ref}></div>
                {isFetching && <p>Loading...</p>}
            </div>
        </div>
    );
}
