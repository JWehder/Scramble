import PropTypes from 'prop-types'
import Message from './Message';
import LeaguesPreview from './LeaguesPreview';
import DropdownLi from './DropdownLi';
import News from './News';
import User from './User'

export default function DropoutItem({ type }) {

    switch (type) {
        case "Messages":
            type = <Message />;
            break;
        case "Teams & Leagues":
            type = <LeaguesPreview />;
            break;
        case "Play":
            type = <DropdownLi />;
            break;
        case "User":
            type = <User />;
            break;
        default:
            type = <News />;
            break;
    }

    return (
        <div>
            {type}
        </div>
    )

}

DropoutItem.propTypes = {
    type: PropTypes.string.isRequired
}