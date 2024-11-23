import {Golfer} from "./golfers"

export interface Team {
    id?: string;  // PyObjectId to string
    TeamName: string;
    ProfilePicture?: string;  // optional string
    Golfers: Golfer[]
    OwnerId?: string;  // PyObjectId to string
    LeagueId: string;  // PyObjectId to string
    Points: number;
    FAAB: number;
    WaiverNumber?: number;
    Placement?: number;
    TeamStats: {
        AvgScore: number;
        MissedCuts: number;
        Top10s: number;
        TotalUnderPar: number;
        Wins: number;
    };
    created_at?: string;  // datetime to string
    updated_at?: string;  // datetime to string
}