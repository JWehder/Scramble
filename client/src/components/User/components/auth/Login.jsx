import { useState } from "react";
import google_logo from "../../../../assets/web_light_rd_na.svg";
import { useGoogleLogin } from '@react-oauth/google';
import FacebookLoginButton from "./FacebookLoginButton";
import Button from "../../../Utils/components/Button";
import { useDispatch, useSelector } from 'react-redux';
import { login, clearLoginErrors, setShowLogin } from "../../state/userSlice"
import NotificationBanner from "../../../Utils/components/NotificationBanner";

export default function Login({ showForgotPassword }) {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({}); // Initialize as an empty object
    const [showPassword, setShowPassword] = useState(false);

    const dispatch = useDispatch();

    const loginErrors = useSelector((state) => state.users.loginErrors);
    const verifiedBanner = useSelector((state) => state.users.verifiedBanner);
    
    const stopShowingLogin = () => {
      dispatch(setShowLogin(false))
    };

    const loginWithGoogle = useGoogleLogin({
        onSuccess: tokenResponse => console.log(tokenResponse),
    });

    if (loginErrors) {
      dispatch(clearLoginErrors());
    }
  
    const handleLogin = (e) => {
      e.preventDefault();
      const newErrors = {};
  
      if (!usernameOrEmail) {
        newErrors.usernameOrEmail = 'Username or email is required';
      }
      if (!password) {
        newErrors.password = 'Password is required';
      }
  
      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
      } else {
        setErrors({});
        const userObj = {
          usernameOrEmail,
          password,
        };
        dispatch(login(userObj));
        if (!loginErrors) {
          return null;
        }
      }
    };
  
    return (
      <div className="px-4 sm:px-8 md:px-12 lg:px-16 xl:px-24 py-6 font-PTSans text-light w-full h-full">
        <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-medium text-center mb-6">Login</h1>
        { loginErrors && typeof(loginErrors) !== Object &&
          <NotificationBanner
            message={loginErrors}
            variant="error"
            timeout={10000}
          />
        }
        { verifiedBanner ?
          <NotificationBanner
          message="Please sign in with your new credentials"
          variant={'success'}
          timeout={10000}
        />
        :
        ""
        }
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Username/Email Input */}
          <div className="mb-4 relative">
            <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="usernameOrEmail">
              Username or Email
            </label>
            <input
              className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full ${errors.usernameOrEmail ? 'border-red-500' : 'border'}`}
              id="usernameOrEmail"
              type="text"
              placeholder="Username or email address"
              value={usernameOrEmail}
              onChange={(e) => {
                setUsernameOrEmail(e.target.value)
                errors.usernameOrEmail = ""
              }}
            />
          </div>
          { errors.usernameOrEmail &&
            <p className="text-red-500 font-bold text-sm italic">
              {errors.usernameOrEmail}
            </p>
          }
  
          {/* Password Input */}
          <div className="mb-6 relative">
            <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              className={`shadow appearance-none bg-light border w-full py-2 px-3 text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full ${errors.password ? 'border-red-500' : 'border'}`}
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                errors.password = ""
              }}
            />
            <button
              className="absolute top-9 sm:top-9 md:top-9 lg:top-11 xl:top-11 right-3 text-dark hover:text-middle"
              onClick={() => setShowPassword(!showPassword)}
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
          </div>
          { errors.password &&
            <p className="text-red-500 font-bold text-sm mt-1">
              {errors.password}
            </p>
          }
          { loginErrors &&
            <p className="text-red-500 font-bold text-md mt-1">Username, password, or email is incorrect. Please try again.</p>
          }
  
          {/* Login Button */}
          <div className="flex items-center justify-between">
            <Button 
              variant="secondary" 
              type="submit"
              size="md"
              className="w-full md:w-auto"
            >
              Continue
            </Button>
            <a 
              onClick={showForgotPassword} 
              className="inline-block align-baseline font-bold text-sm sm:text-base cursor-pointer"
            >
              Forgot Password?
            </a>
          </div>
        </form>
  
        {/* Other login options (Google/Facebook) */}
        <div className="mt-6 text-center flex flex-col sm:flex-row justify-center items-center w-full space-y-4 sm:space-y-0 sm:space-x-4">
          <button
            className="flex justify-center items-center bg-light hover:brightness-110 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline sm:w-auto text-md sm:text-md md:w-auto font-PTSans"
            onClick={loginWithGoogle}
          >
            <img src={google_logo} alt="google logo" />
            <span className="mx-2">Login with Google</span>
          </button>
          <FacebookLoginButton buttonText="Login with Facebook" />
        </div>
  
        {/* Sign Up Link */}
        <div className="mt-6 text-center">
          <p 
            onClick={stopShowingLogin}
            className="inline-block align-baseline font-bold text-sm cursor-pointer"
          >
            Don't have an account?{' '}
            <a>Sign Up</a>
          </p>
        </div>
      </div>
    );
  }