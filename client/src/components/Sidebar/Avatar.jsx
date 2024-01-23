import PropTypes from 'prop-types'
import Tooltip from './Tooltip'

export default function Avatar({ imgUrl, name, borderColor, size }) {
    const borderSize = borderColor === "transparent" ? 0 : 2;

    return (
        <Tooltip tooltip = {name} >
        <div 
            className={`flex items-center justify-center w-${size} rounded-full overflow-hidden hover:cursor-pointer mx-1 ${borderColor} ring-${borderSize}`}>
              <img 
                  alt={name}
                  src={imgUrl} 
                  className={`bg-slate-200 w-${size} h-${size} object-cover`}
              />
        </div>
        </Tooltip>

    )
}

Avatar.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    name: PropTypes.string,
    borderColor: PropTypes.string,
    size: PropTypes.number
}