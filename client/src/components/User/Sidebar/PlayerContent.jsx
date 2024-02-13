
export default function PlayerContent() {

    const currentScore = -2;
    const prevFourHolesScore = -1;

    return (
            <div
            className='hover:visible opacity-75 bg-black text-white p-1 rounded-md absolute top-full mt-2 whitespace-nowrap text-small'
            >
                <div>Hole: 13</div>
                <div>Place: 13th</div>
                <div>Currently: {currentScore}</div>
                <div>Prev. 4 Holes: {prevFourHolesScore}</div>
            </div>    
    )
}