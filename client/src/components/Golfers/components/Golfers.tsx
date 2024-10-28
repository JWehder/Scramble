import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../User/components/home/TableHeaders"
import { useParams } from "react-router-dom";
import React from "react";
import { useDispatch } from "react-redux";
import { getAvailableGolfers } from "../state/golferSlice";
import { useInfiniteQuery } from "@tanstack/react-query";
import axios from "axios";

// Fetch golfers with league ID for pagination
const fetchAvailableGolfers = async ({ pageParam = 0, leagueId }: { pageParam?: number; leagueId: string }) => {
    const response = await axios.get(`/api/golfers/available_golfers/leagues/${leagueId}?page=${pageParam}`);
    return response.data;
};

export default function Golfers() {
    // Retrieve the league ID from the URL
    const { id: leagueId } = useParams<{ id: string }>();

    // Use React Query for infinite pagination
    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetching,
        isFetchingNextPage,
    } = useInfiniteQuery(
        ['golfers', leagueId],
        ({ pageParam }) => fetchAvailableGolfers({ pageParam, leagueId: leagueId! }),
        {
            getNextPageParam: (lastPage: GolfersResponse) => lastPage.nextPage, // Define lastPage type
        }
    );

    // Map golfers for rendering
    const displayRoster = data?.pages.map((page) =>
        page.golfers.map((player, idx) => (
            <PlayerData
                key={player.id}
                name={player.FirstName + " " + player.LastName}
                rank={player.Rank}
                age={player.Age}
                even={idx % 2 === 0}
            />
        ))
    );

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