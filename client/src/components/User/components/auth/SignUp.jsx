import { useState } from "react";
import { setShowLogin, signup } from "../../state/userSlice";
import google_logo from "../../../../assets/web_light_rd_na.svg"
import FacebookLoginButton from "./FacebookLoginButton";
import Button from "../../../Utils/components/Button";
import { useDispatch } from "react-redux";

export default function SignUp() {
  const dispatch = useDispatch();

  const showLogin = () => {
    dispatch(setShowLogin(true));
  }

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Handle signup logic here
    dispatch(signup({
      username,
      email,
      password
    }))
    dispatch(setShowLogin())
  };

  const handlePasswordToggle = (type) => {
    const inputField = document.getElementById(type);
    if (inputField) {
      inputField.type = inputField.type === "password" ? "text" : "password";
    }
  };

  return (
    <div className="px-8 pt-6 pb-8 mb-4 text-light w-full h-full rounded-xl font-bold">
      <h1 className="text-2xl font-medium text-center mb-4">Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm mb-2" htmlFor="username">
            Username
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            id="username"
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            id="email"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="mb-4 relative">
          <label className="block text-sm mb-2" htmlFor="password">
            Password
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 bg-light text-darkleading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full pr-10 text-dark"
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            className="absolute right-0 top-0 mt-2 mr-4 hover:text-green-600"
            onClick={() => handlePasswordToggle("password")}
          >
            <svg
              className="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M10 9.47a3.5 3.5 0 0 1 4.47-.34l-.745-6.15-5.196 4.59a3.5 3.5 0 0 1-1.38-4.222L4.75 2.985A3.5 3.5 0 0 1 9.235 7l.745 6.15z" />
              <path
                d="M15.706 5.293a3.5 3.5 0 0 1 0 4.944l-2.12 2.12-4.596-4.59a3.5 3.5 0 0 1-1.38-4.222L4.75 2.985A3.5 3.5 0 0 1 9.235 7l.745 6.15z"
              />
            </svg>
        </button>
        </div>
        <div className="mb-4 relative">
        <label className="block text-sm font-bold mb-2" htmlFor="confirmPassword">
            Confirm Password
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 bg-light leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full pr-10 text-dark"
            id="confirmPassword"
            type="password"
            placeholder="Confirm your password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <button
            className="absolute right-0 top-0 mt-2 mr-4 hover:text-green-600"
            onClick={() => handlePasswordToggle("confirmPassword")}
          >
            <svg
              className="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M10 9.47a3.5 3.5 0 0 1 4.47-.34l-.745-6.15-5.196 4.59a3.5 3.5 0 0 1-1.38-4.222L4.75 2.985A3.5 3.5 0 0 1 9.235 7l.745 6.15z" />
              <path
                d="M15.706 5.293a3.5 3.5 0 0 1 0 4.944l-2.12 2.12-4.596-4.59a3.5 3.5 0 0 1-1.38-4.222L4.75 2.985A3.5 3.5 0 0 1 9.235 7l.745 6.15z"
              />
            </svg>
          </button>
        </div>
        <div className="flex items-center justify-between">
          <Button 
          type="submit"
          variant="primary"
          size="md"
          >
            Continue
          </Button>
          <p 
          className="inline-block align-baseline font-bold text-sm cursor-pointer"
          onClick={showLogin}
          >
            Already have an account?{' '}
            <a>
              Sign In
            </a>
          </p>
        </div>
        <div className="mt-6 text-center flex justify-center items-center">
            <button
              className="flex justify-center items-center bg-light hover:brightness-110 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
            >
              <img src={google_logo} />
              <span className="mx-2">Sign up with Google</span>
            </button>
        </div>
        <div>
            <div className="mt-4 text-center flex justify-center items-center">
                <FacebookLoginButton buttonText="Sign up with Facebook" />
            </div>
        </div>
      </form>
    </div>
  );
}
