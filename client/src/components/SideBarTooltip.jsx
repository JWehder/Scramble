import PropTypes from 'prop-types';
import DropoutItem from './DropoutItem';
import Message from './Message';

export default function SideBarTooltip({ title }) {
    // receive data from data source

    return (
        <div className='sidebar-tooltip group-hover:scale-100'>
            <h3 className='p-1 text-center'>{title}</h3>
            <hr />
            <div 
            className='w-full p-1 rounded text-center hover:bg-gray-700 my-1'
            >
                League 1
                <DropoutItem />
            </div>
            <Message />
        </div>
    )
}

SideBarTooltip.propTypes = {
    title: PropTypes.string.isRequired
}