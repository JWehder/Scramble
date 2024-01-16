import PropTypes from 'prop-types';

export default function SideIcon({ icon, text = 'tooltip' }) {
    return (
        <div className="sidebar-icon group">
            {icon}

            <span className="sidebar-tooltip group-hover:scale-100">
                {text}
            </span>

        </div>

    )
}

SideIcon.propTypes = {
    icon: PropTypes.element.isRequired,
    text: PropTypes.string.isRequired
}