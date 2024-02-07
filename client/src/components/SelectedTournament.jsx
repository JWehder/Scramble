export default function SelectedTournament({ element, removeTournament }) {
    return (
        <div className="ml-2 mt-2">
            <label htmlFor="element" className="inline-flex items-center">
                <button className="border font-bold bg-gray-400 hover:bg-white w-8" onClick={() => removeTournament(element)}>X</button>
                <span className="ml-2">{element}</span>
            </label>
        </div>
    )
}