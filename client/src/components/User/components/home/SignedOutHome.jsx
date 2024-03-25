import { useState } from "react";
import ForgotPassword from "../auth/ForgotPassword";
import EnterCode from "../auth/EnterCode";
import Modal from "../auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "../../state/userSlice";
import Login from "../auth/Login";
import SignUp from "../auth/SignUp";
import HowToPlay from "./HowToPlay";
import GamesCarousel from "./GamesCarousel";
import Title from "./Title";
import { redirect } from 'react-router-dom';

export default function SignedOutHome() {
    const dispatch = useDispatch();

    const [showLogin, setShowLogin] = useState(true);
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showCode, setShowCode] = useState(false);

    const open = useSelector((state) => state.users.loginModal);
    const signedIn = useSelector((state) => state.users.user);

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
        <div className="flex-grow shrink">
            <Title />
            <HowToPlay />
            <GamesCarousel />

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