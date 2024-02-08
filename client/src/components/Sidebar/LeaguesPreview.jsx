import League from "./League";

export default function LeaguesPreview() {

    // pull of user's info including their players from state

    // createPlayerAvatars: mapping function for displaying player avatars
    // function createPlayerAvatars() {};

    // if players are playing, they will receive a glowingwrapper

    const userLeagues = ["league 1", "league 2", "league 3"];

    return (
        <>
            {userLeagues ? 
                userLeagues.map((league) => <League league={league} />)
            :
                "Join a league!"
            }
        </>
    )
}