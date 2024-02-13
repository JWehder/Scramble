import PropTypes from 'prop-types';

export default function PlayerTooltip({ children, player }) {

    return (
        <div className={'tooltip-container group/avatars'}>
            {player}
            <div className='tooltip group-hover/avatars:scale-100 top-13'>
                {children}
            </div>
        </div>
    )
}

PlayerTooltip.propTypes = {
    children: PropTypes.node.isRequired,
    avatar: PropTypes.node
}