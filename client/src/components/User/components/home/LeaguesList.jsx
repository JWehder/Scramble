import MatchPlayQuickView from "./MatchPlayQuickView"
import StrokePlayQuickView from "./StrokePlayQuickView"

export default function LeaguesList() {
    const leagues = [
        {
            leagueName: "League",
            leagueType: "Strokes Play",
            myCurrentPlace: "6th",
            teamAhead: {
                teamName: "team4",
                teamScore: -11,
                top10: 2,
                rank: 4
            },
            teamBehind: {
                teamName: "team6",
                teamScore: -8,
                top10: 1,
                rank: 2
            },
            myTeam: {
                teamName: "team5",
                teamScore: -10,
                top10: 2,
                rank: 6
            }
        },
        {
            name: "League",
            type: "Match Play",
            team1Rank: "6th",
            team2Rank: "4th",
            team1Name: "team1",
            team2Name:"team2",
            team2Players: ["player1", "player2", "player3"],
            team1Players: ["player1", "player2", "player3"],
            team1Score: -11,
            team2Score: -5
        },
        {
            leagueName: "League",
            leagueType: "Best Ball",
            myCurrentPlace: 6,
            teamAhead: {
                teamName: "team4",
                teamScore: -11,
                top10: 2,
                rank: 4
            },
            teamBehind: {
                teamName: "team6",
                teamScore: -8,
                top10: 1,
                rank: 2
            },
            myTeam: {
                teamName: "team5",
                teamScore: -10,
                top10: 2,
                rank: 6
            }
        },
    ]


    return (
        <div className="flex gap-2 h-full w-full flex-col">
            <MatchPlayQuickView league={leagues[1]} />
            <StrokePlayQuickView league={leagues[2]} />
        </div>
    )
}