import { useState } from "react";
import ForgotPassword from "../auth/ForgotPassword";
import EnterCode from "../auth/EnterCode";
import Modal from "../../../Utils/components/Modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal, setShowLogin, closewVerifyEmail } from "../../state/userSlice";
import Login from "../auth/Login";
import SignUp from "../auth/SignUp";
import HowToPlay from "./HowToPlay";
import GamesCarousel from "./GamesCarousel";
import Title from "./Title";
import { redirect } from 'react-router-dom';
import VerifyEmail from "../auth/VerifyEmail";

export default function SignedOutHome() {
    const dispatch = useDispatch();
  
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);
  
    // Redux selectors
    const open = useSelector((state) => state.users.loginModal);
    const signedIn = useSelector((state) => state.users.user);
    const showLogin = useSelector((state) => state.users.showLogin);
    const showVerifyEmail = useSelector((state) => state.users.showVerifyEmail);
  
    function onClose() {
      // Reset forms to default and close modal
      dispatch(setShowLogin(true));  // Reset login view on close
      closewVerifyEmail();  // Reset verification on close
      setShowForgotPassword(false);
      setShowCode(false);
      dispatch(setLoginModal(false));  // Close the modal
    }
  
    // Redirect if signed in
    if (signedIn) {
      redirect("/leagues");
    }
  
    return (
      <div className="flex-grow">
        <Title />
        <HowToPlay />
        <GamesCarousel />
  
        <Modal open={open} onClose={onClose} bgColor={'bg-dark'}>
          <div className="w-[550px] min-w-[450px] max-w-[700px] min-h-[400px] max-h-[650px] flex items-center justify-center flex-grow flex-shrink">
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
        </Modal>
      </div>
    );
  }