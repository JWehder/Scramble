import React from "react";

const SkeletonTableHeaders: React.FC<{ columns: number }> = ({ columns }) => (
  <div className="w-full flex lg:text-md md:text-md sm:text-sm text-sm truncate font-bold p-1 items-center text-clip bg-middle animate-pulse border-b border-light">
    {/* Left side: Placeholder for headers */}
    <div className="text-center flex w-1/2">
      <div className="w-1/6 bg-light rounded h-2"></div>
      <div className="w-5/6 bg-light rounded h-2"></div>
    </div>
    <div className="flex w-1/2 flex-row">
      {Array.from({ length: columns }).map((_, idx) => (
        <div
          key={idx}
          className="flex flex-col w-6 flex-grow px-1 items-center justify-center p-1 bg-light rounded h-2"
        ></div>
      ))}
    </div>
  </div>
);

export default SkeletonTableHeaders;
