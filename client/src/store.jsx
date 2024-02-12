import { configureStore } from "@reduxjs/toolkit";
import usersReducer from "./components/Sidebar/state/userSlice";

const store = configureStore({
    reducer:{
        users: usersReducer
    },
});

export default store;