import Avatar from "../../../Utils/components/Avatar";
import Badge from "../../../Utils/components/Badge";
import PlayerContent from "./PlayerContent";
import PlayerTooltip from "./PlayerTooltip";
import PropTypes from 'prop-types';

export default function Player({ score = 0, imgUrl, name, size, active }) {
    let badgeColor;
    let badgeSize;
    let avatarSize = null;

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

    switch(size) {
        case 'sm':
            badgeSize = '1';
            avatarSize = '10';
            break;
        case 'md':
            badgeSize = '3';
            avatarSize = '12';
            break;
        case 'lg':
            badgeSize = '5';
            avatarSize = '14';
            break;    
    }


    return (
        <>
            { active ?
                <PlayerTooltip
                player={
                    <div className="relative flex items-center justify-center rounded-full pt-4">
                        <Avatar 
                        imgUrl={imgUrl}
                        name={name}
                        size={avatarSize}
                        />
                            <Badge 
                            bgColor={badgeColor}
                            className={`hover:opacity-95 opacity-75 text-white`}
                            size={badgeSize}
                            >
                                {score}
                            </Badge>
                    </div>
                }
                >
                    <PlayerContent />
                </PlayerTooltip>
                :
                <PlayerTooltip
                player={
                    <Avatar 
                    imgUrl={imgUrl}
                    name={name}
                    size={avatarSize}
                    />
                }
                >
                    <div
                    className='hover:visible opacity-75 bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
                    >
                        {name}
                    </div>
                </PlayerTooltip>

            
            }

        </>
    )
}

Player.propTypes = {
    name: PropTypes.string.isRequired,
    imgUrl: PropTypes.string.isRequired,
    size: PropTypes.string.isRequired, 
    score: PropTypes.number
}