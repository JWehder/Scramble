export interface Team {
    id?: string;  // PyObjectId to string
    TeamName: string;
    ProfilePicture?: string;  // optional string
    Golfers: Record<string, Record<string, any>>;  // dictionary type with string keys and values of any type
    OwnerId?: string;  // PyObjectId to string
    LeagueId: string;  // PyObjectId to string
    Points: number;
    FAAB: number;
    WaiverNumber?: number;
    created_at?: string;  // datetime to string
    updated_at?: string;  // datetime to string
}