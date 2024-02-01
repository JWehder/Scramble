import PropTypes from 'prop-types'

export default function Avatar({ imgUrl, name, score = 0, size }) {
    // take in the current score and output either green, gray, or red for 
    // the badge

    let badgeColor;

    if (score > 0) {
        badgeColor = 'bg-red-600';
    } else if (score === 0) {
        badgeColor = 'bg-gray-600';
    } else {
        badgeColor = 'bg-green-600';
    }

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
                <div className={`absolute ${badgeColor} rounded top-0 left-0 opacity-85 p-1 h-5 w-5`}>
                    <span className='text-xs'>{score}</span>
                </div>
            </div>
    )
}

Avatar.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    name: PropTypes.string,
    borderColor: PropTypes.string,
    size: PropTypes.string
}