import { motion } from "framer-motion";
import Button from "./Utils/components/Button";
import { FaArrowRightLong } from "react-icons/fa6";
import greenRounded from "../assets/green_rounded.png";
import { useDispatch } from 'react-redux';
import { setLoginModal } from "./User/state/userSlice";

export default function Title() {
    const dispatch = useDispatch();

    function handleClick() {
        dispatch(setLoginModal(true));
    }

    return (
        <div
            className="w-full flex items-center min-h-screen"
            style={{
                backgroundImage: `url(${greenRounded})`,
                backgroundSize: 'contain',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <motion.div
                variants={{
                    hidden: { opacity: 0, y: 75 },
                    visible: { opacity: 1, y: 0 }
                }}
                initial="hidden"
                animate="visible"
                transition={{ duration: 1.5, delay: 0.25 }}
                className="flex flex-col pl-12" // Adjust left padding for content alignment
            >
                <h1 className="text-4xl md:text-7xl font-bold text-light font-PTSans mb-6 z-25">Fantasy Golf</h1>
                <p className="text-light text-md mb-6 md:text-lg font-PTSans z-25">Watch Golf Like Never Before!</p>
                <div className="w-1/2">
                    <Button 
                    className="z-25"
                    handleClick={handleClick}
                    >
                        <div className="flex justify-center items-center animate-pulse">
                            Get Started
                            <FaArrowRightLong className="ml-1" /> 
                        </div>
                    </Button>
                </div>
            </motion.div>
        </div>
    );
}