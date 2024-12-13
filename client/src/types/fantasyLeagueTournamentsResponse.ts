import { Tournament } from "./tournaments"

export interface FantasyLeagueTournamentsResponse {
    pastFantasyLeagueTournaments: Tournament[],
    upcomingFantasyLeagueTournaments: Tournament[],
    upcomingProSeasonTournaments: Tournament[]
}