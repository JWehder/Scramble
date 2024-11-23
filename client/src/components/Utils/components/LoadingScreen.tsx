import React from 'react';

interface LoadingScreenProps {
  message?: string;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ message = 'Loading...' }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-dark bg-opacity-50 z-50">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-middle border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-white text-lg font-semibold">{message}</p>
      </div>
    </div>
  );
};

export default LoadingScreen;
