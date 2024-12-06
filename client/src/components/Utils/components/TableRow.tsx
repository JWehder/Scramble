import React from 'react';
import TData from './TData';

type TableRowProps = {
    firstTwoDatapoints: string[] | React.ReactNode[];
    data: Record<string, any>;
    columns: Set<string>;
    onClick: () => void;
    brightness: string
};

const TableRow: React.FC<TableRowProps> = ({ firstTwoDatapoints, data, columns, onClick, brightness }) => (

    <div 
        onClick={onClick}
        className={`w-full flex bg-middle h-10 justify-center items-center hover:z-20 cursor-pointer hover:shadow-lg shadow-middle flex-row border-box ${brightness} text-sm md:text-sm lg:text-md sm:text-sm truncate hover:b-1 my-0.5 overflow-visible border-x-2 border-middle font-PTSans`}
    >
        {/* Left side: Start date and tournament name */}
        <div className="flex w-1/2 items-center">
            <div className=" flex w-1/6 px-2 text-left text-sm md:text-sm sm:text-sm">
                {firstTwoDatapoints[0]}
            </div>
            <div className="w-5/6 text-left flex items-center pl-6">
                <div className="flex justify-center text-md md:text-sm sm:text-sm p-2">
                    {firstTwoDatapoints[1]}
                </div>
            </div>
        </div>
        
        {/* Right side: Dynamic columns */}
        <div className="flex w-1/2 flex-row items-center">
            {Array.from(columns)?.map((col, idx) => (
                <TData key={idx}>
                    {data[col] ?? "--"}
                </TData>
            ))}
        </div>
    </div>
);

export default TableRow;
