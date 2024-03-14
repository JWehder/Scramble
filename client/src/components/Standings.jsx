import Starters from "./Utils/components/Starters";

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

      return (
        <div className="w-10/12 overflow-auto rounded-lg shadow-md">
          <table className="w-full overflow-hidden">
            <thead>
              <tr className="text-xs font-medium text-light uppercase bg-dark border-b border-gray-200 text-center">
                <th className="p-4">Rank</th>
                <th className="p-4">Team Name</th>
                <th className="p-4">Score</th>
                <th className="p-4">Top 10</th>
                <th className="p-4">Missed Cuts</th>
                <th className="p-4">Wins</th>
              </tr>
            </thead>
            <tbody>
              {sortedData.map((item, index) => (
                <tr key={index} className="border-b border-gray-200 hover:bg-middle">
                    <td className=" text-center p-2 whitespace-nowrap">{index + 1}</td>
                    <td className="p-2">
                        <div className="flex-row flex justify-center items-center">
                            {item.teamName}
                        </div>  
                        <div className="flex-row flex justify-center items-center">
                            <Starters />
                        </div>  
                    </td>
                    <td className="p-2 text-center">{item.score}</td>
                    <td className="p-2 text-center">{item.top10}</td>
                    <td className="p-2 text-center">{item.missedCuts}</td>
                    <td className="p-2 text-center">{item.wins}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}