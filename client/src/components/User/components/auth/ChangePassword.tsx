import React, { useState } from 'react';
import Button from '../../../Utils/components/Button';
import { useSelector } from 'react-redux';
import { RootState } from '../../../../store';

interface PasswordChange {
  email: string;
  newPassword: string;
}

// Component definition with type annotations
export default function ChangePassword({
  handlePasswordChange,
  email,
}: {
  handlePasswordChange: (data: PasswordChange) => void; // Accepts an object of type PasswordChange
  email: string;
}) {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null); // Initialize as an empty object
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState<boolean>(false);

  const resetPasswordError = useSelector((state: RootState) => state.users.resetPasswordError)

  const handlePasswordToggle = () => {
    setShowPassword(!showPassword);
  };

  const handleConfirmPasswordToggle = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate passwords before submission
    if (newPassword !== confirmPassword) {
      setError("Passwords must match. Please check your spelling.")
      return;
    }

    // Handle password change logic here
    
    handlePasswordChange({ email, newPassword });
  };

  return (
    <div className="font-PTSans text-light rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
      <h1 className="text-2xl text-center mb-4 font-bold">Change Password</h1>
      <form onSubmit={handleSubmit}>
        {/* Password Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full pr-10 ${ error ? 'border-red-500' : 'border'}`}
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Enter your password"
            value={newPassword}
            onChange={(e) => {
              setNewPassword(e.target.value);
              setError(null);
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
          {resetPasswordError && (
            <p className="text-red-500 font-bold text-sm italic">{ resetPasswordError as React.ReactNode }</p>
          )}

        </div>

        {/* Confirm Password Input */}
        <div className="mb-4 relative">
          <label className="block text-sm sm:text-md lg:text-lg font-bold mb-2" htmlFor="confirmPassword">
            Confirm Password
          </label>
          <input
            className={`shadow appearance-none border w-full py-2 px-3 bg-light text-dark leading-tight focus:outline-none focus:shadow-outline rounded-full pr-10 ${error ? 'border-red-500' : 'border'}`}
            id="confirmPassword"
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Confirm your password"
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value);
              setError(null);
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
          {error && (
            <p className="text-red-500 font-bold text-sm italic">{error as React.ReactNode}</p>
          )}
        </div>
        <div className="flex items-center justify-between">
          <Button 
            variant="secondary" 
            type="submit"
            onClick={null}
            disabled={false}
            size='md'
          >
            Change Password
          </Button>
        </div>
      </form>
    </div>
  );
}