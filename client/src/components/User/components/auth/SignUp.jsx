import { useState } from "react";
import { setShowLogin, signup } from "../../state/userSlice";
import google_logo from "../../../../assets/web_light_rd_na.svg";
import FacebookLoginButton from "./FacebookLoginButton";
import Button from "../../../Utils/components/Button";
import { useDispatch, useSelector } from "react-redux";
import NotificationBanner from "../../../Utils/components/NotificationBanner";

export default function SignUp() {
  const dispatch = useDispatch();

  const showLogin = () => {
    dispatch(setShowLogin(true));
  };

  const signupErrors = useSelector((state) => state.users.signupErrors);

  // State to track form inputs
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // State to track errors
  const [errors, setErrors] = useState({});
  
  // Password visibility toggles
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handlePasswordToggle = () => {
    setShowPassword(!showPassword);
  };

  const handleConfirmPasswordToggle = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newErrors = {};
    if (!username) newErrors.username = 'Username is required';
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    if (password !== confirmPassword) newErrors.confirmPassword = 'Passwords do not match';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      setErrors({});
      // Dispatch signup action
      dispatch(signup({ username, email, password }));
    }
  };

  return (
    <div className="px-4 sm:px-8 md:px-12 lg:px-16 xl:px-24 py-6 font-PTSans text-light">
      <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-medium text-center mb-6">Sign Up</h1>
      { signupErrors && typeof(signupErrors) !== Object &&
        <NotificationBanner
          message={signupErrors}
          variant="error"
          timeout={10000}
        />
      }
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Username Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="username">
            Username
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full ${errors.username || signupErrors?.Username ? 'border-red-500' : 'border'}`}
            id="username"
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setErrors({ ...errors, username: '' });
            }}
          />
          {errors.username && (
            <p className="text-red-500 font-bold text-sm italic">{errors.username}</p>
          )}
          {signupErrors?.Username && (
            <p className="text-red-500 font-bold text-sm italic">{signupErrors.Username}</p>
          )}
        </div>

        {/* Email Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full ${errors.email || signupErrors?.Email ? 'border-red-500' : 'border'}`}
            id="email"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setErrors({ ...errors, email: '' });
            }}
          />
          {errors.email && (
            <p className="text-red-500 font-bold text-sm italic">{errors.email}</p>
          )}
          { signupErrors?.Email && (
            <p className="text-red-500 font-bold text-sm italic">{signupErrors.Email }</p>
          )}
        </div>

        {/* Password Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full pr-10 ${errors.password || signupErrors?.Password ? 'border-red-500' : 'border'}`}
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setErrors({ ...errors, password: '' });
            }}
          />
          <button
            className="absolute top-9 sm:top-9 md:top-9 lg:top-11 xl:top-11  right-3 text-dark hover:text-middle"
            onClick={() => handlePasswordToggle()}
            type="button" // prevents form submission
          >
            {showPassword ? (
              // "Hide password" icon (eye with slash)
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="eye-icon"
                width="24"
                height="24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7 1.015-3.233 3.497-5.873 6.646-6.725m3.073-.151A9.958 9.958 0 0112 5c4.478 0 8.268 2.943 9.542 7-.267.852-.665 1.656-1.167 2.392m-2.326 2.326A9.956 9.956 0 0112 19a9.958 9.958 0 01-6.646-2.725"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 3l18 18"
                />
              </svg>
            ) : (
              // "Show password" icon (normal eye)
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="eye-icon"
                width="24"
                height="24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M2.458 12C3.732 7.943 7.522 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.478 0-8.268-2.943-9.542-7z"
                />
              </svg>
            )}
          </button>
          {errors.password && (
            <p className="text-red-500 font-bold text-sm italic">{ errors.password }</p>
          )}
          { signupErrors?.Password && (
            <p className="text-red-500 font-bold text-sm italic">{signupErrors.Password }</p>
          )}
        </div>

        {/* Confirm Password Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="confirmPassword">
            Confirm Password
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full pr-10 ${errors.confirmPassword ? 'border-red-500' : 'border'}`}
            id="confirmPassword"
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Confirm your password"
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value);
              setErrors({ ...errors, confirmPassword: '' });
            }}
          />
          <button
            className="absolute top-9 sm:top-9 md:top-9 lg:top-11 xl:top-11  right-3 text-dark hover:text-middle"
            onClick={() => handleConfirmPasswordToggle()}
            type="button" // prevents form submission
          >
            {showConfirmPassword ? (
              // "Hide password" icon (eye with slash)
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="eye-icon"
                width="24"
                height="24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7 1.015-3.233 3.497-5.873 6.646-6.725m3.073-.151A9.958 9.958 0 0112 5c4.478 0 8.268 2.943 9.542 7-.267.852-.665 1.656-1.167 2.392m-2.326 2.326A9.956 9.956 0 0112 19a9.958 9.958 0 01-6.646-2.725"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 3l18 18"
                />
              </svg>
            ) : (
              // "Show password" icon (normal eye)
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="eye-icon"
                width="24"
                height="24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M2.458 12C3.732 7.943 7.522 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.478 0-8.268-2.943-9.542-7z"
                />
              </svg>
            )}
          </button>
          {errors.confirmPassword && (
            <p className="text-red-500 font-bold text-sm italic">{errors.confirmPassword}</p>
          )}
        </div>

        {/* Sign Up Button */}
        <div className="flex items-center justify-between">
          <Button variant="secondary" type="submit" size="md" className="w-full md:w-auto">
            Sign Up
          </Button>
        </div>
      </form>

      {/* Other sign-up options */}
      <div className="mt-6 text-center flex flex-col sm:flex-row justify-center items-center w-full space-y-4 sm:space-y-0 sm:space-x-4">
        <button
          className="flex justify-center items-center bg-light hover:brightness-110 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline w-full sm:w-auto"
          onClick={() => console.log("Google signup not implemented")}
        >
          <img src={google_logo} alt="google logo" />
          <span className="mx-2">Sign up with Google</span>
        </button>
        <FacebookLoginButton buttonText="Sign up with Facebook" />
      </div>

      {/* Login Link */}
      <div className="mt-6 text-center">
        <p
          onClick={showLogin}
          className="inline-block align-baseline font-bold text-sm cursor-pointer"
        >
          Already have an account? <a>Login</a>
        </p>
      </div>
    </div>
  );
}
