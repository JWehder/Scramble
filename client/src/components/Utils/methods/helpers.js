function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

const post = async(url, obj, thunkAPI) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify(obj),
        }); 
        const data = await response.json()
        if (response.ok) {
            return data
        } else {
            return thunkAPI.rejectWithValue(data)
        }
    } catch(err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.")
    }
}

const show = async(url, thunkAPI) => {
    try {
        const response = await fetch(url)
        const data = await response.json()
        if (response.ok) {
            return data
        } else {
            return thunkAPI.rejectWithValue(data.error)
        }
    } catch(err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.")
    }
}

const patch = async(url, obj, thunkAPI) => {
    try {
        const response = await fetch(url, {
            method: "PATCH",
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify(obj),
        }); 
        const data = await response.json()
        if (response.ok) {
            return data
        } else {
            console.log(data.errors)
            return thunkAPI.rejectWithValue(data.errors)
        }
    } catch(err) {
        return thunkAPI.rejectWithValue("Error occurred. Please try again.")
    }
}

const get = url => {
    return fetch(`${url}`)
    .then((response) => response.json())
    .then((data) => (data))
}

export default function range(start, end, step = 1) {
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