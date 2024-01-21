import Avatar from "./Avatar"
import imgUrl from "../assets/i.png"
import imgUrl2 from "../assets/i-1.png"

export default function LeaguePreview() {

    return (
        <div className="flex">
        <div>
            Team 1 
            <div className='flex my-1 align-center justify-center'>
                <Avatar imgUrl={imgUrl} name="Justin Thomas" />
                <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
                <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
            </div>
            <span>108.08</span>
        </div>
        <div className="mx-1">
        vs 
        </div>
        <div>
            Team 2
            <div className='flex my-1 align-center justify-center'>
                <Avatar imgUrl={imgUrl} name="Justin Thomas" />
                <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
                <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
            </div>
            <span>108.08</span>
        </div>
        
    </div>
    )
}