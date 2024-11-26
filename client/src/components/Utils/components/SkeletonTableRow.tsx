import React from "react";

const SkeletonTableRow: React.FC<{ columns: number }> = ({ columns }) => (
  <div className="w-full flex bg-dark animate-pulse h-10 justify-center items-center flex-row border-box text-sm my-1">
    {/* Left side: Placeholder for start date and tournament name */}
    <div className="flex w-1/2 items-center">
      <div className="w-1/6 text-center px-2 bg-middle rounded h-4"></div>
      <div className="w-5/6 text-left flex items-center pl-6">
        <div className="bg-middle rounded w-full h-4"></div>
      </div>
    </div>
    {/* Right side: Placeholder for dynamic columns */}
    <div className="flex w-1/2 flex-row items-center">
      {Array.from({ length: columns }).map((_, idx) => (
        <div
          key={idx}
          className="flex-grow h-4 bg-middle rounded mx-1"
        ></div>
      ))}
    </div>
  </div>
);

export default SkeletonTableRow;