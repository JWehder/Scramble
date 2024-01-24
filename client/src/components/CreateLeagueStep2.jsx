export default function CreateLeagueStep2({ setCreateLeagueStep }) {
    return (
        <div>
            <h2>test2</h2>
            <button class="border hover:bg-black" onClick={() => setCreateLeagueStep(1)}>Back</button>
        </div>
    )
}