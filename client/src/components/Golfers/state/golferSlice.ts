import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

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
    }
});

export const { } = golferSlice.actions;

export default golferSlice.reducer;