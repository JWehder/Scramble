import PropTypes from 'prop-types';
import SideBarTooltip from './SideBarTooltip';

export default function SideIcon({ icon, text = 'tooltip' }) {
    return (
        <div className="sidebar-icon group">
            {icon}

            <SideBarTooltip title= {text} />

        </div>

    )
}

SideIcon.propTypes = {
    icon: PropTypes.element.isRequired,
    text: PropTypes.string.isRequired
}