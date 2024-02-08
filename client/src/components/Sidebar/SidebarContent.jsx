import DropoutItem from "./DropoutItem"
import PropTypes from 'prop-types';

export default function SidebarContent({ type }) {
    return (
        <>
            <h3 className='p-1 text-center'>{type}</h3>
            <hr />
            <div 
            className='w-full p-1 rounded text-center my-1'
            >
                <DropoutItem type={type} />
            </div>
        </>
    )
}

SidebarContent.propTypes = {
    type: PropTypes.string
}