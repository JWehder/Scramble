import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { Golfer } from "../../../types/golfers";

interface GolferState {
    status: string;
    showGolferModal: boolean;
    selectedGolfer: Golfer | undefined;
}

const initialState: GolferState = {
    status: "idle",
    showGolferModal: false,
    selectedGolfer: undefined,
};

const golferSlice = createSlice({
    name: "golfer",
    initialState,
    reducers: {
        setSelectedGolfer (state, action) {
            state.selectedGolfer = action.payload;
        },
        unsetSelectedGolfer (state) {
            state.selectedGolfer = undefined;
        }
    },
    extraReducers: builder => {
        builder
    }
});

export const { setSelectedGolfer, unsetSelectedGolfer } = golferSlice.actions;

export default golferSlice.reducer;