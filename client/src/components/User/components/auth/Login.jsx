import { useState } from "react";
import google_logo from "../../../../assets/web_light_rd_na.svg";
import { useGoogleLogin } from '@react-oauth/google';
import { setShowLogin } from "../../state/userSlice";
import FacebookLoginButton from "./FacebookLoginButton";
import Button from "../../../Utils/components/Button";
import { useDispatch } from 'react-redux';
import { login } from "../../state/userSlice"
import NotificationBanner from "../../../Utils/components/NotificationBanner";

export default function Login({ showForgotPassword }) {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const dispatch = useDispatch();
    
    const showLogin = () => {
      dispatch(setShowLogin(false))
    }

    const handleLogin = () => {
        const userObj = {
          usernameOrEmail,
          password
        };
        dispatch(login(userObj));  // Dispatch the login action
    };

    const loginWithGoogle = useGoogleLogin({
        onSuccess: tokenResponse => console.log(tokenResponse),
    });
  
    return (
        <div className="px-8 pt-6 pb-8 mb-4 font-PTSans text-light w-full h-full">
          <h1 className="text-2xl font-medium text-center mb-4">Login</h1>
          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-md lg:text-md md:text-md sm:text-md font-bold mb-2" htmlFor="usernameOrEmail">
                Username or Email
              </label>
                <input
                  className="shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
                  id="usernameOrEmail"
                  type="text"
                  placeholder="Username or email address"
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
                />

            </div>
            <div className="mb-6">
              <label className="block text-md lg:text-md md:text-md sm:text-md font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                className="shadow appearance-none bg-light border w-full py-2 px-3 text-dark leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="flex items-center justify-between">
              <Button 
              variant="secondary" 
              type="submit"
              size="md"
              >
                Continue
              </Button>
              <a onClick={showForgotPassword} className="inline-block align-baseline font-bold text-sm hover:text-dark cursor-pointer">
                Forgot Password?
              </a>
            </div>
          </form>
          <NotificationBanner 
            message="This is a damn error!"
            variant="error"
          />
          <div>
            <div className="mt-6 text-center flex justify-center items-center w-full">
              <button
                className="flex justify-center items-center bg-light hover:brightness-110 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
                onClick={() => loginWithGoogle()}
              >
                <img src={google_logo} alt="google logo" />
                <span className="mx-2">Login with Google</span>
              </button>
          </div>
          <div>
            <div className="mt-4 text-center flex justify-center items-center">
                <FacebookLoginButton buttonText="Login with Facebook" />
            </div>
          </div>
          </div>
          <div className="mt-6 text-center">
            <p 
            onClick={showLogin}
            className="inline-block align-baseline font-bold text-sm hover:text-dark cursor-pointer"
            >
              Don't have an account?{' '}
              <a>
                Sign Up
              </a>
            </p>
          </div>
        </div>
    );
};