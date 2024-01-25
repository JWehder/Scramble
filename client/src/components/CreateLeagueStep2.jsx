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
            <h2>Rules</h2>
            <div className="border overflow-y-auto h-40">
                {rules().map(e => <CheckList key={e} element={e} />)}
            </div>
            <button className="border hover:bg-black" onClick={() => setCreateLeagueStep(3)}>Next</button>
            <button className="border hover:bg-black" onClick={() => setCreateLeagueStep(1)}>Back</button>
        </div>
    )
}