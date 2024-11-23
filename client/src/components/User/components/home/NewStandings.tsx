import React from "react";
import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from "chart.js";
import TableHeaders from "../../../Utils/components/TableHeaders";
import TableRow from "../../../Utils/components/TableRow";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

export default function Standings() {
  const data = [
    {
      teamName: "Farhan's Team",
      score: 221,
      wins: 8,
      missedCuts: 2,
      top10s: 19,
      totalUnderPar: -221,
    },
    {
      teamName: "Birdie Kings",
      score: 200,
      wins: 6,
      missedCuts: 3,
      top10s: 15,
      totalUnderPar: -190,
    },
    {
      teamName: "Sand Masters",
      score: 185,
      wins: 5,
      missedCuts: 4,
      top10s: 12,
      totalUnderPar: -175,
    },
    {
      teamName: "Bogey Busters",
      score: 175,
      wins: 3,
      missedCuts: 5,
      top10s: 10,
      totalUnderPar: -150,
    },
    {
      teamName: "Eagle Eyes",
      score: 165,
      wins: 4,
      missedCuts: 6,
      top10s: 8,
      totalUnderPar: -130,
    },
  ];

  // Prepare data for charts
  const teamNames = data.map((team) => team.teamName);
  const scores = data.map((team) => team.score);
  const wins = data.map((team) => team.wins);
  const missedCuts = data.map((team) => team.missedCuts);
  const top10s = data.map((team) => team.top10s);

  const headers = ["Rank", "Team", "Score", "Top 10s", "Missed Cuts", "Wins"]

  // Bar chart data
  const barData = {
    labels: teamNames,
    datasets: [
      {
        label: "Scores",
        data: scores,
        backgroundColor: "#4ADE80",
      },
    ],
  };

  const desiredKeysSet = new Set(["score",
  "wins",
  "missedCuts",
  "top10s",
  "totalUnderPar"])

  // Pie chart data for wins
  const pieData = {
    labels: teamNames,
    datasets: [
      {
        data: wins,
        backgroundColor: ["#34D399", "#60A5FA", "#F87171", "#FBBF24", "#A78BFA"],
      },
    ],
  };

  return (
    <div className="w-full h-full overflow-auto p-6 space-y-10 bg-dark text-light font-PTSans">
      {/* Dashboard Title */}
      <div className="flex justify-between items-center mb-6">
        <div className="text-right">
          <p>Next Tournament: Masters, April 20th-24th</p>
          <p>Next Draft: April 20th-24th</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Bar Chart */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Team Scores</h2>
          <Bar data={barData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        {/* Pie Chart */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Team Wins Distribution</h2>
          <Pie data={pieData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>
      </div>

      {/* Leaderboard */}
      <div className="">
        <TableHeaders headers={headers} />
      </div>
        {data.map((team, idx) => (
            <TableRow 
            firstTwoDatapoints={[idx + 1, team.teamName]}
            data={team}
            columns={desiredKeysSet}
            brightness={idx % 2 === 0 ? 'brightness-125' : ''}
            onClick={() => console.log("clicked this team")}
            />
        ))}
      </div>
  );
}