import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { ObjectId } from 'mongodb';

interface GolferTournamentDetails {
    id?: ObjectId;  // Optional, maps to '_id'
    GolferId: ObjectId;
    Position: string;
    Name: string;
    Score: string;
    R1?: string;
    R2?: string;
    R3?: string;
    R4?: string;
    TotalStrokes?: string;
    Earnings?: string;
    FedexPts?: string;
    TournamentId: ObjectId;
    Rounds: ObjectId[];
    created_at?: Date;
    updated_at?: Date;
}

interface Golfer {
    id?: ObjectId;  // Optional, maps to '_id'
    Rank?: string;
    FirstName: string;
    LastName: string;
    Age?: number;
    Earnings?: number;
    FedexPts?: number;
    Events?: number;
    Rounds?: number;
    Flag?: string;
    Cuts?: number;
    Top10s?: number;
    Wins?: number;
    AvgScore?: number;
    GolferPageLink?: string;
    Birthdate?: Date;
    Birthplace?: string;
    HtWt?: string;
    College?: string;
    Swing?: string;
    TurnedPro?: string;
    TournamentDetails?: GolferTournamentDetails[];
    OWGR?: string;
    created_at?: Date;
    updated_at?: Date;
}

interface ErrorResponse {
    data: string;
}

export const getAvailableGolfers = createAsyncThunk<
    Golfer[], // Return type of fulfilled action
    string, // Type of `league_id` parameter
    { rejectValue: ErrorResponse } // Type of the error returned on rejection
>(
    "/auth/available_golfers",
    async (league_id, thunkAPI) => {
        try {
            const response = await axios.get<Golfer[]>(`/api/golfers/available_golfers/leagues/${league_id}`);
            return response.data;
        } catch (err: any) {
            const error: ErrorResponse = { data: err.response?.data.error || 'Unknown error' };
            return thunkAPI.rejectWithValue(error);
        }
    }
);

const initialState = {
    status: "idle", 
};

const golferSlice = createSlice({
    name: "golfer",
    initialState,
    reducers: {

    },
    extraReducers: builder => {
        builder
        .addCase(getAvailableGolfers.pending, (state) => {
            state.status = "loading";
          })
        .addCase(getAvailableGolfers.fulfilled, (state, action) => {
            console.log(action.payload);
            state.status = "idle";
        })
        .addCase(getAvailableGolfers.rejected, (state, action) => {
            console.log(action.payload);
        })
    }
});

export const { } = golferSlice.actions;

export default golferSlice.reducer;