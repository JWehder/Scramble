import React, { useState } from 'react';
import Button from '../../../Utils/components/Button';

export default function ChangePassword({ handlePasswordChange }) {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate passwords before submission
    if (newPassword !== confirmPassword) {
      alert('Passwords do not match. Please try again.');
      return;
    }

    // Handle password change logic here
    console.log('New password:', newPassword);
    // handlePasswordChange(newPassword);
  };

  return (
    <div className="font-PTSans text-middle rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
      <h1 className="text-2xl text-center mb-4">Change Password</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-bold mb-2" htmlFor="newPassword">
            New Password
          </label>
          <input
            type="password"
            id="newPassword"
            className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="Enter your new password"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-green-400 text-sm font-bold mb-2" htmlFor="confirmPassword">
            Confirm New Password
          </label>
          <input
            type="password"
            id="confirmPassword"
            className="shadow appearance-none border w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-green-500 focus:border-green-500 rounded-full"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Re-enter your new password"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <Button type="Submit">
            Change Password
          </Button>
        </div>
      </form>
    </div>
  );
}