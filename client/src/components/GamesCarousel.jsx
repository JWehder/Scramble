import { useRef } from 'react';
import golfLinks from '../assets/golf-links.png';

export default function GamesCarousel() {

    const games = [
        {
            gameName: "Stroke Play",
            description: "In this game mode, golfers accumulate points as a team. Your objective to win is having the team with the score furthest below par combined.",
            minNumOfPlayers: 4,
            maxNumOfPlayers: 32,
            img: golfLinks
        },
        {
            gameName: "Best Ball",
            description: "In this game mode, golfers accumulate points as a team. Your objective to win is having the team with the score furthest below par combined.",
            minNumOfPlayers: 4,
            maxNumOfPlayers: 32,
            img: golfLinks
        },
        {
            gameName: "Head to Head",
            description: "In this game mode, golfers accumulate points as a team. Your objective to win is having the team with the score furthest below par combined.",
            minNumOfPlayers: 4,
            maxNumOfPlayers: 32,
            img: golfLinks
        },
    ];

    const scrollContainer = useRef(null);

    const handleBackClick = () => {
        scrollContainer.current.style.scrollBehavior = 'smooth';
        scrollContainer.current.scrollLeft -= 400;
    };

    const handleNextClick = () => {
        scrollContainer.current.style.scrollBehavior = 'smooth';
        scrollContainer.current.scrollLeft += 400;
    };

    const handleArrowClicks = (e) => {
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
            e.preventDefault();
        };
    };

    return (
        <>
            <div 
            className='flex justify-center items-center align-center'>
                <div className='justify-center w-8'>
                    <BackButton handleBackClick={handleBackClick} />
                </div>
                <>
                <div 
                className='flex justify-center items-center mt-3 w-[525px] scrollbar-hide'
                onKeyDown={(e) => handleArrowClicks(e)}
                tabIndex={0}
                >
                    <div 
                    className='flex overflow-x-auto items-center scrollbar-hide'
                    >
                        <div 
                        className='flex flex-nowrap overflow-x-auto overflow-scroll scrollbar-hide w-full h-[350px] align-baseline' 
                        ref={scrollContainer}
                        onWheel={() => handleWheel()}
                        >
                            <div 
                            className='flex items-center justify-center m-auto scrollbar-hide'
                            >
                                
                            </div>
                        </div>
                    </div>
                    {/* handle the click to the next flashcard */}
                    
                </div>
                </>
                <div className='justify-center w-8'>
                    <NextButton handleNextClick={handleNextClick} />
                </div>
            </div>
            <div>
                <input
                value={queryVal}
                ref={inputRef}
                onChange={(e) => handleFlashcardQuery(e.target.value)}
                className='border-none outline-none text-blue-500 text-center mr-1 w-3'
                />
                / {showSaved ? 
                savedFlashcards.length : 
                sets[currentSetPointer].flashcards.length}
            </div>
        </>
    )
}