import CheckList from "./CheckList"

export default function CreateLeagueStep3({ setCreateLeagueStep }) {
    const tournaments = () => {
        const tournamentArray = []
        for(let i = 1; i <= 15; i++) {
            tournamentArray.push(`tournament ${i}`)
        }
        return tournamentArray
    }

    return (
        <div>
            <h2>Schedule</h2>
            <div className="border overflow-y-auto h-40">
                {tournaments().map(e => <CheckList key={e} element={e} />)}
            </div>
            <button className="border hover:bg-black" onClick={() => setCreateLeagueStep(1)}>Finish</button>
            <button className="border hover:bg-black" onClick={() => setCreateLeagueStep(2)}>Back</button>
        </div>
    )
}