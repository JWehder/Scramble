import PropTypes from 'prop-types';
import imgUrl from "../assets/i.png"
import imgUrl2 from "../assets/i-1.png"
import Avatar from './Avatar';

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
            <div >
                Team 1 vs Team 2
                <div className='flex'>
                    <Avatar imgUrl={imgUrl} name="Justin Thomas" />
                    <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
                    <Avatar imgUrl={imgUrl2} name="Scottie Scheffler" />
                </div>
            </div>
            </div>
            <div className='text-center'>League 2</div>
        </div>
    )
}

SideBarTooltip.propTypes = {
    title: PropTypes.string.isRequired
}