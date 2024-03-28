import { motion } from "framer-motion";

export default function HamburgerMenu({ setActive, active, color }) {

    color = `bg-${color}`;

    return (
        <>
            <motion.button
            initial={false}
            onClick={() => setActive((pv) => !pv)}
            animate={active ? "open" : "closed"}
            className="relative w-12 h-12 p-1 rounded-full bg-light/0 transition-colors hover:bg-light/20"
            >
                <motion.span 
                style={{
                    top: "35%",
                    left: "50%",
                    x: "-50%",
                    y: "-50%"
                }}
                className={`absolute w-6 h-1 ${color}`}
                variants={{
                    open: {
                        rotate: ["0deg", "0deg", "45deg"],
                        top: ["35%", "50%", "50%"]
                    },
                    closed: {
                        rotate: ["45deg", "0deg", "0deg"],
                        top: ["50%", "50%", "35%"]
                    }
                }}
                />
                <motion.span 
                style={{
                    top: "50%",
                    left: "50%",
                    x: "-50%",
                    y: "-50%"
                }}
                className={`absolute w-6 h-1 ${color}`}
                variants={{
                    open: {
                        rotate: ["0deg", "0deg", "-45deg"]
                    },
                    closed: {
                        rotate: ["-45deg", "0deg", "0deg"]
                    }
                }}
                />
                <motion.span 
                style={{
                    bottom: "35%",
                    left: "calc(50% + 6px)",
                    x: "-50%",
                    y: "50%"
                }}
                className={`absolute w-3 h-1 ${color}`}
                variants={{
                    open: {
                        rotate: ["0deg", "0deg", "45deg"],
                        left: '50%',
                        bottom: ["35%", "50%", "50%"]
                    },
                    closed: {
                        rotate: ["45deg", "0deg", "0deg"],
                        left: "calc(50% + 6px)",
                        bottom: ["50%", "50%", "35%"]              
                    }
                }}
                />
            </motion.button>

        </>
    )
}