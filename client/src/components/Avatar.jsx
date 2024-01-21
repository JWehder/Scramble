import PropTypes from 'prop-types'
import Tooltip from './Tooltip'

export default function Avatar({ imgUrl, name }) {
    return (
        <div 
        className='flex items-center justify-center w-9 rounded-full overflow-hidden hover:cursor-pointer mx-0.5'>
              <img 
                  alt={name}
                  src={imgUrl} 
                  className='bg-slate-200 w-9 h-9 object-cover'
              />
              <Tooltip name = {name} />
        </div>

    )
}

Avatar.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    name: PropTypes.string
}