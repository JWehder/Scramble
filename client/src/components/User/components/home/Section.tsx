import React from "react";
import { motion } from "framer-motion";

export default function Section({ desc, img, title }
    :
    {
        desc: string,
        img: string,
        title: string
    }) {

    return (
        <motion.div 
        className="flex items-center justify-content"
        initial={{ opacity: 0 }}
        transition={{ duration: 1.5, delay: 0.25 }}
        whileInView={{ opacity: 1 }}
        >
            <div className="w-3/4">
                <h2 className="text-left font-lobster mb-2 text-xl lg:text-3xl md:text-3xl sm:text-xl">
                    {title}
                </h2>
                <p className="text-left text-sm lg:text-lg md:text-lg sm:text-sm">
                    <span>Placeholder content for {desc} section.</span>
                </p>
            </div>
            <div className="w-1/4">
                <img
                src={img}
                alt={`${title} Fantasy Golf`}
                className="object-cover"
                />
            </div>
        </motion.div>
    )
}
