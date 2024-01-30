import PropTypes from 'prop-types';
import DropoutItem from './DropoutItem';

export default function TooltipContent({ title, direction }) {
    // receive data from data source

    return (
        <div className={`tooltip group-hover:scale-100 ${direction}`}>
            <h3 className='p-1 text-center'>{title}</h3>
            <hr />
            <div 
            className='w-full p-1 rounded text-center hover:bg-gray-700 my-1'
            >
                <DropoutItem title={title} />
            </div>
        </div>
    )
}

SideBarTooltip.propTypes = {
    title: PropTypes.string.isRequired,
    direction: PropTypes.string.isRequired
}