import { useState } from "react";
import ForgotPassword from "../auth/ForgotPassword";
import EnterCode from "../auth/EnterCode";
import Modal from "../../../Utils/components/Modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal, setShowLogin } from "../../state/userSlice";
import Login from "../auth/Login";
import SignUp from "../auth/SignUp";
import HowToPlay from "./HowToPlay";
import GamesCarousel from "./GamesCarousel";
import Title from "./Title";
import { redirect } from 'react-router-dom';

export default function SignedOutHome() {
    const dispatch = useDispatch();

    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);

    const open = useSelector((state) => state.users.loginModal);
    const signedIn = useSelector((state) => state.users.user);
    const showLogin = useSelector((state) => state.users.showLogin)

    function onClose() {
        // set the forms to default
        setShowLogin(true);
        setShowForgotPassword(false);
        setShowCode(false);
        dispatch(setLoginModal(false));
    };

    if (signedIn) {
        redirect("/leagues");
    }

    return (
        <div className="flex-grow">
            <Title />
            <HowToPlay />
            <GamesCarousel />

            <Modal open={open} onClose={onClose}>
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