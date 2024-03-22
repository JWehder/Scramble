import Event from "./Event";

export default function EventDate({ date }) {
    // dates will have events and present them beneath it

    const presentEvents = date.events.map((event, idx) => {
        if (idx % 2 === 0) {
            return <Event key={date.date} event={event} even />
        } else {
            return <Event key={date.date} event={event} />
        }
    })

    return (
        <div>
            <div className="bg-dark text-lg p-1 text-light font-PTSans">
                {date.day} - {date.date}
            </div>
            {presentEvents}
        </div>
    )
}