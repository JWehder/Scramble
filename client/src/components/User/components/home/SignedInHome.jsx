import SideBar from "../sidebar/Sidebar";
import { Outlet } from "react-router-dom";
import Modal from "../../../Utils/components/Modal";
import { setPlayerModal } from "../../state/userSlice"
import { useSelector, useDispatch } from 'react-redux';

export default function SignedInHome() {

    const dispatch = useDispatch();

    const open = useSelector((state) => state.users.playerModal)

    function onClose() {
        dispatch(setPlayerModal())
    }

    return ( 
        <div className="pt-20 pb-12 bg-dark h-screen w-screen overflow-hidden">
            <SideBar />
            <div className='w-full flex justify-center items-center flex-col min-w-[800px] min-h-[600px] flex-grow'>
                <Outlet />
            </div>
            <Modal open={open} onClose={onClose} title="" />
        </div>
    )
}