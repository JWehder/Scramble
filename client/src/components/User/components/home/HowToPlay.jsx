import friends from "../../../../assets/friends_playing_rounded.png";
import trophy from "../../../../assets/trophy_rounded.png";
import golfer from "../../../../assets/golfer.png";
import Section from "./Section";

export default function HowToPlay() {
    const sections = [
        {
        title: "Create or Join a League",
        img: friends,
        description: "Create a league your way. Or join a public league from our large community of golf fanatics!"
        }, 
        {
        title: "Pick Your Tournaments",
        img: trophy,
        description: "Choose which tournaments your league engages in. Not every player plays in each tournament so it's key to find which tournaments the top players are playing in."
        },
        {
        title: "Draft Players: Every Tournament Week!",
        img: golfer,
        description: "Each week there is a tournament there will be a draft to determine who you will be playing with"
        }, 
        {
        title: "Win!",
        img: golfer,
        description: "Based on your scoring format, at the end of the season crown your winner!"
        }
    ]

    return (
        <div className="min-vh-100 min-content bg-dark"
        >
        {/* Title on left, sections on right */}
            <div className="flex flex-wrap md:flex-row h-full">
                <div className="w-full md:w-1/4 flex items-center justify-center py-8 px-4 md:px-8">
                    <h1 className="text-6xl font-PTSans text-light text-left">
                        How to Play
                    </h1>
                </div>
                <div className="w-full md:w-3/4 flex flex-col items-start justify-center px-4 py-4 md:px-8 md:py-12">
                    <div className="space-y-6">
                    {sections.map((section, idx) => {
                        return (
                            <Section
                            key={`Section${idx}`}
                            desc={section.description}
                            img={section.img}
                            title={section.title}
                            />
                        )
                    })}
                    </div>
                </div>
            </div>
        </div>
    )
}