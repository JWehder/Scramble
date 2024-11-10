import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { fetchWrapper } from "../../Utils/methods/helpers";
import axios, { AxiosResponse } from "axios";
import { League } from "../../../types/leagues";

interface LeagueResponse {
    data: League;
}

export const getLeague = createAsyncThunk<LeagueResponse, string>(
    "leagues/fetchLeagueById",
    async (league_id, thunkAPI) => {
        if (!league_id) {
            return thunkAPI.rejectWithValue("League ID is undefined");
        }
        try {
            const response: AxiosResponse<LeagueResponse> = await axios.get(`/api/leagues/${league_id!}`);
            return response.data;
        } catch (error) {
            return thunkAPI.rejectWithValue(error);
        }
    }
);

interface LeagueState {
    status: string;
    selectedLeague: League | undefined;
    leagueError: string | null
}

const initialState: LeagueState = {
    status: "idle",
    selectedLeague: undefined,
    leagueError: null
};

const leagueSlice = createSlice({
    name: "league",
    initialState,
    reducers: {

    },
    extraReducers: builder => {
        builder
        .addCase(getLeague.pending, (state) => {
            state.status = "loading";
            state.leagueError = null;
        })
        .addCase(getLeague.fulfilled, (state, action) => {
            state.status = "succeeded";
            state.selectedLeague = action.payload.data; // assuming 'data' is the key for your league data
            state.leagueError = null;
        })
        .addCase(getLeague.rejected, (state, action) => {
            state.status = "failed";
            state.leagueError = action.error.message || "Failed to fetch league data";
        });
    }
});

export const { } = leagueSlice.actions;

export default leagueSlice.reducer;