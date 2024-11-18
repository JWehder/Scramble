import TeamData from "./TeamData";
import TableHeaders from "../../../Utils/components/TableHeaders";
import DashboardTitle from "./DashboardTitle";

export default function Standings() {
    const data = [
        {
            teamName: "team 1",
            score: 129,
            top10: 5,
            missedCuts: 4,
            wins: 3
        }
    ]

    for (let i = 2; i <= 12; i++) {
        data.push({
          teamName: `team ${i}`,
          score: 100 + i * 5,  // Generate scores increasing by 5
          top10: i,  // Top 10 increasing by 1
          missedCuts: i % 2,  // Missed cuts increasing by half steps (rounded down)
          wins: i % 3  // Wins cycling between 0, 1, 2
        });
    }

    const sortedData = data.sort((a, b) =>  b.score - a.score);

    const teams = sortedData.map((team, idx) => {
        if (idx % 2 === 0) {
          return <TeamData
          team={team}
          rank = {idx + 1}
          even
          />
        } else {
          return <TeamData
          rank = {idx + 1}
          team={team}
          />
        }
    })

    const headers = ["Rank", "Team", "Score", "Top 10s", "Missed Cuts", "Wins"]

    return (
    <div className="w-full h-full overflow-auto text-light font-PTSans">
        <DashboardTitle>
            <div className="flex-1 text-right mr-3">
                <p>Next Tournament: Masters, April 20th-24th</p>
                <p>Next Draft: April 20th-24th</p>
            </div>
        </DashboardTitle>
        <TableHeaders headers={headers} />
        {teams}
    </div>
    );
}