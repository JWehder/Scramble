export default function Eagle({ children }) {
    return (
        <div className="rounded-full border-2 font-bold border-light font-lobster flex flex-col justify-center items-center text-sm text-light h-8 w-8 bg-transparent">
            <div className="rounded-full border-2 font-bold border-light font-lobster flex flex-col justify-center items-center text-sm text-light h-6 w-6 bg-transparent">
                {children}
            </div>
        </div>
    )
}