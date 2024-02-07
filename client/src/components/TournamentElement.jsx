import { useState } from "react"


export default function TournamentElement({ element, selectedTournaments, setSelectedTournaments }) {
    const addTournamentToList = () => {
        if(selectedTournaments.includes(element) === false) setSelectedTournaments([...selectedTournaments, element])
    }

    return (
        <div className="ml-2 mt-2">
            <label htmlFor="element" className="inline-flex items-center">
                <button className="border font-bold bg-gray-400 hover:bg-white w-12" onClick={addTournamentToList}>Add</button>
                <span className="ml-2">{element}</span>
            </label>
        </div>
    )
}