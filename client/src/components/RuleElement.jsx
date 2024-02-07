import { useState } from "react"


export default function RuleElement({ element }) {
    const [textInput, setTextInput] = useState("")

    return (
        <div className="ml-2 mt-2">
            <label htmlFor="element" className="inline-flex items-center">
                <input className="border border-black w-12 text-black placeholder-black h-8 pl-2" name="element" type="text" value={textInput} onChange={() => setTextInput()} />
                <span className="ml-2">{element}</span>
            </label>
        </div>
    )
}