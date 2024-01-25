import { useState } from "react"

export default function CreateLeagueStep1({ setCreateLeagueStep }) {
    const [isPrivate, setIsPrivate] = useState(false)

    const showPasscodeInput = () => {
        if(isPrivate) return (
            <div>
                <label htmlFor="pass-code">Pass Code</label>
                <input className="border" name="pass-code" type="text" placeholder="pass code"/>
            </div>
        )
        else return null
    }

    return (
        <div>
            <div>
                <div>
                    <label htmlFor="league-name">League Name</label>
                    <input className="border" name="league-name" type="text" placeholder="league name" />
                </div>
                <div>
                    <label htmlFor="private-check">Private</label>
                    <input className="border" name="private-check" type="checkbox" checked={isPrivate} onChange={() => setIsPrivate(!isPrivate)} />
                </div>
                {showPasscodeInput()}
                <div>
                    <label htmlFor="share-link">Copy this link to share with friends</label>
                    <input className="border" name="share-link" type="text" placeholder="premade link" />
                </div>
                <button className="border hover:bg-black" onClick={() => setCreateLeagueStep(2)}>Next</button>
            </div>
        </div>
    )
}