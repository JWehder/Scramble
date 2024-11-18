import { AsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Define a custom ThunkAPI interface
export interface ThunkAPI {
  rejectWithValue: <T>(value: T) => PayloadAction<T>;
  dispatch: any;
  getState: any;
  extra: any;
}


// Function to generate a random integer within a range
function getRandomNumber(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min) + min);
}

// Generic POST request function
async function post<T>(url: string, obj: object, thunkAPI: ThunkAPI): Promise<T | ReturnType<ThunkAPI['rejectWithValue']>> {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(obj),
        });
        const data = await response.json();
        if (response.ok) {
            return data as T;
        } else {
            return thunkAPI.rejectWithValue(data);
        }
    } catch (err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.");
    }
}

// Generic GET request with error handling using thunkAPI
async function show<T>(url: string, thunkAPI: ThunkAPI): Promise<T | ReturnType<ThunkAPI['rejectWithValue']>> {
    try {
        const response = await fetch(url);
        const data = await response.json();
        if (response.ok) {
            return data as T;
        } else {
            return thunkAPI.rejectWithValue(data.error);
        }
    } catch (err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.");
    }
}

// Generic PATCH request function
async function patch<T>(url: string, obj: object, thunkAPI: ThunkAPI): Promise<T | ReturnType<ThunkAPI['rejectWithValue']>> {
    try {
        const response = await fetch(url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(obj),
        });
        const data = await response.json();
        if (response.ok) {
            return data as T;
        } else {
            console.log(data.errors);
            return thunkAPI.rejectWithValue(data.errors);
        }
    } catch (err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.");
    }
}

// Simple GET request without error handling
function get<T>(url: string): Promise<T> {
    return fetch(url)
        .then((response) => response.json())
        .then((data) => data as T);
}

// Range generator function
export default function range(start: number, end: number, step = 1): number[] {
    const length = Math.floor((end - start) / step) + 1;
    return Array.from({ length }, (_, index) => start + index * step);
}

// const displayErrors = (errors, errorKey = null) => {

//     return errors.map((error) => {
//         if (errorKey === "password" && error === "is invalid") {
//             error = "Sorry, your password is invalid. Your password must be at least 8 characters, contain at least one digit, at least one lowercase letter, one uppercase letter, and one special character (! @ # $ % ^ &)"
//         } else if (errorKey === "email" && error === "is invalid") {
//             error = "Please follow typical email formatting: joe@email.com"
//         } else if (errorKey === "password" && (error === "can't be blank" || error === "is too short (minimum is 8 characters)")) {
//             return null
//         }
//         return <ErrorMessage error={error} />
//     })
// }

const fetchWrapper = {
    post: post,
    get: get,
    patch: patch,
    show: show
}

export { fetchWrapper }