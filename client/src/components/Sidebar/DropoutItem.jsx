import PropTypes from 'prop-types'
import DropdownLi from './DropdownLi';
import User from './User'
import League from './League';
import Message from './Message';
import Article from './Article';

export default function DropoutItem({ type }) {
    let userData = null;

    switch (type) {
        case "Messages":
            type = <Message />;
            userData = [1,2,3,4];
            break;
        case "Teams & Leagues":
            type = <League />;
            userData = [1,2,3,4];
            break;
        case "Play":
            type = <DropdownLi />;
            userData = [1,2,3,4];
            break;
        case "User":
            type = <User />;
            userData = [1,2,3,4];
            break;
        default:
            type = <Article />;
            userData = [1,2,3,4];
            break;
    }

    return (
        <>
            <div className="flex items-center justify-center flex-col">
                { userData ?
                userData.slice(0, 3).map(() => type)
                :
                `there are no ${type} to display`
                }
                <div 
                className="divide-x divide-x-slate-700 p-2 hover:bg-slate-700 rounded-md w-24">
                    See more...
                </div>
            </div>
        </>

    )

}

DropoutItem.propTypes = {
    type: PropTypes.string.isRequired
}