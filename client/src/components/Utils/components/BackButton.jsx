// eslint-disable-next-line react/prop-types
export default function BackButton({ handleBackClick }) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" onClick={handleBackClick} viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 cursor-pointer mx-2 stroke-slate-400">
        <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18" />
        </svg>
    )
}