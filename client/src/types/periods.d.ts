interface FreeAgentSignings {
    [key: string]: Array[string]
}

interface Drops {
    [key: string]: Array[string]
}

export interface Period {
    id: string;
    StartDate: Date;
    EndDate: Date;
    PeriodNumber: number;
    WaiverPool?: object;
    FantasyLeagueSeasonId: string;
    Standings: Array[string];
    FreeAgentSignings?: FreeAgentSignings;
    Matchups?: Array[[string, string]];
    Drops?: Drops;
    TournamentId: string;
    TeamResults: Array[string];
    LeagueId: string;
    DraftId?: string;
    created_at: string;
    updated_at: string;
}