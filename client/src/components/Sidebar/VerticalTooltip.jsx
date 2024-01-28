import { useRef } from "react";
import { propTypes } from "react-bootstrap/esm/Image";

export default function VerticalTooltip({ children }) {

    const container = useRef();
    const tooltipRef = useRef();

    return (
        <div 
        ref = {container}
        onMouseEnter={() => {
            if (!tooltipRef || !container.current) return;

            tooltipRef.current.style.top = -15 + "px";
        }}
        className='group/item relative inline-block text-center'
        >
            {children}
                <div
                ref={tooltipRef}
                className='invisible group-hover/item:visible opacity-0 group-hover/item:opacity-75 transition bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
                >
                    <div>Hole: 13</div>
                    <div>Place: 13th</div>
                </div>    
        </div>
    )
}

VerticalTooltip.propTypes = {
    children: propTypes.node
}