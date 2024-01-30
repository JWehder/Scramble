import PropTypes from 'prop-types';
import SideBarTooltip from './SideBarTooltip';
import VerticalTooltip from './VerticalTooltip';

export default function SideIcon({ icon, type = 'tooltip', user }) {

    return (
        <div className="sidebar-icon group">
            {icon}

            { user ?
                <VerticalTooltip /> 
                :
                <SideBarTooltip title= {type} direction={'top-14'} />
            }
            
        </div>
    )
}

SideIcon.propTypes = {
    icon: PropTypes.element.isRequired,
    type: PropTypes.string.isRequired,
    user: PropTypes.bool.isRequired
}