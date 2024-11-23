import SideBar from "../sidebar/Sidebar";
import { Outlet } from "react-router-dom";
import React from "react";

interface SignedInHomeProps {
    children: React.ReactNode; // This defines the `children` prop
}

export const SignedInHome: React.FC<SignedInHomeProps> = ({ children }) => {

    return ( 
        <div className="pt-20 pb-12 bg-dark h-screen w-screen overflow-auto">
            <SideBar />
            <Outlet />
        </div>
    )
}