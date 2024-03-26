import { useDispatch } from 'react-redux';
import { setLoginModal } from '../../User/state/userSlice';
import Button from './Button';
import { useSelector } from 'react-redux';
import { motion } from "framer-motion";

export default function Header({ setShowLogin }) {
    const dispatch = useDispatch();

    function handleSignUpClick() {
        dispatch(setLoginModal(true));
        dispatch(setShowLogin(false));
    };

    function handleLoginClick() {
        dispatch(setLoginModal(true));
        dispatch(setShowLogin(true));
    };

    function handleGetTheAppClick() {
        return null;
    };

    const isSignedIn = useSelector((state) => state.users.user)

    return (
        <div className="fixed top-0 w-full z-35 mb-1 bg-dark shadow-lg">
        <div className="p-0.5 bg-custom-gradient" />
            <div className="flex justify-center p-2">
                <div className="flex justify-between items-center w-full px-4">
                    <div className="flex-grow w-1/3" />

                    <div className="flex justify-center items-center w-1/3">
                        <h1 className="text-3xl lg:text-5xl md:text-5xl sm:text-3xl font-lobster text-center bg-custom-gradient text-transparent bg-clip-text">
                            Scramble
                        </h1>
                    </div>

                    <div className="flex space-x-4 w-1/3">
                        { isSignedIn ? 
                            ""
                            :
                            <>
                                <Button
                                variant="primary"
                                size="md"
                                onClick={handleSignUpClick}
                                >
                                    Sign Up
                                </Button>
                                <Button
                                variant="primary"
                                size="md"
                                onClick={handleLoginClick}
                                >
                                    Login
                                </Button>
                            </>
                        }
                        <Button
                        variant="secondary"
                        size="md"
                        onClick={handleGetTheAppClick}
                        >
                            Get the App
                        </Button>
                    </div>
                    <motion.div
                    variants={{
                        hidden: { display: none, cursor: pointer }
                    }}
                    initial="hidden"
                    animate="visible"
                    >
                        <span className="block w-6 h-1 my-1.5 mx-auto"></span>
                        <span></span>
                        <span></span>
                    </motion.div>
                </div>
            </div>
        </div>
    )
}