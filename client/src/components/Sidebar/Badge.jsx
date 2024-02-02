export default function Badge({ children, bgColor }) {
    // there needs to be certain configured elements within the parent div to make this work. See -> Player Component

    return (
        <>
            <span 
            className={`${bgColor} text-xs rounded-full top-2 right-[-6px] p-3.5 h-5 w-5 absolute flex justify-center items-center`}
            >
                {children}
            </span>
        </>
    )
}