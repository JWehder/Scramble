import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import { fetchWrapper } from "../../Utils/methods/helpers";
import axios from "axios";

const initialState = {
    user: false,
}

const leagueSlice = createSlice({
    name: "user",
    initialState,
    reducers: {

    }
});

export const { } = leagueSlice.actions;

export default leagueSlice.reducer;