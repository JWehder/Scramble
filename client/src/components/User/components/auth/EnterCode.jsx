import React, { useState } from 'react';
import Button from '../../../Utils/components/Button';

export default function EnterCode({ handleClick, resendCode }) {
  const [code, setCode] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle code verification logic here
    console.log(code);
  };

  return (
    <div className="text-middle rounded px-8 pt-6 pb-8 mb-4 font-PTSans w-full h-full">
      <h1 className="text-2xl text-center mb-4">Verify Code</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-bold mb-2" htmlFor="code">
            Verification Code
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            id="code"
            type="text"
            placeholder="Enter the code sent to your email"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
        </div>
        <div className="flex items-center justify-between">
          <Button type="Submit">
            Verify Code
          </Button>
          <p onClick={resendCode} className="inline-block align-baseline font-bold text-sm text-green-400 hover:text-green-600 cursor-pointer">
            Didn't receive code? <a>Resend</a>
          </p>
        </div>
      </form>
    </div>
  );
}