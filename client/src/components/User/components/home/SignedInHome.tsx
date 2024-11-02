import SideBar from "../sidebar/Sidebar";
import { Outlet } from "react-router-dom";
import Modal from "../../../Utils/components/Modal";
import { setPlayerModal } from "../../state/userSlice"
import { useSelector, useDispatch } from 'react-redux';
import PlayerPage from "../../../Golfers/components/player/PlayerPage";
import { RootState } from "../../../../store"
import React from "react";

interface SignedInHomeProps {
    children: React.ReactNode; // This defines the `children` prop
}

export const SignedInHome: React.FC<SignedInHomeProps> = ({ children }) => {

    const dispatch = useDispatch();

    const open = useSelector((state: RootState ) => state.golfers.showGolferModal)

    function onClose() {
        dispatch(setPlayerModal())
    }

    return ( 
        <div className="pt-20 pb-12 bg-dark h-screen w-screen overflow-x-auto">
            <SideBar />
            <div className='w-full flex justify-center items-center flex-col min-w-[800px] min-h-[600px] flex-grow'>
                <Outlet />
            </div>
        </div>
    )
}