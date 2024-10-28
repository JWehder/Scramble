import React from "react";

interface DashboardTitleProps {
    title: string;
    children?: React.ReactNode;
}

export default function DashboardTitle(
    { title, children }: DashboardTitleProps) {
    return (
        <div className='flex-row h-16 w-full mb-5 pl-14 flex text-light font-PTSans'>
            <div className="flex-1 flex items-center">   
                <h1 className='text-4xl'>{title}</h1>
            </div>
            
            <div className="flex-1 flex items-center justify-center">
                {children}
            </div>
        </div>
    )
}