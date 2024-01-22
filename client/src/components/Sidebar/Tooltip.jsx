import PropTypes from 'prop-types';


export default function Tooltip({ name }) {
    return (
        <div className=''>
            {name}
        </div>

    )

}

Tooltip.propTypes = {
    name: PropTypes.string.isRequired
}