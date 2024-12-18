import React from 'react';

interface LoadingWidgetProps {
  message?: string;
}

const LoadingWidget: React.FC<LoadingWidgetProps> = ({ message = 'Loading...' }) => {
  return (
      <div className="text-center">
        <div className="w-4 h-4 border-4 border-middle border-t-transparent rounded-full animate-spin ml-1"></div>
        <p className="text-light text-lg font-semibold">{message}</p>
      </div>
  );
};

export default LoadingWidget;