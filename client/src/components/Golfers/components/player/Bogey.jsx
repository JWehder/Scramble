export default function Bogey({ children, size = "6" }) {
    size = `w-${size} h-${size}`;

    return (
        <div className={`border-2 font-bold border-light font-lobster flex flex-col justify-center items-center text-sm text-light ${size} bg-transparent`}
        >
            {children}
        </div>
    )
}