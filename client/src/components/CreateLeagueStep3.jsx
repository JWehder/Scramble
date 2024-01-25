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
            <p className="text-xl font-bold pb-3">Tournaments</p>
            <div className="border border-black overflow-y-auto h-60 w-96">
                {tournaments().map(e => <CheckList key={e} element={e} />)}
            </div>
            <div className="grid justify-end pt-3">
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(1)}>Finish</button>
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(2)}>Back</button>
            </div>
        </div>
    )
}