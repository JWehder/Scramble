import SideBar from "../sidebar/Sidebar";
import { Outlet } from "react-router-dom";
import { useState } from "react";
import ForgotPassword from "../auth/ForgotPassword";
import EnterCode from "../auth/EnterCode";
import Modal from "../auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "../../state/userSlice";
import Login from "../auth/Login";
import SignUp from "../auth/SignUp";

export default function SignedInHome() {

    const dispatch = useDispatch();

    const [showLogin, setShowLogin] = useState(true);
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);

    const open = useSelector((state) => state.users.loginModal);

    function onClose() {
        // set the forms to default
        setShowLogin(true);
        setShowForgotPassword(false);
        setShowCode(false);
        dispatch(setLoginModal(false));
    };

    return ( 
        <div className="w-full h-full pt-20 pb-12 min-h-min">
            <SideBar />
            <div className='w-full flex justify-center items-center flex-col h-full'>
                <Outlet />
            </div>
            <Modal open={open} onClose={onClose} title={"Login or Sign up"}>
                { showForgotPassword ?
                showCode ?
                <EnterCode />
                :
                <ForgotPassword 
                showCode={() => setShowCode(true)} 
                showLogin={() => {
                    setShowLogin(true);
                    setShowForgotPassword(false);
                }}
                />
                :
                showLogin ? 
                    <Login 
                    showLogin={() => setShowLogin(!showLogin)} 
                    showForgotPassword={() => setShowForgotPassword(!showForgotPassword)}
                    />
                    :
                    <SignUp showLogin={() => setShowLogin(!showLogin)} />
                }
            </ Modal>
        </div>
    )
}