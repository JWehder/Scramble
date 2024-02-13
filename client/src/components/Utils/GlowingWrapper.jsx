import PropTypes from 'prop-types';

export default function GlowingWrapper({ children, color, pulse }) {

    switch (color) {
        case "red":
            color = "from-red-600";
            break;
        case "gray":
            color = "from-gray-600";
            break;
        case "green":
            color = "from-green-600";
            break;
        default:
            color = "from-green-600";
            break;
    }

    pulse = pulse ? 'animate-pulse' : '';

    return (
        <div className="relative inline-block">
            <div className={`absolute -inset-0 rounded-full blur-sm bg-gradient-to-r ${color} to-white ${pulse}`} />
            {children}
        </div>
    )
}

GlowingWrapper.propTypes = {
    color: PropTypes.string.isRequired
}