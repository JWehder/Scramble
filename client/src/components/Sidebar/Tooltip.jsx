import PropTypes from 'prop-types';
import { useRef } from 'react';

export default function Tooltip({ children, tooltip }) {
    const tooltipRef = useRef(null);
    const container = useRef(null);

    const currentScore = -2;
    const prevFourHolesScore = -1;

    return (
        <div 
        ref = {container}
        onMouseEnter={() => {
            if (!tooltipRef || !container.current) return;

            tooltipRef.current.style.left = -15 + "px";
        }}
        className='group/item relative inline-block text-center'
        >
            {children}

            {currentScore ? 
                <div
                ref={tooltipRef}
                className='invisible group-hover/item:visible opacity-0 group-hover/item:opacity-75 transition bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
                >
                    {tooltip}
                    <div>Hole: 13</div>
                    <div>Place: 13th</div>
                    <div>Currently: {currentScore}</div>
                    <div>Prev. 4 Holes: {prevFourHolesScore}</div>
                </div>    
                :
                <span 
                ref={tooltipRef}
                className='invisible group-hover/item:visible opacity-0 group-hover/item:opacity-75 transition bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
                >
                    {tooltip}
                </span>
            }
        </div>
    )
}

Tooltip.propTypes = {
    tooltip: PropTypes.string.isRequired,
    children: PropTypes.node,
    direction: PropTypes.string
}