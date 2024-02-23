import Modal from "./User/components/auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "./User/state/userSlice";
import Login from "./User/components/auth/Login";
import SignUp from "./User/components/auth/SignUp";
import { useState } from "react";
import ForgotPassword from "./User/components/auth/ForgotPassword";
import EnterCode from "./User/components/auth/EnterCode";
import Scramble_Homepage from "../assets/green-image.png";
import Button from "./Utils/components/Button";

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
        <div className="bg-green-800">
            
            <div className="fixed top-0 w-full z-50 mb-1 bg-gray-50 shadow-lg">
                <div className="p-0.5 bg-gradient-to-r from-green-700 via-green-300 to-teal-300" />
                    <div className="flex justify-center p-2">
                    <div className="flex justify-between items-center w-full px-4">
                        {/* First div */}
                        <div className="flex-grow w-1/3" />

                        {/* Second div */}
                        <div className="flex justify-center items-center w-1/3">
                            <h1 className="text-4xl font-lobster text-center bg-gradient-to-r from-green-400 via-green-600 to-green-900 text-transparent bg-clip-text">
                                Scramble
                            </h1>
                        </div>

                        {/* Third div */}
                        <div className="flex space-x-4 w-1/3">
                            <Button
                            handleClick={handleSignUpClick}
                            >
                                Sign Up
                            </Button>
                            <Button
                            handleClick={handleLoginClick}
                            >
                                Login
                            </Button>
                            <Button
                            handleClick={handleGetTheAppClick}
                            >
                                Get the App
                            </Button>
                        </div>
                    </div>
                    </div>
                </div>

                <div className="relative flex items-center justify-center mt-20 ml-7">
                    <div className="flex items-center justify-center">
                        <img 
                            src={Scramble_Homepage} 
                            alt="Homepage Image" 
                            className="w-full h-[600px] object-cover rounded-lg"
                        />
                    </div>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <h1 className="text-4xl font-bold text-white">Fantasy Golf</h1>
                        <p className="text-white text-lg mt-2">
                            Watch Golf Like Never Before!
                        </p>
                        <Button className="mt-4">Get Started</Button>
                    </div>
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