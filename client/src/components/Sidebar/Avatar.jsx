import PropTypes from 'prop-types'
import AvatarTooltip from './PlayerTooltip';

export default function Avatar({ imgUrl, name, size }) {
    // take in the current score and output either green, gray, or red for 
    // the badge

    const newSize = Number(size) * 4;

    return (
            <div 
                className={`flex relative items-center justify-center rounded-full overflow-hidden hover:cursor-pointer mx-1`}
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
                        borderSize: `${newSize}px`
                    }}
                />
            </div>
    )
}

Avatar.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    name: PropTypes.string,
    borderColor: PropTypes.string,
    size: PropTypes.string
}