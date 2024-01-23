import PropTypes from 'prop-types';
import { useRef } from 'react';


export default function Tooltip({ children, tooltip }) {
    const tooltipRef = useRef(null);
    const container = useRef(null);

    return (
        <div 
        ref = {container}
        onMouseEnter={({clientX}) => {
            if (!tooltipRef || !container.current) return;
            const { left } = container.current.getBoundingClientRect();

            tooltipRef.current.style.left = (clientX - left) + "px";
        }}
        className='group relative inline-block'
        >
            {children}
            <span 
            ref={tooltipRef}
            className='invisible group-hover:visible opacity-0 group-hover:opacity-100 transition bg-blue-500 text-white p-1 rounded absolute top-full mt-2 whitespace-nowrap'
            >
                {tooltip}
            </span>

        </div>
    )
}

Tooltip.propTypes = {
    tooltip: PropTypes.string.isRequired,
    children: PropTypes.node
}