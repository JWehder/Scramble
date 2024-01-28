import PropTypes from 'prop-types'
import Message from './Message';
import LeaguePreview from './LeaguePreview';
import DropdownLi from './DropdownLi';
import News from './News';

export default function DropoutItem({ title }) {

    let type = null;

    switch (title) {
        case "Messages":
            type = <Message />;
            break;
        case "Leagues":
            type = <LeaguePreview />;
            break;
        case "Play":
            type = <DropdownLi />
            break;
        case "User":
            
        default:
            type = <News />
            break;
    }

    return type;

}

DropoutItem.propTypes = {
    title: PropTypes.string.isRequired
}