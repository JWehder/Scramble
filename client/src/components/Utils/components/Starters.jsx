import Player from "../../User/components/sidebar/Player";

export default function Starters() {
    const players = ["Scottie Scheffler", "Justin Thomas", "Xander Schauffle"];

    return (
        <div className='flex my-1 align-center justify-center'>
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