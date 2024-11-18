import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import axios, { AxiosResponse } from "axios";
import { UsersData } from "../../../types/users";

interface ErrorPayload {
    error: string;
}

interface UserResponse {
    user: UsersData;
}

interface UsersMessage {
    message: string
}

interface LoginInfo {
    usernameOrEmail: string
    password: string
}

interface UpdateUserResponse {
    Username: string;
    Email: string;
    IsVerified: string;
}

interface SignupErrors {
    Username: string | undefined;
    Password: string | undefined;
    Email: string | undefined;
    general: string | undefined;
}

interface UserState {
    user: any | null;
    loginErrors: ErrorPayload | string | null;
    signupErrors: SignupErrors | { general: string } | null;
    updateError: ErrorPayload | string | null;
    resendCodeError: ErrorPayload | string | null;
    verifyEmailError: ErrorPayload | string | null;
    logoutError: ErrorPayload | string | null;
    resetPasswordError: ErrorPayload | string | null;
    resendCodeStatus: "idle" | "pending" | "rejected";
    showForgotPassword: boolean;
    loginModal: boolean;
    showLogin: boolean;
    showVerifyEmail: boolean;
    showCode: boolean;
    verifiedBanner: boolean;
    status: "idle" | "pending" | "loading";
    holesComparisonChart: boolean;
    tempUser: boolean;
    leagues: { name: string; team1Name: string }[];
    messages: string[];
    articles: { title: string; caption: string }[];
    games: string[];
}

const initialState: UserState = {
    user: null,
    loginErrors: null,
    signupErrors: null,
    updateError: null,
    resendCodeError: null,
    verifyEmailError: null,
    logoutError: null,
    resetPasswordError: null,
    resendCodeStatus: "idle",
    showForgotPassword: false,
    showCode: false,
    loginModal: false,
    showLogin: true,
    showVerifyEmail: false,
    verifiedBanner: false,
    status: "idle",
    holesComparisonChart: false,
    tempUser: false,
    leagues: [
        { name: "Jake's League", team1Name: "Jake's team" },
        { name: "Jake's League", team1Name: "Jake's team" },
        { name: "Jake's League", team1Name: "Jake's team" }
    ],
    messages: ["Hey there!", "Hey there!", "Hey there!"],
    articles: [
        { title: "Outrageous Hole Out by Tiger", caption: "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. See video below:" },
        { title: "Outrageous Hole Out by Tiger", caption: "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. See video below:" },
        { title: "Outrageous Hole Out by Tiger", caption: "Tiger plays the 16th hole of WM perfectly and nearly knocks in a hole. See video below:" }
    ],
    games: ["Best Ball", "Match Play", "Stroke Play"],
};

export const login = createAsyncThunk<
    UserResponse,
    LoginInfo,
    { rejectValue: ErrorPayload | undefined }
>("auth/login", async (credentials, thunkAPI) => {
    try {
        const response = await axios.post("/api/auth/login", credentials);
        return response.data;
    } catch (err: any) {
        const error = err.response.data;
        return thunkAPI.rejectWithValue(error);
    }
});

export const verifyEmail = createAsyncThunk<
    UsersMessage, 
    object, 
    { rejectValue: ErrorPayload | undefined }
    >(
    "auth/verify_email",
    async (codeAndEmail: object, thunkAPI) => {
        try{
            const response: AxiosResponse<UsersMessage> = await axios.post("/ api/auth/verify_email", codeAndEmail);
            return response.data
        } catch (err: any) {
            const error = err.response.data;
            return thunkAPI.rejectWithValue(error);
        }
    }
);

export const resendCode = createAsyncThunk<
    UsersMessage, 
    string,
    { rejectValue: ErrorPayload | undefined }
    >(
    "/api/auth/send_new_verify_email_code",
    async (email: string, thunkAPI) => {
        try {
            const response: AxiosResponse<UsersMessage> = await axios.post("/api/auth/send_new_verify_email_code", { email });
            return response.data
        } catch (err: any) {
            const error = err.response.data;
            return thunkAPI.rejectWithValue(error);
        }
    }
);

export const getUser = createAsyncThunk<UsersData, void, { rejectValue: ErrorPayload | undefined }>("/api/auth/me", async (_, thunkAPI) => {
    try {
        const response = await axios.get('/api/auth/me');
        return response.data;
    } catch (err: any) {
        const error = err.response.data;
        return thunkAPI.rejectWithValue(error);
    }
});

export const signup = createAsyncThunk<UsersMessage, LoginInfo, { rejectValue: SignupErrors }> (
    "auth/signup",
    async (userObj: LoginInfo, thunkAPI) => {
        try {
            const response: AxiosResponse<UsersMessage> = await axios.post("/api/auth/signup", userObj);
            return response.data;
        } catch (err: any) {
            const error = err.response.data;
            return thunkAPI.rejectWithValue(error);
        }
    }
);

export const updateUser = createAsyncThunk<
  UpdateUserResponse,
  { [key: string]: any },  // Type for userObj
  { rejectValue: ErrorPayload }
>(
  "/auth/updateUser",
  async (userObj, thunkAPI) => {  // Take userObj as the argument
    try {
      const response = await axios.patch(`/api/auth/update_user`, userObj);  // Pass userObj directly in the patch request
      return response.data;
    } catch (err: any) {
      const error = err.response.data;
      return thunkAPI.rejectWithValue(error);
    }
  }
);

export const logout = createAsyncThunk<UsersMessage, void, { rejectValue: ErrorPayload }>("/auth/logout", async (_, thunkAPI) => {
    try {
        const response: AxiosResponse<UsersMessage>  = await axios.delete(`/api/auth/logout`);
        return response.data;
    } catch (err: any) {
        const error = err.response.data;
        return thunkAPI.rejectWithValue(error);
    }
});

