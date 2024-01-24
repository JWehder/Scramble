import { useState } from "react";
import CreateLeagueStep1 from "./CreateLeagueStep1";
import CreateLeagueStep2 from "./CreateLeagueStep2";

export default function CreateLeague() {
    const [createLeagueStep, setCreateLeagueStep] = useState(1)

    const createLeagueSteps = () => {
        if(createLeagueStep === 1) return <CreateLeagueStep1 setCreateLeagueStep={setCreateLeagueStep}/>
        else return <CreateLeagueStep2 setCreateLeagueStep={setCreateLeagueStep}/>
    }

    return (
        <div class="p-10">
            <h3>Create A League</h3>
            <div>
                {createLeagueSteps()}
            </div>
        </div>
    )
}