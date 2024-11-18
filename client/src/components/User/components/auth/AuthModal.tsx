import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../../../store";
import { resetPassword, resetAuth, setShowChangePassword } from "../../state/userSlice";
import Modal from "../../../Utils/components/Modal";
import Login from "./Login";
import VerifyEmail from "./VerifyEmail";
import SignUp from "./SignUp";
import ChangePassword from "./ChangePassword";
import EnterCode from "./EnterCode";

export default function AuthModal() {
    const dispatch = useDispatch<AppDispatch>();

    const [showForgotPassword, setShowForgotPassword] = useState<boolean>(false);
    const [resetPasswordEmail, setResetPasswordEmail] = useState<string>('');

    // Redux selectors
    const open = useSelector((state: RootState) => state.users.loginModal);
    const showLogin = useSelector((state: RootState) => state.users.showLogin);
    const showVerifyEmail = useSelector((state: RootState) => state.users.showVerifyEmail);
    const showChangePassword = useSelector((state: RootState) => state.users.showChangePassword);
    
    function onClose() {
        dispatch(resetAuth());
        setShowForgotPassword(false);
    };  

    function changePassword(password: string) {
        dispatch(resetPassword(password));
    };

    return (
        <Modal open={open} onClose={onClose} bgColor={'bg-dark'} closeButtonColor={'light'}>
            <div className="w-full h-full flex items-center justify-center">
                <div className="w-[90%] max-w-[700px] min-h-[200px] sm:min-h-[300px] sm:w-[550px] md:w-[600px] lg:w-[650px] xl:w-[700px] p-4 bg-dark rounded-xl transition-all duration-300 ease-in-out">
                { showForgotPassword ? (
                    showChangePassword ? (
                    <ChangePassword 
                    handlePasswordChange={changePassword}
                    />
                    ) : (
                    <EnterCode 
                    setResetPasswordEmail={setResetPasswordEmail}
                    />
                    )
                ) : showLogin ? (
                    <Login
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