import { useState } from "react"

export default function CreateLeagueStep1({ setCreateLeagueStep }) {
    const [isPrivate, setIsPrivate] = useState(false)

    const showPasscodeInput = () => {
        if(isPrivate) return (
            <div>
                <input className="border border-black text-black placeholder-black h-12 w-96 pl-2" name="pass-code" type="text" placeholder="Pass Code"/>
            </div>
        )
        else return null
    }

    return (
        <div className="pt-6">
            <div className="pb-3">
                <input className="border border-black text-black placeholder-black h-12 w-96 pl-2" name="league-name" type="text" placeholder="League Name" />
            </div>
            <div className="pb-3">
                <label htmlFor="private-check" className="inline-flex items-center">
                    <span className="mr-2">Private</span>
                    <div className={`w-8 h-8 ${isPrivate ? "border border-current rounded-sm" : null}`}>
                        <input className=" h-full w-full accent-white" name="private-check" type="checkbox" checked={isPrivate} onChange={() => setIsPrivate(!isPrivate)} />
                    </div>
                </label>
            </div>
            {showPasscodeInput()}
            <div className="grid pt-1 pb-3">
                <label htmlFor="share-link">Copy this link to share with friends</label>
                <input className="border border-black w-64 text-black placeholder-black h-12 w-96 pl-2" name="share-link" type="text" placeholder="premade link" />
            </div>
            <div className="grid justify-center">
                <button className="border font-bold bg-gray-400 hover:bg-white h-12 w-72" onClick={() => setCreateLeagueStep(2)}>Next</button>
            </div>
        </div>
    )
}