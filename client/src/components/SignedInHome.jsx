import SideBar from "./User/components/sidebar/Sidebar";
import { Outlet } from "react-router-dom";

export default function SignedInHome() {

    return ( 
        <div className="w-full h-full pt-20 pb-16">
            <SideBar />
            <div className='w-full flex justify-center items-center flex-col'>
                <Outlet />
            </div>
        </div>
    )
}