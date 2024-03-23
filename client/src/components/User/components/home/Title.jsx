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
                <h1 className="text-4xl md:text-7xl font-bold text-light font-PTSans mb-6 z-25 ml-4">Fantasy Golf</h1>
                <p className="text-light text-md mb-6 md:text-lg font-PTSans z-25 ml-4">Watch Golf Like Never Before!</p>
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