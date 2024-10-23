import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setLoginModal, setShowLogin } from '../../User/state/userSlice';
import { motion } from "framer-motion";
import HamburgerMenu from "./HamburgerMenu";
import MobileNavButtons from "./MobileNavButtons";
import HeaderButtons from './HeaderButtons';
import { useMediaQuery } from "@uidotdev/usehooks";
import Button from './Button';

export default function Header() {
    const dispatch = useDispatch();

    const [active, setActive] = useState(false);

    const isMobile = useMediaQuery("only screen and (max-width : 768px)");

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

    const menuVars = {
        initial: {
            scaleY: 0
        },
        animate: {
            scaleY: 1,
            transition: {
                duration: 0.5,
                ease: [0.12, 0, 0.39, 0]
            }
        },
        exit: {
            scaleY: 0,
            transition: {
                duration: 0.5,
                ease: [0.22, 1, 0.36, 1]
            }
        }
    };

    const containerVars = {
        initial: {
            transition: {
                delayChildren: 0.25,
                staggerChildren: 0.09
            }
        }, 
        open: {
            transition: {
                delayChildren: 0.25,
                staggerChildren: 0.09
            }
        }
    };

    return (
        <div className="fixed top-0 w-full z-35 mb-1 bg-dark shadow-lg">
        <div className="p-0.5 bg-custom-gradient" />
            <div className="flex justify-center p-2">
                <div className="flex justify-between items-center w-full px-4">
                    <div className="flex-grow w-1/3">
                        { isMobile ?
                        <HamburgerMenu 
                        color="light"
                        active={active} 
                        setActive={() => setActive((pv) => !pv)}
                        />
                        :
                        ""
                        }

                        { active &&
                        <motion.div 
                        variants={menuVars}
                        initial="initial"
                        animate="animate"
                        exit="exit"
                        className= 'fixed w-full h-screen left-0 top-0 p-10 text-light bg-dark origin-top'
                        >
                            <div className="flex h-full flex-col">
                                <div className="flex justify-between items-center">
                                    <HamburgerMenu 
                                        color="light"
                                        active={active} 
                                        setActive={() => setActive((pv) => !pv)}
                                    />
                                    <h1 className="text-2xl lg:text-5xl md:text-5xl sm:text-2xl font-lobster text-center bg-light text-transparent bg-clip-text">
                                        Scramble
                                    </h1>
                                </div>
                                <motion.div 
                                variants={containerVars}
                                initial="initial"
                                animate="open"
                                exit="initial"
                                className="flex flex-col h-full justify-center items-center font-lobster gap-4">
                                    <MobileNavButtons 
                                    handleGetTheAppClick={handleGetTheAppClick}
                                    handleLoginClick={handleLoginClick}
                                    handleSignUpClick={handleSignUpClick}
                                    />
                                </motion.div>
                            </div>  
                        </motion.div>
                        }
                    </div>

                    <div className="flex justify-center items-center w-1/3">
                        <h1 className="text-3xl lg:text-5xl md:text-5xl sm:text-3xl font-lobster text-center bg-custom-gradient text-transparent bg-clip-text">
                            Scramble
                        </h1>
                    </div>

                    {isMobile ?
                    <div className='flex justify-end items-center w-1/3'>
                        <Button
                        handleClick={handleGetTheAppClick}
                        size="sm"
                        variant="secondary"
                        >
                            Get the App
                        </Button>
                    </div>
                    :
                    <HeaderButtons 
                    handleGetTheAppClick={handleGetTheAppClick}
                    handleLoginClick={handleLoginClick}
                    handleSignUpClick={handleSignUpClick}
                    />    
                    }

                </div>
            </div>
        </div>
    )
}