import PropTypes from 'prop-types';

export default function Tooltip({ children, icon, direction }) {

    switch (direction) {
        case "top":
            direction = "top-14";
            break;
        case "left":
            direction = "left-14"
            break;
        case "right":
            direction = "right-14";
            break;
        case "bottom":
            direction = "bottom-14";
            break;
        default:
            direction = "left-14";
            break;
    }

    return (
        <div className="tooltip-container group">
            {icon}

            <div className={`tooltip group-hover:scale-100 ${direction}`}>
                {children}
            </div>
            
        </div>
    )
}

Tooltip.propTypes = {
    children: PropTypes.node.isRequired,
    direction: PropTypes.string
}