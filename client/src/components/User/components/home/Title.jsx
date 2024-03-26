import { motion } from "framer-motion";
import greenRounded from "../../../../assets/green_rounded.png";
import { useDispatch } from 'react-redux';
import { setLoginModal } from "../../state/userSlice";
import Button from "../../../Utils/components/Button";

export default function Title() {
    const dispatch = useDispatch();

    function handleClick() {
        dispatch(setLoginModal(true));
    }

    return (
        <div
            className="w-full flex items-center h-[550px] lg:h-screen md:h-screen sm:h-[550px]"
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
                className="flex flex-col pl-5 lg:pl-10 md:pl-10 sm:pl-5" // Adjust left padding for content alignment
            >
                <h1 className="text-3xl lg:text-6xl md:text-6xl sm:text-3xl font-bold text-light font-PTSans mb-3 lg:mb-6 md:mb-6 sm:mb-3 z-25">
                    Fantasy Golf
                </h1>
                <p className="text-light text-bold text-sm lg:text-md md:text-md sm:text-sm mb-3 lg:mb-6 md:mb-6 sm:mb-3 md:text-lg font-PTSans z-25">
                    Watch Golf Like Never Before!
                </p>
                <div className="w-1/2">
                    <Button
                    variant="secondary"
                    size="lg"
                    >
                        Get Started
                    </Button>
                </div>
            </motion.div>
        </div>
    );
}