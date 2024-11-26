import { createSlice } from "@reduxjs/toolkit";
import { Team } from "../../../types/teams"

interface LeagueState {
    status: string;
    userTeams: Team[];
    leaguesTeams: Team[];
    userSelectedTeam: Team | null;
    teamsError: string | null
}

const initialState: LeagueState = {
    status: "idle",
    userTeams: [],
    leaguesTeams: [],
    userSelectedTeam: null,
    teamsError: null
};

const teamsSlice = createSlice({
    name: "teams",
    initialState,
    reducers: {
        setTeams(state, action) {
            state.userTeams = action.payload;
        },        
        clearSelectedTeam(state) {
            state.userSelectedTeam = null;  // Optionally, clear selected team
        },
        setSelectedTeam(state, action) {
            // Find the team based on the LeagueId
            const selectedTeam = state.userTeams.find(team => team.LeagueId === action.payload);

            // If a team is found, set it as the selected team and filter it out from the teams array
            if (selectedTeam) {
                state.userSelectedTeam = selectedTeam;

                // Filter out the selected team from the teams array to avoid duplication
                state.userTeams = state.userTeams.filter(team => team.LeagueId !== action.payload);
            }
        },
        setLeagueTeams(state, action) {
            state.leaguesTeams = action.payload
        }
    },
    extraReducers: builder => {
        builder
    }
});

export const { setTeams, setLeagueTeams, setSelectedTeam } = teamsSlice.actions;

export default teamsSlice.reducer;