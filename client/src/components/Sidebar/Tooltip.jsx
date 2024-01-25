import PropTypes from 'prop-types';
import { useRef } from 'react';

export default function Tooltip({ children, tooltip }) {
    const tooltipRef = useRef(null);
    const container = useRef(null);

    // made up currentScore val until we have data
    

    return (
        <div 
        ref = {container}
        onMouseEnter={() => {
            if (!tooltipRef || !container.current) return;

            tooltipRef.current.style.left = -10 + "px";
        }}
        className='group/item relative inline-block'
        >
            {children}
            <span 
            ref={tooltipRef}
            className='invisible group-hover/item:visible opacity-0 group-hover/item:opacity-75 transition bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
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