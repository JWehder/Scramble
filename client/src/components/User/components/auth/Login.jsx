import { useState } from "react";
import google_login from "../../../../assets/google_login.svg";
import google_logo from "../../../../assets/web_light_rd_na.svg";

export default function Login({ showLogin }) {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const handleSubmit = (e) => {
      e.preventDefault();
      // Handle login logic here
      console.log('Login with', usernameOrEmail, password);
    };
  
    return (
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h1 className="text-2xl font-medium text-center mb-4">Login</h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-green-400 text-sm font-bold mb-2" htmlFor="usernameOrEmail">
                Username or Email
              </label>
                <input
                  className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
                  id="usernameOrEmail"
                  type="text"
                  placeholder="Username or email address"
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
                />

            </div>
            <div className="mb-6">
              <label className="block text-green-400 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="flex items-center justify-between">
              <button
                className="bg-gradient-to-r from-teal-500 to-green-700 hover:bg-gradient-to-l text-white font-bold py-2 px-4 rounded focus:outline-none shadow-md"
                type="submit"
              >
                Continue
              </button>
              <a href="#" className="inline-block align-baseline font-bold text-sm text-green-400 hover:text-green-800">
                Forgot Password?
              </a>
            </div>
          </form>
          <div className="mt-6 text-center flex justify-center items-center">
            <button
              className="flex justify-center items-center bg-white hover:bg-gray-100 border border-gray-300 text-gray-700 py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
            >
              <img src={google_logo} />
              <span className="mx-2">Login with your Google Account</span>
            </button>
          </div>
          <div className="mt-6 text-center">
            <p 
            onClick={showLogin}
            className="inline-block align-baseline font-bold text-sm text-green-400 hover:text-green-600 cursor-pointer"
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