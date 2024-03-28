import Player from "./Player";

export default function Starters() {
    const players = ["Scottie Scheffler", "Justin Thomas", "Xander Schauffle"];

    return (
        <div className='flex my-1 align-center justify-center max-w-max'>
            {
                players.map((player) => {
                    return <Player
                        imgUrl={""}        
                        name={player}
                        size="sm"
                        score={-2}
                    />
                })
            }
        </div>
    )
}