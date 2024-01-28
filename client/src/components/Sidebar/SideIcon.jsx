import PropTypes from 'prop-types';
import SideBarTooltip from './SideBarTooltip';
import VerticalTooltip from './VerticalTooltip';

export default function SideIcon({ icon, text = 'tooltip', user }) {
    return (
        <div className="sidebar-icon group">
            {icon}

            { user ?
                <VerticalTooltip /> 
                :
                <SideBarTooltip title= {text} />
            }
            

        </div>

    )
}

SideIcon.propTypes = {
    icon: PropTypes.element.isRequired,
    text: PropTypes.string.isRequired,
    user: PropTypes.bool.isRequired
}