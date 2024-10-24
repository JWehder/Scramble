import { configureStore } from "@reduxjs/toolkit";
import usersReducer from "./components/User/state/userSlice";
import leaguesReducer from "./components/Leagues/state/leagueSlice";

const store = configureStore({
    reducer:{
        users: usersReducer,
        leagues: leaguesReducer
    },
});

export default store;