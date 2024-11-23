import React from "react";

export default function Bogey({ children, size = "6" } : { children: React.ReactNode, size: string }) {
    size = `w-${size} h-${size}`;

    return (
        <div className={`border-4 font-bold border-light font-lobster flex flex-col justify-center items-center text-sm text-light ${size} bg-transparent`}
        >
            {children}
        </div>
    )
}