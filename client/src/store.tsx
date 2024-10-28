import { configureStore } from "@reduxjs/toolkit";
import usersReducer from "./components/User/state/userSlice";
import leaguesReducer from "./components/Leagues/state/leagueSlice";

const store = configureStore({
    reducer:{
        users: usersReducer,
        leagues: leaguesReducer
    },
});

// Infer the `RootState` type from the store
export type RootState = ReturnType<typeof store.getState>;

// Export the store
export default store;