export const resetPassword = createAsyncThunk<UsersMessage, string, { rejectValue: ErrorPayload }>(
    "auth/resetPassword",
    async (password: string, thunkAPI) => {
        try {
            const response: AxiosResponse<UsersMessage> = await axios.post("api/auth/reset_password", { password });
            return response.data
        } catch (err: any) {
            const error = err.response.data;
            return thunkAPI.rejectWithValue(error);
        }

    }
);

const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setLoginModal(state, action: PayloadAction<boolean>) {
            if (!action.payload) {
                return { ...initialState };
            } else {
                state.loginModal = action.payload;
            }
        },
        setHolesComparisonChart(state) {
            state.holesComparisonChart = !state.holesComparisonChart;
        },
        setShowLogin(state, action: PayloadAction<boolean>) {
            state.showLogin = action.payload;
        },
        clearLoginErrors(state) {
            state.loginErrors = null;
        },
        clearSignupErrors(state) {
            state.signupErrors = null;
        },
        closeVerifyEmail(state) {
            state.showVerifyEmail = false;
        },
        clearResendCodeError(state) {
            state.resendCodeError = null;
        },
        clearVerifyEmailError(state) {
            state.verifyEmailError = null;
        },
        resetShowCode(state) {
            state.showCode = false;
        }
    },
    extraReducers: (builder) => {
        builder
        // Login action
        .addCase(login.pending, (state) => {
            state.status = "pending";
            state.loginErrors = null;
        })
        .addCase(login.fulfilled, (state, action) => {
            state.status = "idle";
            state.user = action.payload.user;
            state.showLogin = false;
            state.loginModal = !action.payload.user.IsVerified;
            state.showVerifyEmail = !action.payload.user.IsVerified;
            state.loginErrors = null;
        })
        .addCase(login.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.status = "idle";
            state.loginErrors = action.payload?.error || "An unexpected error occurred.";
        })
        
        // Verify email action
        .addCase(verifyEmail.pending, (state) => {
            state.status = "pending";
            state.verifyEmailError = null;
        })
        .addCase(verifyEmail.fulfilled, (state) => {
            state.status = "idle";
            state.showVerifyEmail = false;
            state.verifiedBanner = true;
            state.verifyEmailError = null;
            if (state.user) {
                state.loginModal = false;
                state.user = {
                    ...state.user,
                    IsVerified: true,
                };
            } else {
                state.showLogin = true;
                state.showForgotPassword = false;
            }

        })
        .addCase(verifyEmail.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.status = "idle";
            state.verifyEmailError = action.payload?.error || "Verification failed";
        })

        // Resend code action
        .addCase(resendCode.pending, (state) => {
            state.resendCodeStatus = "pending";
            state.resendCodeError = null;
        })
        .addCase(resendCode.fulfilled, (state, action) => {
            state.resendCodeStatus = "idle";
            state.resendCodeError = null;
            state.showForgotPassword = true;
            state.showCode = true;
        })
        .addCase(resendCode.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.resendCodeStatus = "rejected";
            state.resendCodeError = action.payload?.error || "Failed to resend code";
        })

        // Get user action
        .addCase(getUser.pending, (state) => {
            state.status = "loading";
        })
        .addCase(getUser.fulfilled, (state, action) => {
            state.status = "idle";
            state.user = action.payload;
        })
        .addCase(getUser.rejected, (state, action) => {
            state.status = "idle";
            state.user = null;
        })

        // Signup action
        .addCase(signup.pending, (state) => {
            state.status = "pending";
            state.signupErrors = null;
        })
        .addCase(signup.fulfilled, (state) => {
            state.status = "idle";
            state.signupErrors = null;
        })
        .addCase(signup.rejected, (state, action: PayloadAction<SignupErrors |undefined>) => {
            state.status = "idle";
            state.signupErrors = action.payload || { general: "Signup failed" };
        })

        // Update user action
        .addCase(updateUser.pending, (state) => {
            state.status = "pending";
            state.updateError = null;
        })
        .addCase(updateUser.fulfilled, (state, action) => {
            state.status = "idle";
            state.user = {
                ...state.user,
                ...action.payload,
            };
            state.updateError = null;
        })
        .addCase(updateUser.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.status = "idle";
            state.updateError = action.payload?.error || "Update failed";
        })

        // Logout action
        .addCase(logout.pending, (state) => {
            state.status = "pending";
            state.logoutError = null;
        })
        .addCase(logout.fulfilled, (state) => {
            state.status = "idle";
            state.user = null;
            state.logoutError = null;
        })
        .addCase(logout.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.status = "idle";
            state.logoutError = action.payload?.error || "Logout failed";
        })

        // Reset password action
        .addCase(resetPassword.pending, (state) => {
            state.status = "pending";
            state.loginErrors = null;
        })
        .addCase(resetPassword.fulfilled, (state) => {
            state.status = "idle";
            state.showLogin = true;
            state.loginErrors = null;
        })
        .addCase(resetPassword.rejected, (state, action: PayloadAction<ErrorPayload | undefined>) => {
            state.status = "idle";
            state.resetPasswordError = action.payload?.error || "Password reset failed";
        });
    }
});

export const {
  setLoginModal,
  setHolesComparisonChart,
  setShowLogin,
  clearLoginErrors,
  clearSignupErrors,
  closeVerifyEmail,
  clearResendCodeError,
  clearVerifyEmailError,
  resetShowCode
} = userSlice.actions;

export default userSlice.reducer;