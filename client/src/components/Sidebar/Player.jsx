import Avatar from "../Utils/Avatar";
import Badge from "../Utils/Badge";
import PlayerContent from "./PlayerContent";
import PlayerTooltip from "./PlayerTooltip";
import PropTypes from 'prop-types';

export default function Player({ score = 0, imgUrl, name, size }) {
    let badgeColor;

    if (score > 0) {
        badgeColor = 'bg-red-600/75';
        score = '+' + score.toString();
    } else if (score === 0) {
        badgeColor = 'bg-gray-600/75';
        score = 'E'
    } else {
        badgeColor = 'bg-green-600/75';
        score = score.toString();
    }

    return (
        <>
            <div className="relative flex items-center justify-center rounded-full pt-4">
                <Avatar 
                imgUrl={imgUrl}
                name={name}
                size={size}
                />
                <Badge 
                bgColor={badgeColor}
                className={`hover:opacity-95 opacity-75 text-white`}
                >
                    {score}
                </Badge>
            </div>
        </>
    )
}

Player.propTypes = {
    name: PropTypes.string.isRequired,
    imgUrl: PropTypes.string.isRequired,
    size: PropTypes.string.isRequired, 
    score: PropTypes.number
}