import React from "react";

const SkeletonTableHeaders: React.FC<{ columns: number }> = ({ columns }) => (
  <div className="w-full flex lg:text-md md:text-md sm:text-sm text-sm truncate font-bold p-1 items-center text-clip bg-dark animate-pulse">
    {/* Left side: Placeholder for headers */}
    <div className="text-center flex w-1/2">
      <div className="w-1/6 bg-middle rounded h-4"></div>
      <div className="w-5/6 bg-middle rounded h-4"></div>
    </div>
    <div className="flex w-1/2 flex-row">
      {Array.from({ length: columns }).map((_, idx) => (
        <div
          key={idx}
          className="flex flex-col w-6 flex-grow px-1 items-center justify-center p-1 bg-middle rounded h-4"
        ></div>
      ))}
    </div>
  </div>
);

export default SkeletonTableHeaders;
