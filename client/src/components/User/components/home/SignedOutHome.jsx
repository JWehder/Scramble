import { useEffect, useState } from "react";
import ForgotPassword from "../auth/ForgotPassword";
import EnterCode from "../auth/EnterCode";
import Modal from "../../../Utils/components/Modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal, setShowLogin, closeVerifyEmail } from "../../state/userSlice";
import { useNavigate } from 'react-router-dom'; 
import Login from "../auth/Login";
import SignUp from "../auth/SignUp";
import HowToPlay from "./HowToPlay";
import GamesCarousel from "./GamesCarousel";
import Title from "./Title";
import VerifyEmail from "../auth/VerifyEmail";

export default function SignedOutHome() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
  
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);
  
    // Redux selectors
    const open = useSelector((state) => state.users.loginModal);
    const signedIn = useSelector((state) => state.users.user);
    const showLogin = useSelector((state) => state.users.showLogin);
    const showVerifyEmail = useSelector((state) => state.users.showVerifyEmail);
  
    function onClose() {
        dispatch(setShowLogin(true));    // Reset login view on close
        dispatch(closeVerifyEmail());   // Reset verification state
        setShowForgotPassword(false);
        setShowCode(false);
        dispatch(setLoginModal(false));  // Close the modal
    };

    useEffect(() => {
        console.log("should be moving to leagues")
        navigate("/leagues");
    }, [signedIn]);
  
    return (
      <div className="flex-grow">
        <Title />
        <HowToPlay />
        <GamesCarousel />
  
        <Modal open={open} onClose={onClose} bgColor={'bg-dark'}>
            <div className="w-full h-full flex items-center justify-center">
                <div className="w-[90%] max-w-[700px] min-h-[200px] sm:min-h-[300px] sm:w-[550px] md:w-[600px] lg:w-[650px] xl:w-[700px] p-4 bg-dark rounded-md transition-all duration-300 ease-in-out">
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
      </div>
    );
  }