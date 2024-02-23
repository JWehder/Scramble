export default function Button({ children, handleClick }) {

    return (
        <>
            <button
                className="bg-gradient-to-r from-green-700 via-green-400 to-teal-400 hover:bg-gradient-to-l text-white font-bold py-2 px-4 rounded-full focus:outline-none shadow-md"
                type="submit"
                onClick={handleClick}
            >
                {children}
            </button>
        </>

    )
}