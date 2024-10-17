import { motion } from 'framer-motion';

export default function MobileNavButtons({ handleLoginClick, handleSignUpClick, handleGetTheAppClick }) {

    const mobileButtonVars = {
        initial: {
            y: "30vh",
            transition: {
                duration: 0.5,
                ease: [0.37, 0, 0.63, 1],
                delay: 0.75
            }
        }, 
        open: {
            y: 0,
            transition: {
                duration: 0.7,
                ease: [0, 0.55, 0.45, 1],
                delay: 0.75
            }
        }
    }

    return (
        <>
            <div className='overflow-hidden'>
                <motion.div 
                variants={mobileButtonVars} 
                className="text-5xl py-2 space-y-2 cursor-pointer"
                >
                    <p
                    onClick={handleLoginClick}
                    className='text-center'
                    >
                        Login
                    </p>
                </motion.div>
            </div>
            <div className='overflow-hidden'>
                <motion.div
                variants={mobileButtonVars} 
                className="text-5xl py-2 space-y-2 cursor-pointer"
                >
                    <p
                    onClick={handleSignUpClick}
                    className='text-center'
                    >
                        Sign Up
                    </p>
                </motion.div>
            </div>
            <div className='overflow-hidden'>
                <motion.div
                variants={mobileButtonVars} 
                className="text-5xl py-2 space-y-2 cursor-pointer"
                >
                    <p
                    onClick={handleGetTheAppClick}
                    className='text-center'
                    >
                        Get the App
                    </p>
                </motion.div>
            </div>
        </>
    )
}