import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
    status: "idle", 
    showGolferModal: false,
    selectedGolfer: null,
};

const golferSlice = createSlice({
    name: "golfer",
    initialState,
    reducers: {
        setSelectedGolfer (state, action) {
            state.selectedGolfer = action.payload;
        }
    },
    extraReducers: builder => {
        builder
    }
});

export const {  } = golferSlice.actions;

export default golferSlice.reducer;