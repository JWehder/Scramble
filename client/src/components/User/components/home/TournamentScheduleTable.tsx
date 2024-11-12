import React, { useState } from "react";
import { useSelector } from "react-redux";
import TableRow from "../../../Utils/components/TableRow";
import { RootState } from "../../../../store";
import { Tournament } from "../../../../types/tournaments";
import TableHeaders from "./TableHeaders";
import { useFetchTournamentDetails } from "../../../../hooks/tournaments";

export default function TournamentScheduleTable({ setSelectedTournament }) {

    const currentFantasyLeagueSeasonId = useSelector((state: RootState) => state.leagues.selectedLeague?.CurrentFantasyLeagueSeasonId)

    const { data,
        isFetching,
        isSuccess,
        isError
    } = useFetchTournamentDetails(currentFantasyLeagueSeasonId);

    const desiredKeysSet = new Set(["City", "State", "Purse", "PreviousWinner"]);

    const headers = ["Date", "Tournament Name", "City", "State", "Purse", "Winner"];

    return (
        <div className="bg-middle rounded-xl text-light">
            <TableHeaders headers={headers} />
            { isSuccess && data?.tournaments.map((tournament: Tournament, idx) => {
                let newDesiredKeysSet = {};
                // Replace "PreviousWinner" with "Winner"
                if (desiredKeysSet.has("PreviousWinner")) {
                    desiredKeysSet.delete("PreviousWinner"); // Remove the old value
                    desiredKeysSet.add("Winner"); // Add the new value
}
                return  (
                <TableRow 
                firstTwoDatapoints={[tournament.StartDate, tournament.Name]}
                data={tournament}
                columns={desiredKeysSet}
                brightness={idx % 2 === 0 ? 'brightness-125' : ''}
                onClick={() => setSelectedTournament(tournament)}
                />
                )
            })}
            { isError && <div>Error loading tournament details.</div> }
            { isFetching && <div>Loading...</div> }
        </div>
    )
}