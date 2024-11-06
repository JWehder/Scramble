import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../User/components/home/TableHeaders"
import { useParams } from "react-router-dom";
import React, { useEffect, useState } from "react";
import {  useQueryClient } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import Modal from "../../Utils/components/Modal";
import PlayerPage from "./player/PlayerPage";
import { useFetchAvailableGolfers } from "../../../hooks/golfers";
import { useDispatch, useSelector } from "react-redux";
import { setSelectedGolfer } from "../state/golferSlice";
import { RootState } from "../../../store";

export default function Golfers() {
    // Retrieve the league ID from the URL
    const { leagueId } = useParams<{ leagueId: string }>();
    const queryClient = useQueryClient();
    const dispatch = useDispatch();

    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetching,
        isFetchingNextPage,
        isError,
        error,
    } = useFetchAvailableGolfers(leagueId!);

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
    };

    const handleGolferClick = (golfer: object) => {
        dispatch(setSelectedGolfer(golfer));
    };

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
                            onClick={() => handleGolferClick(golfer)}
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
