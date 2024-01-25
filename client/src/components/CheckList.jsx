import { useState } from "react"


export default function CheckList({ element }) {
    const [elementChecked, setElementChecked] = useState(false)

    return (
        <div className="ml-2 mt-2">
            <label htmlFor="element" className="inline-flex items-center">
            <div className={`w-6 h-6 ${elementChecked ? "border border-current rounded-sm" : null}`}>
                <input className=" h-full w-full accent-white" name="element" type="checkbox" checked={elementChecked} onChange={() => setElementChecked(!elementChecked)} />
            </div>
            <span className="ml-2">{element}</span>
            </label>
        </div>
    )
}