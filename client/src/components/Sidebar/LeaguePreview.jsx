import Avatar from "./Avatar"
import imgUrl from "../../assets/i.png"
import imgUrl2 from "../../assets/i-1.png"
import GlowingWrapper from "./GlowingWrapper"
import Tooltip from "./Tooltip"
import PlayerContent from "./PlayerContent"

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
                <Tooltip 
                icon={
                    <Avatar 
                    imgUrl={imgUrl} 
                    name="Justin Thomas" 
                    size="14"
                    score={-2}
                    />
                }
                direction = "top"
                >
                    <PlayerContent />
                </Tooltip>

                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                score={2}
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                />
            </div>
            <span>108.08</span>
        </div>
        <div className="mx-1">
        vs 
        </div>
        <div>
            Team 2
            <div className='flex my-1 align-center justify-center'>
                <Avatar 
                imgUrl={imgUrl} 
                name="Justin Thomas" 
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                size="14"
                />
            </div>
            <span>108.08</span>
        </div>
        
    </div>
    )
}