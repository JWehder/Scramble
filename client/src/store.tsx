import { configureStore } from "@reduxjs/toolkit";
import usersReducer from "./components/User/state/userSlice";
import leaguesReducer from "./components/Leagues/state/leagueSlice";
import golfersReducer from "./components/Golfers/state/golferSlice";

const store = configureStore({
    reducer:{
        users: usersReducer,
        leagues: leaguesReducer,
        golfers: golfersReducer
    },
});

// Infer the `RootState` type from the store
export type RootState = ReturnType<typeof store.getState>;

// Export the store
export default store;
