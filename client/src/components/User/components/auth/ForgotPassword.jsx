import React, { useState } from 'react';
import Button from '../../../Utils/components/Button';

export default function ForgotPassword({ showLogin, showCode }) {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle email submission and code sending logic here
    console.log(email);
    showCode();
  };

  return (
    <div className="text-light font-PTSans rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
    <h1 className="text-2xl text-center mb-4">Reset Password</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline text-dark bg-light focus:ring-green-500 focus:border-green-500 rounded-full"
            id="email"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="flex items-center justify-between">
            <Button variant="secondary" type="submit">
              Send Code
            </Button>
            <p 
            onClick={showLogin}
            className="inline-block align-baseline font-bold text-sm text-light hover:text-middle cursor-pointer"
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