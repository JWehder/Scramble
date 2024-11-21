import React from 'react';

// TypeScript types for data consistency
type Event = {
    tournamentName: string;
    tournamentLocation: string;
    tournamentPurse: string;
    leagueName: string;
};

type DateWithEvents = {
    date: string; // Format: YYYY-MM-DD
    day: string;
    events: Event[];
};

type EventDateProps = {
    date: DateWithEvents;
};

// Mock data
const dates: DateWithEvents[] = [
    {
        date: "2024-12-04",
        day: "Monday",
        events: [
            {
                tournamentName: "Player's Championship Draft",
                tournamentLocation: "Jacksonville, FL",
                tournamentPurse: "$4,200,000",
                leagueName: "Weber Invitational",
            },
            {
                tournamentName: "Fantasy Golf League Kickoff",
                tournamentLocation: "Orlando, FL",
                tournamentPurse: "$1,500,000",
                leagueName: "Elite Golfers Club",
            },
        ],
    },
    {
        date: "2024-12-06",
        day: "Wednesday",
        events: [
            {
                tournamentName: "Winter Open",
                tournamentLocation: "Miami, FL",
                tournamentPurse: "$3,000,000",
                leagueName: "South Florida League",
            },
        ],
    },
];

// Component to render individual events
const EventItem: React.FC<{ event: Event }> = ({ event }) => (
    <div className="p-2 border-b font-PTSans">
        <h3 className="text-lg font-semibold">{event.tournamentName}</h3>
        <p>{event.tournamentLocation}</p>
        <p>Purse: {event.tournamentPurse}</p>
        <p>League: {event.leagueName}</p>
    </div>
);

// Component to render events on a specific date
const EventDate: React.FC<EventDateProps> = ({ date }) => (
    <div className="p-4 bg-middle rounded-md mb-4 shadow">
        <h2 className="text-xl font-bold mb-2">
            {date.day}, {date.date}
        </h2>
        {date.events.map((event, idx) => (
            <EventItem key={idx} event={event} />
        ))}
    </div>
);

// Main Schedule component
const Schedule: React.FC = () => (
    <div className="w-full rounded-xl overflow-auto p-4 text-light bg-dark">

        {dates.map((date, idx) => (
            <EventDate key={idx} date={date} />
        ))}
    </div>
);

export default Schedule;// TypeScript types for data consistency
