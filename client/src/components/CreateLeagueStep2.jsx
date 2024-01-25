import CheckList from "./CheckList"

export default function CreateLeagueStep2({ setCreateLeagueStep }) {
    const rules = () => {
        const ruleArray = []
        for(let i = 1; i <= 15; i++) {
            ruleArray.push(`rule ${i}`)
        }
        return ruleArray
    }

    return (
        <div>
            <p className="text-xl font-bold pb-3">Rules</p>
            <div className="border border-black overflow-y-auto h-60 w-96">
                {rules().map(e => <CheckList key={e} element={e} />)}
            </div>
            <div className="grid justify-end pt-3">
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(3)}>Next</button>
                <button className="border font-bold bg-gray-400 hover:bg-white w-40" onClick={() => setCreateLeagueStep(1)}>Back</button>
            </div>
        </div>
    )
}