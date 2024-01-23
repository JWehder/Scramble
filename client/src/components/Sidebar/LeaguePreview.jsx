import Avatar from "./Avatar"
import imgUrl from "../../assets/i.png"
import imgUrl2 from "../../assets/i-1.png"

export default function LeaguePreview() {

    // pull of user's info including their players from state

    // createPlayerAvatars: mapping function for displaying player avatars
    // function createPlayerAvatars() {};

    // function determining the player's border color
    // function determineBorderColor() {}

    return (
        <div className="flex p-2">
        <div>
            Team 1 
            <div className='flex my-1 align-center justify-center'>
                <Avatar 
                imgUrl={imgUrl} 
                name="Justin Thomas" 
                borderColor="ring-green"
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                borderColor="border-gray-700"
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
                borderColor="border-green-700"
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
                borderColor="border-green-700"
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                borderColor="border-green-700"
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                borderColor="border-red-700"
                size="14"
                />
                <Avatar 
                imgUrl={imgUrl2} 
                name="Scottie Scheffler" 
                borderColor="border-green-700"
                size="14"
                />
            </div>
            <span>108.08</span>
        </div>
        
    </div>
    )
}