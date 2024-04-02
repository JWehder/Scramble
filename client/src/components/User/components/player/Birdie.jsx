export default function Birdie({ children }) {
    return (
        <div className="rounded-full border-2 font-bold border-light font-lobster flex justify-center items-center text-sm text-light h-7 w-7 bg-transparent">
            {children}
        </div>
    )
}