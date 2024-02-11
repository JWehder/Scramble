import PropTypes from 'prop-types'
import DropdownLi from './DropdownLi';
import User from './User'
import League from './League';
import Message from './Message';
import Article from './Article';

export default function DropoutItem({ type, userData }) {

    // userData = [
    //     "Hey there!",
    //     "Hey there!",
    //     "Hey there!"
    // ];


    let leaguesData = 
        [
            {
            "name": "Jake's League",
            "team1Name": "Jake's team",
            "team2Name": "Mitch's team"
            },
            {
              "name": "Jake's League",
              "team1Name": "Jake's team",
              "team2Name": "Mitch's team"
            },
            {
              "name": "Jake's League",
              "team1Name": "Jake's team",
              "team2Name": "Mitch's team"
            }
        ];

    let Component;

    switch (type) {
        case "Messages":
            Component = Message;
            break;
        case "Teams & Leagues":
            Component = League;
            break;
        case "Play":
            Component = DropdownLi;
            break;
        case "User":
            Component = User;
            break;
        default:
            Component = Article;
            break;
    }

    console.log(userData);

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