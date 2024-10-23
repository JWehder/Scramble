import React, { useState, useEffect } from 'react';

export default function NotificationBanner({ message, variant, timeout, onClose }) {
    const [isVisible, setIsVisible] = useState(true);
  
    useEffect(() => {
      // Only set a timer if a timeout is provided
      if (timeout) {
        const timer = setTimeout(() => {
          setIsVisible(false);  // Hide the banner after timeout
          if (onClose) onClose();  // Call onClose callback if provided
        }, timeout);
  
        return () => clearTimeout(timer);  // Cleanup timeout on component unmount
      }
    }, [timeout, onClose]);

    // Determine the background color based on the variant
    const getVariantStyle = () => {
      switch (variant) {
        case 'success':
          return 'bg-green-300';  
        case 'error':
          return 'bg-red-300'; 
        case 'warning':
          return 'bg-yellow-300'; 
        default:
          return 'bg-blue-300'; 
      }
    };

  if (!isVisible) return null;

  return (
    <div className={`${getVariantStyle()} text-white px-2 py-2 rounded fixed left-1/2 top-2 transform -translate-x-1/2 w-11/12 md:w-1/3 shadow-lg`}>
      <div className="flex items-center justify-between">
        <span className="text-sm px-0.5">{message}</span>
        <button
          onClick={() => {
            setIsVisible(false);
            if (onClose) {
              onClose();
            }
          }}
          className="text-white hover:text-gray-200 focus:outline-none"
        >
          ✕
        </button>
      </div>
    </div>
  );
}