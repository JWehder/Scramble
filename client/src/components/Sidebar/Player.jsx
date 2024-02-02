import Avatar from "../Utils/Avatar";
import Badge from "../Utils/Badge";
import PlayerContent from "./PlayerContent";
import PlayerTooltip from "./PlayerTooltip";

export default function Player({ score = 0, imgUrl, name, size }) {
    let badgeColor;

    if (score > 0) {
        badgeColor = 'bg-red-600/75';
    } else if (score === 0) {
        badgeColor = 'bg-gray-600/75';
    } else {
        badgeColor = 'bg-green-600/75';
    }

    return (
        <>
            <PlayerTooltip
            player={
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
            }
            >
                <PlayerContent />
            </PlayerTooltip>

        </>
    )
}