import Avatar from "./Avatar"
import imgUrl from "../../assets/i.png"
import imgUrl2 from "../../assets/i-1.png"
import PlayerContent from "./PlayerContent"
import AvatarTooltip from "./PlayerTooltip"
import Player from "./Player"

export default function LeaguePreview() {

    // pull of user's info including their players from state

    // createPlayerAvatars: mapping function for displaying player avatars
    // function createPlayerAvatars() {};

    // if players are playing, they will receive a glowingwrapper

    return (
        <div className="flex p-2">
        <div>
            Team 1 
            <div className='flex my-1 align-center justify-center'>
                <Player 
                    imgUrl={imgUrl}        
                    name="Justin Thomas" 
                    size="14"
                    score={-2}
                />
                <AvatarTooltip
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
                <AvatarTooltip 
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    score={2}
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
                <AvatarTooltip 
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
            </div>
            <span>108.08</span>
        </div>
        <div className="mx-1">
        vs 
        </div>
        <div>
            Team 2
            <div className='flex my-1 align-center justify-center'>
                <AvatarTooltip
                avatar={
                    <Avatar 
                    imgUrl={imgUrl} 
                    name="Justin Thomas" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
                <AvatarTooltip
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
                <AvatarTooltip 
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>
                <AvatarTooltip
                avatar={
                    <Avatar 
                    imgUrl={imgUrl2} 
                    name="Scottie Scheffler" 
                    size="14"
                    />
                }
                >
                    <PlayerContent />
                </AvatarTooltip>    

            </div>
            <span>108.08</span>
        </div>
        
    </div>
    )
}