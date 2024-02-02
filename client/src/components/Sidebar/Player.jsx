import Avatar from "./Avatar";
import PlayerContent from "./PlayerContent";
import PlayerTooltip from "./PlayerTooltip";

export default function Player({ score = 0, imgUrl, name, size }) {
    let badgeColor;

    if (score > 0) {
        badgeColor = 'bg-red-600';
    } else if (score === 0) {
        badgeColor = 'bg-gray-600';
    } else {
        badgeColor = 'bg-green-600';
    }

    return (
        <>
            <PlayerTooltip
            player={
                <>
                <Avatar 
                imgUrl={imgUrl}
                name={name}
                size={size}
                />
                <div className={`absolute ${badgeColor} rounded-full top-0 left-0 opacity-85 p-1 h-5 w-5`}>
                        <span className='text-xs text-center'>{score}</span>
                </div>
                </>
            }
            >
                <PlayerContent />
            </PlayerTooltip>

        </>
    )
}