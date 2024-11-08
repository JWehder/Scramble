import React, { useEffect, useState } from "react";
import TableHeaders from "./TableHeaders";
import axios from "axios";
import { Tournament } from "../../../../types/tournaments";

export default function TournamentSchedule() {
    const [tournaments, setTournaments] = useState<Tournament[] | null>();

    useEffect(() => {
        const response = axios.get(``)
    }, [])

    const headers: string[] = ["dates", "tournament name", "location/venue", "previous winner"]

    return (
        <>
            <TableHeaders headers={headers} />

        </>

    )
}