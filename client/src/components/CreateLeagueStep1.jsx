import { useState } from "react"

export default function CreateLeagueStep1({ setCreateLeagueStep }) {
    const [isPrivate, setIsPrivate] = useState(false)

    const showPasscodeInput = () => {
        if(isPrivate) return (
            <div>
                <label for="pass-code">Pass Code</label>
                <input class="border" name="pass-code" type="text" placeholder="pass code"/>
            </div>
        )
        else return null
    }

    return (
        <div>
            <div>
                <div>
                    <label for="league-name">League Name</label>
                    <input class="border" name="league-name" type="text" placeholder="league name" />
                </div>
                <div>
                    <label for="private-check">Private</label>
                    <input class="border" name="private-check" type="checkbox" checked={isPrivate} onChange={() => setIsPrivate(!isPrivate)} />
                </div>
                {showPasscodeInput()}
                <div>
                    <label for="share-link">Copy this link to share with friends</label>
                    <input class="border" name="share-link" type="text" placeholder="premade link" />
                </div>
                <button class="border hover:bg-black" onClick={() => setCreateLeagueStep(2)}>Next</button>
            </div>
        </div>
    )
}