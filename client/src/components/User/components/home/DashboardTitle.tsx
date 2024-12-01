import React, { useEffect } from "react";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import Avatar from "../../../Utils/components/Avatar";

interface DashboardTitleProps {
    title: string | undefined;
    avatar: string | undefined;
    children?: React.ReactNode;
}

interface GolfersGreeting {
    message: string; // Adjust this according to the actual response structure
}

const fetchGreeting = async (): Promise<GolfersGreeting> => {
    const response = await axios.get<GolfersGreeting>(`/api/golfers/hi`);
    return response.data;
};

export default function DashboardTitle(
    { title, avatar, children }: DashboardTitleProps) {

    return (
        <div className='flex-row h-16 w-full mb-5 pl-14 flex text-light font-PTSans'>
            <div className="flex-1 flex items-center">   
                { avatar ? 
                    <Avatar imgUrl={avatar} size="12" />
                    :
                    null
                }
                <h1 className='text-4xl'>{title}</h1>              
            </div>
            
            <div className="flex-1 flex items-center justify-center">
                {children}
            </div>
        </div>
    )
}