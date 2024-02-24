import Modal from "./User/components/auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "./User/state/userSlice";
import Login from "./User/components/auth/Login";
import SignUp from "./User/components/auth/SignUp";
import { useState } from "react";
import ForgotPassword from "./User/components/auth/ForgotPassword";
import EnterCode from "./User/components/auth/EnterCode";
import Button from "./Utils/components/Button";
import greenrounded from "../assets/green_rounded.png";
import { FaArrowRightLong } from "react-icons/fa6";

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

    function handleSignUpClick() {
        dispatch(setLoginModal(true));
        setShowLogin(false);
    }

    function handleLoginClick() {
        dispatch(setLoginModal(true));
        setShowLogin(true);
    }

    function handleGetTheAppClick() {

    }

    return (
        <div className="bg-dark mt-2">

                <div className="flex">
                    <div className="flex-1 flex justify-end items-center">
                        <div className="flex flex-col items-center justify-center">
                            <h1 className="text-6xl font-bold text-light text-PTSans mb-6">Fantasy Golf</h1>
                            <p className="text-light text-lg mb-6 ">Watch Golf Like Never Before!</p>
                            <Button>
                                Get Started <FaArrowRightLong className="animate-pulse ml-1"/> 
                            </Button>
                        </div>
                    </div>
                    <div className="flex-1 flex justify-center">
                        <img src={greenrounded} alt="Homepage Image" />
                    </div>
                </div>

                <div>

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