import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import { fetchWrapper } from "../../Utils/methods/helpers";
import axios from "axios";

export const login = createAsyncThunk(
    "auth/login", 
    (userObj, thunkAPI) => {
        return fetchWrapper.post("/api/auth/login", userObj, thunkAPI);
});

export const verifyEmail = createAsyncThunk(
  "auth/verify_email", 
  (codeAndEmail, thunkAPI) => {
      return fetchWrapper.post("/api/auth/verify_email", codeAndEmail, thunkAPI);
});

export const resendCode = createAsyncThunk(
  "auth/send_new_verify_email_code", 
  (email, thunkAPI) => {
  return fetchWrapper.post("/api/auth/send_new_verify_email_code", {"email": email}, thunkAPI);
});

export const getUser = createAsyncThunk("/auth/getUser", async(_, thunkAPI) => {
    try {
        const response = await axios.get('/api/auth/me');
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
    return fetchWrapper.post("/api/auth/signup", userObj, thunkAPI);
});

export const updateUser = createAsyncThunk("/auth/updateUser", async(userObj, thunkAPI) => {
        const { id, ...rest } = userObj;
        return fetchWrapper.patch(`/api/auth/users/${id}`, rest, thunkAPI);
});

export const logout = createAsyncThunk("/auth/logout", async( thunkAPI) => {
    try {
        const response = await axios.delete(`/api/auth/logout`);
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
    user: false,
    loginErrors: null,
    signupErrors: null,
    updateError: null,
    resendCodeError: null,
    verifyEmailError: null,
    logoutError: null,
    resendCodeStatus: "idle",
    loginModal: false,
    showLogin: true,
    showVerifyEmail: false,
    verifiedBanner: false,
    status: "idle",
    playerModal: true,
    holesComparisonChart: false,
    tempUser: false,
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
        setLoginModal(state, action) {
          if (!action.payload) {
            // Reset the entire state when closing the modal
            return { ...initialState };
          } else {
            // Only update the loginModal value
            state.loginModal = action.payload;
          }
        },
        setPlayerModal (state) {
          state.playerModal = !(state.playerModal);
        },
        setHolesComparisonChart (state) {
          state.holesComparisonChart = !state.holesComparisonChart;
        },
        setShowLogin (state, action) {
          state.showLogin = action.payload;
        },
        clearLoginErrors (state) {
          state.loginErrors = null;
        },
        clearSignupErrors (state) {
          state.signupErrors = {};
        },
        closeVerifyEmail (state) {
          state.showVerifyEmail = false;
        },
        clearResendCodeError (state) {
          state.resendCodeError = null;
        },
        clearVerifyEmailError (state) {
          state.verifyEmailError = null;
        }
    },
    extraReducers: builder => {
        builder
        .addCase(verifyEmail.pending, (state) => {
          state.status = "pending";
          state.loginErrors = null;
        })
        .addCase(verifyEmail.fulfilled, (state, action) => {
          state.status = "idle";
          state.showVerifyEmail = false;
          if (state.showLogin) {
            state.loginModal = false;
            state.showLogin = true;
          } else {
            console.log("it is supposed to be working correctly.")
            state.showLogin = true;
            state.verifiedBanner = true;
          }

          // if the user verified their email after login
          // set up the user state and allow them in via signedInHome
          if (action.payload.User) {
            console.log("hit me");
            state.user = true;
          };
        })
        .addCase(verifyEmail.rejected, (state, action) => {
          state.verifyEmailError = action.payload.error;
        })
        .addCase(resendCode.pending, (state) => {
          state.resendCodeStatus = "pending";
        })
        .addCase(resendCode.fulfilled, (state) => {
          state.resendCodeStatus = "idle";
        })
        .addCase(resendCode.rejected, (state, action) => {
          state.resendCodeStatus = "rejected";
          state.resendCodeError = action.payload.error;
        })
        .addCase(login.pending, (state) => {
          state.status = "pending";
          state.loginErrors = null;
        })
        .addCase(login.fulfilled, (state, action) => {
          state.status = "idle";
          state.showLogin = false;
          if (!action.payload.IsVerified) {
            state.showVerifyEmail = true;
          } else {
            state.loginModal = false;
          };
        })
        .addCase(login.rejected, (state, action) => {
          state.loginErrors = action.payload;
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
          state.signupErrors = null;
        })
        .addCase(signup.fulfilled, (state) => {
          state.status = "idle";
          state.showVerifyEmail = true;
        })
        .addCase(signup.rejected, (state, action) => {
          console.log(action.payload)
          if (typeof(action.payload) === Object) {
            state.signupErrors = {...action.payload};
          } else {
            state.signupErrors = action.payload;
          }
          console.log(state.signupErrors)
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
          state.signupErrors = null;
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
          state.loginErrors = null;
        })
        .addCase(forgotPassword.fulfilled, (state) => {
          state.status = "idle";
        })
        .addCase(forgotPassword.rejected, (state, action) => {
          // Handle rejection if needed
        })
        .addCase(resetPassword.pending, (state) => {
          state.status = "pending";
          state.loginErrors = null;
        })
        .addCase(resetPassword.fulfilled, (state) => {
          state.status = "idle";
        })
        .addCase(resetPassword.rejected, (state, action) => {
          state.resetPasswordError = action.payload;
        });
    }
});

export const { setSavedChanges, setLoginModal, setPlayerModal, holesComparisonChart, setHolesComparisonChart, setShowLogin, showLogin, clearLoginErrors, clearSignupErrors, showVerifyEmail, closeVerifyEmail, verifiedBanner, clearResendCodeError, clearVerifyEmailError } = userSlice.actions;

export default userSlice.reducer;