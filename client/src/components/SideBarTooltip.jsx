import PropTypes from 'prop-types';
import imgUrl from "../assets/i.png"

export default function SideBarTooltip({ title }) {
    // receive data from data source

    return (
        <div className='sidebar-tooltip group-hover:scale-100'>
            <h3 className='p-1 text-center'>{title}</h3>
            <hr />
            <div 
            className='w-[100%] p-1 rounded text-center hover:bg-gray-700 my-1'
            >
                League 1
            <div>
                Team 1 vs Team 2
                <img 
                alt="Scottie Scheff" 
                src={imgUrl} 
                className='rounded w-[32px] h-[32px]'
                />
                <img 
                alt="Justin T" 
                src="../assets/i-1.png" 
                className='rounded w-[16px] h-[16px]'
                />
            </div>
            </div>
            <div className='text-center'>League 2</div>
        </div>
    )
}

SideBarTooltip.propTypes = {
    title: PropTypes.string.isRequired
}