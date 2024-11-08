import React from "react";
import TableHeaders from "./TableHeaders";

export default function TournamentSchedule() {

    const headers: string[] = ["dates", "tournament name", "location/venue", "previous winner"]

    return (
        <TableHeaders headers={headers} />
        
    )
}