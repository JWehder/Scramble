import React, { useEffect } from "react";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";

interface DashboardTitleProps {
    title: string;
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
    { title, children }: DashboardTitleProps) {

    const { data, error, isLoading } = useQuery({
        queryKey: ['golfersGreeting'], 
        queryFn: fetchGreeting
    });

    useEffect(() => {
        // This effect can be used for additional logic if needed
        if (data) {
            console.log('Fetched greeting:', data.message);
        }
    }, []);

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