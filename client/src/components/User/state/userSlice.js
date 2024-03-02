import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import { fetchWrapper } from "../../Utils/methods/helpers";
import axios from "axios";

export const login = createAsyncThunk(
    "auth/login", 
    (userObj, thunkAPI) => {
        return fetchWrapper.post("/login", userObj, thunkAPI);
});

export const getUser = createAsyncThunk("auth/getUser", async(_, thunkAPI) => {
    try {
        const response = await axios.get('/me');
        return response.data;
    } catch (err) {
        // Handle the error
        const error = err.response.data.errors;
        return thunkAPI.rejectWithValue({ data: error });
    }
});

export const signup = createAsyncThunk(
    "auth/signup", 
    (userObj, thunkAPI) => {
    return fetchWrapper.post("/signup", userObj, thunkAPI);
});

export const updateUser = createAsyncThunk("/auth/updateUser", async(userObj, thunkAPI) => {
        const { id, ...rest } = userObj;
        return fetchWrapper.patch(`/users/${id}`, rest, thunkAPI);
});

export const logout = createAsyncThunk("/auth/logout", async( thunkAPI) => {
    try {
        const response = await axios.delete(`/logout`);
        return response.data;
    } catch (err) {
        const error = err.response.data.errors;
        return thunkAPI.rejectWithValue(error);
    }
});

export const forgotPassword = createAsyncThunk(
    "auth/forgotPassword", 
    (email, thunkAPI) => {
    return fetchWrapper.post("/forgot_password", email, thunkAPI);
});

export const resetPassword = createAsyncThunk(
    "auth/resetPassword", 
    (code, thunkAPI) => {
    return fetchWrapper.post("/reset_password", code, thunkAPI);
});

const initialState = {
    user: true,
    loginError: null,
    signupError: null,
    updateError: null,
    logoutError: null,
    loginModal: false,
    status: "idle",
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
    reducers: {
        setEmailSent (state, action) {
            state.emailSent = action.payload;
        },
        setSavedChanges (state, action) {
            state.savedChanges = action.payload;
        },
        setLoginModal (state, action) {
            state.loginModal = action.payload;
        }
    },
    extraReducers: builder => {
        builder
        .addCase(login.pending, (state) => {
          state.status = "pending";
          state.loginError = null;
        })
        .addCase(login.fulfilled, (state, action) => {
          state.user = action.payload;
          state.status = "idle";
        })
        .addCase(login.rejected, (state, action) => {
          console.log(action.payload);
          state.loginError = action.payload;
        })
        .addCase(getUser.pending, (state) => {
          state.status = "loading";
        })
        .addCase(getUser.fulfilled, (state, action) => {
          console.log(action.payload);
          state.user = action.payload;
          state.status = "idle";
        })
        .addCase(getUser.rejected, (state, action) => {
          console.log(action.payload);
          state.user = null;
        })
        .addCase(signup.pending, (state) => {
          state.status = "pending";
          state.signupError = null;
        })
        .addCase(signup.fulfilled, (state) => {
          state.status = "idle";
        })
        .addCase(signup.rejected, (state, action) => {
          state.signupError = action.payload;
        })
        .addCase(updateUser.pending, (state) => {
          state.status = "pending";
          state.updateError = null;
        })
        .addCase(updateUser.fulfilled, (state, action) => {
          state.user = action.payload;
          state.savedChanges = true;
          state.status = "idle";
        })
        .addCase(updateUser.rejected, (state, action) => {
          state.updateError = action.payload;
        })
        .addCase(logout.pending, (state) => {
          state.status = "pending";
          state.signupError = null;
        })
        .addCase(logout.fulfilled, (state) => {
          state.user = null;
          state.status = "idle";
        })
        .addCase(logout.rejected, (state, action) => {
          state.logoutError = action.payload;
        })
        .addCase(forgotPassword.pending, (state) => {
          state.status = "pending";
          state.loginError = null;
        })
        .addCase(forgotPassword.fulfilled, (state) => {
          state.status = "idle";
        })
        .addCase(forgotPassword.rejected, (state, action) => {
          // Handle rejection if needed
        })
        .addCase(resetPassword.pending, (state) => {
          state.status = "pending";
          state.loginError = null;
        })
        .addCase(resetPassword.fulfilled, (state) => {
          state.status = "idle";
        })
        .addCase(resetPassword.rejected, (state, action) => {
          state.resetPasswordError = action.payload;
        });
    }
});

export const { setSavedChanges, setLoginModal } = userSlice.actions;

export default userSlice.reducer;