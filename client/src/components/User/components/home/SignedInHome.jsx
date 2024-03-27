import SideBar from "../sidebar/Sidebar";
import { Outlet } from "react-router-dom";
import Modal from "../auth/modal";

export default function SignedInHome() {

    return ( 
        <div className="w-full h-full pt-20 pb-12 min-h-min">
            <SideBar />
            <div className='w-full flex justify-center items-center flex-col h-full min-w-[800px]'>
                <Outlet />
            </div>

        </div>
    )
}