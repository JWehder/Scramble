import DashboardTitle from "../../User/components/home/DashboardTitle";
import PlayerData from "./PlayerData";
import TableHeaders from "../../Utils/components/TableHeaders"
import { useParams } from "react-router-dom";
import React, { useEffect } from "react";
import { useInView } from "react-intersection-observer";
import { useFetchAvailableGolfers } from "../../../hooks/golfers";
import { useDispatch } from "react-redux";
import { setSelectedGolfer } from "../state/golferSlice";
import SkeletonTable from "../../Utils/components/SkeletonTable";

export default function Golfers() {
    // Retrieve the league ID from the URL
    const { leagueId } = useParams<{ leagueId: string }>();
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

    const headers = ["Fedex Rank", "Golfer", "Avg Score", "Top 10s", "Wins", "Cuts Made", "Fedex Pts"];

    // Render error message if there's an error
    if (isError) {
        return <div>Error: {error instanceof Error ? error.message : 'An unexpected error occurred.'}</div>;
    };

    const handleGolferClick = (golfer: object) => {
        dispatch(setSelectedGolfer(golfer));
    };

    return (
        <div className="w-full h-full overflow-auto text-light font-PTSans break-all bg-middle p-2">

            <div>
                <TableHeaders headers={headers} />
            </div>
            {data?.pages.map((page, pageIndex) => (
                <div 
                key={pageIndex + (page.nextPage || 0)}
                >
                    {page.golfers.map((golfer, idx) => (
                        <PlayerData
                            key={golfer.id}
                            even={idx % 2 == 0}
                            player={golfer}
                            onClick={() => handleGolferClick(golfer)}
                        />
                    ))}
                </div>
            ))}
            <div className="flex justify-center p-4">
                <div ref={ref}></div>
                {isFetching && <SkeletonTable />}
            </div>
        </div>
    );
}
