import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { fetchWrapper } from "../../Utils/methods/helpers";
import axios from "axios";

export const getLeague = createAsyncThunk(
    "leagues/league_id", 
    (league_id, thunkAPI) => {
    response = axios.get(`/api/leagues/${league_id}`, thunkAPI);
    return response.data;
});

const initialState = {
    league: {},
};

const leagueSlice = createSlice({
    name: "league",
    initialState,
    reducers: {

    },
    extraReducers: builder => {
    }
});

export const { } = leagueSlice.actions;

export default leagueSlice.reducer;