import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "../../../../store";
import { resetPassword, resetAuth, setShowForgotPassword } from "../../state/userSlice";
import Modal from "../../../Utils/components/Modal";
import Login from "./Login";
import VerifyEmail from "./VerifyEmail";
import SignUp from "./SignUp";
import ChangePassword from "./ChangePassword";
import EnterCode from "./EnterCode";
import NotificationBanner from "../../../Utils/components/NotificationBanner";

interface PasswordChange {
    email: string
    newPassword: string
}

export default function AuthModal() {
    const dispatch = useDispatch<AppDispatch>();


    const [resetPasswordEmail, setResetPasswordEmail] = useState<string>('');

    // Redux selectors
    const open = useSelector((state: RootState) => state.users.loginModal);
    const showLogin = useSelector((state: RootState) => state.users.showLogin);
    const showVerifyEmail = useSelector((state: RootState) => state.users.showVerifyEmail);
    const showChangePassword = useSelector((state: RootState) => state.users.showChangePassword);
    const passwordResetSuccessBanner = useSelector((state: RootState) => state.users.resetPasswordSuccessBanner);
    const showForgotPassword = useSelector((state: RootState) => state.users.showForgotPassword);
    
    function onClose() {
        dispatch(resetAuth());
    };  

    const handlePasswordChange = ({ email, newPassword }: PasswordChange) => {
        dispatch(resetPassword({ email, newPassword }));
    };

    return (
        <Modal open={open} onClose={onClose} bgColor={'bg-dark'} closeButtonColor={'light'}>
            <div className="w-full h-full flex items-center justify-center">
                <div className="w-[90%] max-w-[700px] min-h-[200px] sm:min-h-[300px] sm:w-[550px] md:w-[600px] lg:w-[650px] xl:w-[700px] p-4 bg-dark rounded-xl transition-all duration-300 ease-in-out">
                { passwordResetSuccessBanner ?
                <NotificationBanner
                message="Password reset. Please sign in with your new credentials."
                variant="success"
                timeout={10000}
                onClose={null}
                />
                :
                null
                }
                { showForgotPassword ? (
                    showChangePassword ? (
                    <ChangePassword 
                    handlePasswordChange={handlePasswordChange}
                    email={resetPasswordEmail}
                    />
                    ) : (
                    <EnterCode 
                    setResetPasswordEmail={setResetPasswordEmail}
                    />
                    )
                ) : showLogin ? (
                    <Login
                    showForgotPassword={() => dispatch(setShowForgotPassword(true))}
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