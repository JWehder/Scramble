import React, { useState } from 'react';

export default function NotificationBanner({ message, variant }) {
  const [isVisible, setIsVisible] = useState(true);

  // Determine the background color based on the variant
  const getVariantStyle = () => {
    switch (variant) {
      case 'success':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      case 'warning':
        return 'bg-yellow-500';
      default:
        return 'bg-blue-500';
    }
  };

  if (!isVisible) return null;

  return (
    <div className={`${getVariantStyle()} text-white px-4 py-3 rounded fixed top-4 left-1/2 transform -translate-x-1/2 w-11/12 md:w-1/3 shadow-lg`}>
      <div className="flex items-center justify-between">
        <span className="text-sm">{message}</span>
        <button
          onClick={() => setIsVisible(false)}
          className="text-white hover:text-gray-200 focus:outline-none"
        >
          ✕
        </button>
      </div>
    </div>
  );
}