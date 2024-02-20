import Modal from "./User/components/auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "./User/state/userSlice";
import Login from "./User/components/auth/Login";
import SignUp from "./User/components/auth/SignUp";
import { useState } from "react";
import ForgotPassword from "./User/components/auth/ForgotPassword";
import EnterCode from "./User/components/auth/EnterCode";

export default function Home({ setIsLoggedIn }) {
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
        <div className="text-center">
            <h1 className="text-3xl font-bold underline text-center mt-14">
                Scramble
            </h1>
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
            <p className="text-l font-bold underline text-center mt-14" onClick={() => setIsLoggedIn(false)}>Log Out</p>
            <div className="mx-56 p-10">
                <div className="grid mx-28 tb bg-gray-400 h-52 font-bold">
                    <p className="self-center text-center">Banner</p>
                </div>
                <div className="grid grid-cols-3 gap-10 p-10 h-72">
                    <div className="grid rounded bg-gray-400 font-bold">
                        <p className="self-center text-center">How It Works</p>
                    </div>
                    <div className="grid rounded bg-gray-400 font-bold">
                        <p className="self-center text-center">Rules of the Game</p>
                    </div>
                    <div className="grid rounded bg-gray-400 font-bold">
                        <p className="self-center text-center">FAQ</p>
                    </div>
                </div>
            </div>
        </div>
    )
}