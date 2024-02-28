export default function Button({ children, handleClick }) {
    return (
        <button
            className="flex justify-center items-center bg-gradient-to-r from-green-700 via-green-400 to-teal-400 hover:bg-gradient-to-l text-light font-bold py-2 px-4 rounded-full focus:outline-none shadow-md font-PTSans md:text-lg text-sm sm:w-40 md:w-48 lg:w-56 xl:w-64"
            type="submit"
            onClick={handleClick}
        >
            {children}
        </button>
    );
}