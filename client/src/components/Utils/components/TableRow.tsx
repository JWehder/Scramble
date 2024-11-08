import React from 'react';

type TableRowProps = {
    firstTwoDatapoints: string[];
    data: Record<string, any>;
    columns: Set<string>;
    onClick: () => void;
    brightness: string
};

const TableRow: React.FC<TableRowProps> = ({ firstTwoDatapoints, data, columns, onClick, brightness }) => (

    <div 
        onClick={onClick}
        className={`w-full flex bg-middle h-10 justify-center items-center hover:z-20 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} text-sm md:text-sm lg:text-md sm:text-sm truncate hover:b-1 my-1 overflow-visible border-x-2 border-middle`}
    >
        {/* Left side: Start date and tournament name */}
        <div className="flex w-3/6 items-center">
            <div className="w-1/6 text-left px-2 overflow-hidden text-ellipsis whitespace-nowrap">
                {firstTwoDatapoints[0]}
            </div>
            <div className="w-5/6 text-left flex items-center pl-6">
                <div className="flex justify-center overflow-hidden text-ellipsis whitespace-nowrap">
                    {firstTwoDatapoints[1]}
                </div>
            </div>
        </div>
        
        {/* Right side: Dynamic columns */}
        <div className="flex w-3/6 flex-row items-center">
            {Array.from(columns)?.map((col, idx) => (
                <div key={idx} className="flex-grow text-center">
                    {data[col] ?? "--"}
                </div>
            ))}
        </div>
    </div>
);

export default TableRow;
