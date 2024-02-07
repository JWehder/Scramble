import { useState } from "react"
import SelectedTournament from "./SelectedTournament"
import TournamentElement from "./TournamentElement"

export default function CreateLeagueStep3({ setCreateLeagueStep }) {
    const [selectedTournaments, setSelectedTournaments] = useState([])

    const tournaments = () => {
        const tournamentArray = []
        for(let i = 1; i <= 15; i++) {
            tournamentArray.push(`tournament ${i}`)
        }
        return tournamentArray
    }

    const removeTournament = (element) => {
        const newSelectedTournaments = selectedTournaments.filter(e => e !== element)
        setSelectedTournaments(newSelectedTournaments)
    }

    return (
        <div>
            <p className="text-xl font-bold pb-3">Tournaments</p>
            <div className="inline-flex items-center">
                <div className="border border-black overflow-y-auto h-60 w-96 mr-8">
                    {tournaments().map(e => <TournamentElement key={e} element={e} selectedTournaments={selectedTournaments} setSelectedTournaments={setSelectedTournaments} />)}
                </div>
                <div className="border border-black overflow-y-auto h-60 w-96">
                    {selectedTournaments.map(e => <SelectedTournament key={e} element={e} removeTournament={removeTournament} />)}
                </div>
            </div>
            <div className="grid justify-end pt-3">
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(1)}>Finish</button>
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(2)}>Back</button>
            </div>
        </div>
    )
}