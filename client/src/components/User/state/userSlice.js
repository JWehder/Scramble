import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    leagues: [
        {
        "name": "Jake's League",
        "team1Name": "Jake's team"
        },
        {
        "name": "Jake's League",
        "team1Name": "Jake's team"
        },
        {
        "name": "Jake's League",
        "team1Name": "Jake's team"
        }
    ],
    messages: [
    "Hey there!",
    "Hey there!",
    "Hey there!"
    ],
    articles: [
    {
        "title": "Outrageous Hole Out by Tiger",
        "caption": "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. The shot was so close to the pin and the crowd was going wild. If you have not seen it yet, you have to! See video below:"
    },
    {
        "title": "Outrageous Hole Out by Tiger",
        "caption": "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. See video below:"
    },
    {
        "title": "Outrageous Hole Out by Tiger",
        "caption": "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. See video below:"
    }
    ],
    games: ["Best Ball", "Match Play", "Stroke Play"],
}

const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {}
});

export const {} = userSlice.actions;

export default userSlice.reducer;