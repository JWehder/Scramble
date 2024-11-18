import { Team } from "./teams"
import { League } from "./leagues"

export interface UsersData {
    Username: string
    Email: string
    Teams: Team[]
    Leagues: League[]
    IsVerified: Boolean
    VerificationExpiresAt: Date
}