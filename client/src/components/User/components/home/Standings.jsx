import TeamData from "./TeamData";
import LeagueInfo from "./LeagueInfo";

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

      return (
        <div className="w-full h-full overflow-auto text-light font-PTSans">
            <LeagueInfo />
            <div className="w-full flex md:text-lg text-md">
                <div className="text-center flex w-3/6">
                    <div className="w-1/6">
                        Rank
                    </div>
                    <div className="w-5/6">
                        Team
                    </div>
                </div>
                <div className="flex w-3/6 flex-row items-center">
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        Score
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center">
                        Top 10s
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Missed Cuts
                    </div>
                    <div className="flex flex-col w-1/3 items-center justify-center pr-2">
                        Wins
                    </div>
                </div>
            </div>
        {teams}
      </div>

      );
}