import { Hole } from "./holes";

export type Round = {
    Albatross: number;
    Birdies: number;
    Bogeys: number;
    DoubleBogeys: number;
    Eagles: number;
    GolferTournamentDetailsId: string;
    Holes: Hole[]; 
    Pars: number;
    Round: string;
    Score: number;
    TournamentId: string;
    WorseThanDoubleBogeys: number;
    created_at: string; // ISO date string
    id: string;
    updated_at: string; // ISO date string
};