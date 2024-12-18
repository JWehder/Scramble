import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios, { AxiosResponse } from "axios";
import { Golfer } from "../../../types/golfers";

interface GolfersDetailsIdsResponse {
    golfer_scores_ids: string[]
}

export const getLeaguesGolferDetails = createAsyncThunk<GolfersDetailsIdsResponse, { tournamentId: string; leagueId: string }>(
    "periods/fetchLeaguesGolferDetails",
    async ({ tournamentId, leagueId }, thunkAPI) => {
        if (!tournamentId) {
            return thunkAPI.rejectWithValue("Tournament ID is undefined");
        }
        try {
            const response: AxiosResponse<GolfersDetailsIdsResponse> = await axios.post(`/api/periods/fetch_participating_golfers/tournaments/${tournamentId}`, {"leagueId": leagueId});
            return response.data;
        } catch (error) {
            return thunkAPI.rejectWithValue(error);
        }
    }
);

interface GolferState {
    status: string;
    showGolferModal: boolean;
    selectedGolfer: Golfer | undefined;
    leaguesGolfersTournamentDetailsIds: Set<string> | null;
    getLeaguesGolferDetailsIdsError: string | null;
}

const initialState: GolferState = {
    status: "idle",
    showGolferModal: false,
    selectedGolfer: undefined,
    leaguesGolfersTournamentDetailsIds: null,
    getLeaguesGolferDetailsIdsError: null
};

const golferSlice = createSlice({
    name: "golfer",
    initialState,
    reducers: {
        setSelectedGolfer(state, action) {
            state.selectedGolfer = action.payload;
        },
        resetSelectedGolfer(state) {
            state.selectedGolfer = undefined;
        },
        resetLeaguesGolfersTournamentDetailsIds(state) {
            state.leaguesGolfersTournamentDetailsIds = null;
        }
    },
    extraReducers: builder => {
        builder
        .addCase(getLeaguesGolferDetails.pending, (state) => {
            state.status = "loading";
            state.getLeaguesGolferDetailsIdsError = null;
        })
        .addCase(getLeaguesGolferDetails.fulfilled, (state, action) => {
            state.status = "succeeded";
            console.log(action.payload);
            // Convert the array to a Set directly
            state.leaguesGolfersTournamentDetailsIds = new Set(action.payload.golfer_scores_ids);
            state.getLeaguesGolferDetailsIdsError = null;
        })
        .addCase(getLeaguesGolferDetails.rejected, (state, action) => {
            state.status = "failed";
            state.getLeaguesGolferDetailsIdsError = action.error.message || "Failed to fetch teams results and periods data";
        });
    }
});


export const { setSelectedGolfer, resetSelectedGolfer, resetLeaguesGolfersTournamentDetailsIds } = golferSlice.actions;

export default golferSlice.reducer;