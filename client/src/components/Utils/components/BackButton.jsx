// eslint-disable-next-line react/prop-types
export default function BackButton({ handleBackClick, size, color }) {
    size = `w-${size} h-${size}`;

    return (
        <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        onClick={handleBackClick} 
        viewBox="0 0 24 24" 
        strokeWidth={1.5} 
        stroke="currentColor" 
        className={`${size} cursor-pointer mx-2 ${color} hover:brightness-125 hover:translate-x-2`}
        >
            <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18" 
            />
        </svg>
    )
}