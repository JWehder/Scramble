import PropTypes from 'prop-types'
import Tooltip from './Tooltip'

export default function Avatar({ imgUrl, name, borderColor, size }) {
    const borderSize = borderColor === "transparent" ? 0 : 2;

    const newSize = Number(size) * 4;

    return (
        <Tooltip tooltip={name}>
        <div 
            className={`flex items-center justify-center rounded-full overflow-hidden hover:cursor-pointer mx-1 ${borderColor} ring-${borderSize}`}
            style={{
                width: `${newSize}px`
            }}
            >
              <img 
                  alt={name}
                  src={imgUrl} 
                  className={`bg-slate-200 object-cover`}
                  style={{
                    width: `${newSize}px`,
                    height: `${newSize}px`,
                    borderColor: `${borderColor}`,
                    borderSize: `${borderSize}px`
                  }}
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