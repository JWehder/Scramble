// eslint-disable-next-line react/prop-types
export default function NextButton({ handleNextClick, size, color }) {
    size = `w-${size} h-${size}`;

    return (
        <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        strokeWidth={1.5} 
        stroke="currentColor" 
        className={`${size} mx-2 cursor-pointer ${color}`}
        onClick={handleNextClick}>
            <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" 
            />
        </svg>
    )
}