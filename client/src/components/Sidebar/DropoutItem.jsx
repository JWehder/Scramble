import PropTypes from 'prop-types'
import Message from './Message';
import LeaguePreview from './LeaguePreview';
import DropdownLi from './DropdownLi';
import News from './News';
import User from './User'

export default function DropoutItem({ type }) {

    switch (type) {
        case "Messages":
            type = <Message />;
            break;
        case "Leagues":
            type = <LeaguePreview />;
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

    return type;

}

DropoutItem.propTypes = {
    type: PropTypes.string.isRequired
}