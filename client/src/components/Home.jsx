import Modal from "./User/components/auth/modal"
import { useSelector, useDispatch } from 'react-redux';
import { setLoginModal } from "./User/state/userSlice";
import Login from "./User/components/auth/Login";
import SignUp from "./User/components/auth/SignUp";
import { useState } from "react";
import ForgotPassword from "./User/components/auth/ForgotPassword";
import EnterCode from "./User/components/auth/EnterCode";
import Button from "./Utils/components/Button";
import { FaArrowRightLong } from "react-icons/fa6";
import HowToPlay from "./HowToPlay";
import greenRounded from "../assets/green_rounded.png";
import { motion } from "framer-motion";

export default function Home() {
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
        <div className="mt-20">
            <div className="flex-1 flex justify-center items-center min-vh-100 min-content">
                <motion.div
                variants={{
                    hidden: { opacity: 0, y: 75 },
                    visible: { opacity: 1, y: 0 }
                }}
                initial="hidden"
                animate="visible"
                transition={{ duration: 1.5, delay: 0.25 }}
                className="flex flex-col min-vh-100 min-content">
                    <h1 className="text-7xl font-bold text-light font-PTSans mb-6 z-25">Fantasy Golf</h1>
                    <p className="text-light text-xl mb-6 font-PTSans z-25">Watch Golf Like Never Before!</p>
                    <div className="w-1/2">
                        <Button className="z-25">
                        Get Started 
                        <div className="flex justify-center items-center">
                            <FaArrowRightLong className="animate-pulse ml-1" /> 
                        </div>
                        </Button>
                    </div>
                </motion.div>
                <div className="flex-1 flex justify-center">
                    <img
                    src={greenRounded}
                    alt="Homepage Image"
                    className="object-cover"
                    />
                </div>
            </div>

            <HowToPlay />

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

