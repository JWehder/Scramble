import Event from "./Event";
import EventDate from "./EventDate";

export default function Schedule() {
    const dates = [
        {
            date: "12-4-24",
            day: "Monday",
            events: [
                {
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
            ]
        },
        {
            date: "12-4-24",
            day: "Wednesday",
            events: [
                {
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
            ]
        },
        {
            date: "12-4-24",
            day: "Wednesday",
            events: [
                {
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
                {
                    date: 12-4-24,
                    tournamentName: "Player's Championship Draft",
                    tournamentLocation: "Jacksonville, FL",
                    tournamentPurse: "$4,200,000",
                    leagueName: "Weber Invitational"
                },
            ]
        },
    ]

    return (
        <div className="w-1/2 rounded-xl overflow-auto my-2">
            <h1 
            className="text-2xl font-PTSans text-light text-center p-2 bg-middle rounded-t-xl brightness-125"
            >
                Events
            </h1>
            {dates.map((date) => <EventDate date={date} />)}
        </div>
    )
}