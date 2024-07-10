export default function LoggedOut({ setIsLoggedIn }) {
    return (
        <div>
            <h1 className="text-3xl font-bold underline text-center mt-14">
                Scramble
            </h1>
            <p className="text-l font-bold underline text-center mt-14" onClick={() => setIsLoggedIn(true)}>Log In</p>
        </div>
    )
}