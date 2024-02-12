import PropTypes from 'prop-types'
import Game from './Game';
import User from './User'
import League from './League';
import Message from './Message';
import Article from './Article';
import { useSelector } from "react-redux";

export default function DropoutItem({ type }) {

    let userData;

    let Component;

    switch (type) {
        case "Messages":
            Component = Message;
            userData = useSelector((state) => state.users.messages);
            if (!userData) userData = defaultData.messages;
            break;
        case "Teams & Leagues":
            Component = League;
            userData = useSelector((state) => state.users.leagues);
            if (!userData) userData = defaultData.leagues;
            break;
        case "Play":
            Component = Game;
            userData = useSelector((state) => state.users.games);
            if (!userData) userData = defaultData.games;
            break;
        case "User":
            Component = User;
            break;
        case "Articles":
            Component = Article;
            userData = useSelector((state) => state.users.articles);
            if (!userData) userData = defaultData.articles;
        default:
            Component = Article;
            break;
    }

    return (
        <>
            <div className="flex items-center justify-center flex-col">
                { userData ?
                userData.slice(0, 3).map((datapoint) => <Component data={datapoint} />)
                :
                `there are no ${type} to display: ${userData}`
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
    type: PropTypes.string.isRequired,
    userData: PropTypes.arrayOf(PropTypes.string)
}