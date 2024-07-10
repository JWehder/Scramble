import PropTypes from 'prop-types';

export default function Badge({ children, bgColor, size }) {
    // there needs to be certain configured elements within the parent div to make this work. See -> Player Component

    const badgeSize = Number(size) * 4;

    return (
        <>
            <span 
            className={`${bgColor} text-xs rounded-full top-2 right-[-6px] p-3.5 absolute flex justify-center items-center`}
            style={{
                width: `${badgeSize}px`,
                height: `${badgeSize}px`

            }}
            >
                {children}
            </span>
        </>
    )
}

Badge.propTypes = {
    bgColor: PropTypes.string.isRequired,
    children: PropTypes.node.isRequired,
    size: PropTypes.string
}