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
        setSelectedTeamByUserId(state, action) {
            // Find the team based on the UserId
            const selectedTeam = state.leaguesTeams.find(team => team.OwnerId === action.payload);

            // If a team is found, set it as the selected team and filter it out from the teams array
            if (selectedTeam) {
                state.userSelectedTeam = selectedTeam;

                // Filter out the selected team from the teams array to avoid duplication
                state.leaguesTeams = state.userTeams.filter(team => team.OwnerId !== action.payload);
            }
        },
        setLeagueTeams(state, action) {
            const teams = action.payload
            if (state.userSelectedTeam) {
                state.leaguesTeams = teams.filter((team: Team) => team.id === state.userSelectedTeam?.id)
            } else {
                state.leaguesTeams = teams.map((team: Team) => team);
            }
        }
    },
    extraReducers: builder => {
        builder
    }
});

export const { setTeams, setLeagueTeams, setSelectedTeamByUserId } = teamsSlice.actions;

export default teamsSlice.reducer;