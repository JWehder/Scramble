import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../../../store";
import { setShowLogin, closeVerifyEmail, setLoginModal } from "../../state/userSlice";
import Modal from "../../../Utils/components/Modal";
import EnterCode from "./EnterCode";
import ForgotPassword from "./ForgotPassword";
import Login from "./Login";
import VerifyEmail from "./VerifyEmail";
import SignUp from "./SignUp";

export default function AuthModal() {
    const dispatch = useDispatch<AppDispatch>();

    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);

    // Redux selectors
    const open = useSelector((state: RootState) => state.users.loginModal);
    const showLogin = useSelector((state: RootState) => state.users.showLogin);
    const showVerifyEmail = useSelector((state: RootState) => state.users.showVerifyEmail);
    
    function onClose() {
        dispatch(setShowLogin(true));    // Reset login view on close
        dispatch(closeVerifyEmail());   // Reset verification state
        setShowForgotPassword(false);
        setShowCode(false);
        dispatch(setLoginModal(false));  // Close the modal
    };  

    return (
        <Modal open={open} onClose={onClose} bgColor={'bg-dark'}>
        <div className="w-full h-full flex items-center justify-center">
            <div className="w-[90%] max-w-[700px] min-h-[200px] sm:min-h-[300px] sm:w-[550px] md:w-[600px] lg:w-[650px] xl:w-[700px] p-4 bg-dark rounded-xl transition-all duration-300 ease-in-out">
            {showForgotPassword ? (
                showCode ? (
                <EnterCode />
                ) : (
                <ForgotPassword 
                    showCode={() => setShowCode(true)} 
                    showLogin={() => {
                    dispatch(setShowLogin(true));  // Use Redux to change showLogin state
                    setShowForgotPassword(false);
                    }}
                />
                )
            ) : showLogin ? (
                <Login
                showLogin={() => dispatch(setShowLogin(false))}  // Use Redux to toggle showLogin
                showForgotPassword={() => setShowForgotPassword(true)}
                />
            ) : showVerifyEmail ? (
                <VerifyEmail />
            ) : (
                <SignUp />
            )}
            </div>
        </div>
    </Modal>
    )
}