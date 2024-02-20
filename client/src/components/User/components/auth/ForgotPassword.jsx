import React, { useState } from 'react';

export default function ForgotPassword({ showLogin, showCode }) {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle email submission and code sending logic here
    console.log(email);
    showCode();
  };

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h1 className="text-2xl font-medium text-center mb-4">Reset Password</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-green-400 text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            id="email"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="flex items-center justify-between">
            <button
                className="bg-gradient-to-r from-teal-500 to-green-700 hover:bg-gradient-to-l text-white font-bold py-2 px-4 rounded-full focus:outline-none shadow-md"
                type="submit"
            >
                Send Code
            </button>
            <p 
            onClick={showLogin}
            className="inline-block align-baseline font-bold text-sm text-green-400 hover:text-green-600 cursor-pointer"
            >
              Remember Password?{' '}
              <a>
                Login
              </a>
            </p>
        </div>
      </form>
    </div>
  );
}