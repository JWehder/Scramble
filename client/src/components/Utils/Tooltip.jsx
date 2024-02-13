import PropTypes from 'prop-types';

export default function Tooltip({ children, icon, direction, sidebar }) {

    let tooltipContainerClass = 'tooltip-container';
    let tooltipClass = 'tooltip'; 

    if (sidebar) {
        tooltipContainerClass = 'sidebar-tooltip-container';
        tooltipClass = 'sidebar-tooltip';
    }

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
        <div className={`${tooltipContainerClass} group`}>
            {icon}

            <div className={`${tooltipClass} group-hover:scale-100 ${direction}`}>
                {children}
            </div>
        </div>
    )
}

Tooltip.propTypes = {
    children: PropTypes.node.isRequired,
    direction: PropTypes.string,
    sidebar: PropTypes.bool
}