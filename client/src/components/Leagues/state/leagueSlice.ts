import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios, { AxiosResponse } from "axios";
import { League } from "../../../types/leagues";
import { setLeagueTeams } from "../../Teams/state/teamsSlice"
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../../store";

export const getLeague = createAsyncThunk<League, string>(
    "leagues/fetchLeagueById",
    async (league_id, thunkAPI) => {
        if (!league_id) {
            return thunkAPI.rejectWithValue("League ID is undefined");
        }
        try {
            const response: AxiosResponse<League> = await axios.get(`/api/leagues/${league_id!}`);
            const data = response.data

            // Destructure the data to pull out `Teams` and the rest of the league data
            const { Teams, ...leagueWithoutTeams } = data;

            // Dispatch teams to the teams slice
            thunkAPI.dispatch(setLeagueTeams(Teams));

            // Return the rest of the league data (without Teams) for the league slice
            return leagueWithoutTeams;

        } catch (error) {
            return thunkAPI.rejectWithValue(error);
        }
    }
);

interface LeagueState {
    status: string;
    leagues: League[];
    selectedLeague: League | null
    leagueError: string | null
}

const initialState: LeagueState = {
    status: "idle",
    leagues: [],
    selectedLeague: null,
    leagueError: null
};

const leagueSlice = createSlice({
    name: "leagues",
    initialState,
    reducers: {
        setLeagues(state, action) {
            state.leagues = action.payload;
        },
        clearSelectedLeague(state) {
            state.selectedLeague = null;
        }
    },
    extraReducers: builder => {
        builder
        .addCase(getLeague.pending, (state) => {
            state.status = "loading";
            state.leagueError = null;
        })
        .addCase(getLeague.fulfilled, (state, action) => {
            state.status = "succeeded";
            state.selectedLeague = action.payload; // assuming 'data' is the key for your league data
            state.leagueError = null;
        })
        .addCase(getLeague.rejected, (state, action) => {
            state.status = "failed";
            state.leagueError = action.error.message || "Failed to fetch league data";
        });
    }
});

export const { setLeagues } = leagueSlice.actions;

export default leagueSlice.reducer;