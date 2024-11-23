import React from "react"

export default function Birdie({ children } : { children: React.ReactNode }) {
    return (
        <div className="rounded-full border-4 font-bold border-light font-lobster flex flex-col justify-center items-center text-sm text-light h-6 w-6 bg-transparent">
            {children}
        </div>
    )
}