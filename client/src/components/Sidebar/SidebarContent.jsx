import DropoutItem from "./DropoutItem"


export default function SidebarContent({ type = 'tooltip' }) {
    return (
        <>
            <h3 className='p-1 text-center'>{type}</h3>
            <hr />
            <div 
            className='w-full p-1 rounded text-center hover:bg-gray-700 my-1'
            >
                <DropoutItem type={type} />
            </div>
        </>
    )
}