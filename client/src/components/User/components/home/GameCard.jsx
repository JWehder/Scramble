import PropTypes from 'prop-types';

export default function GameCard({ game }) {
    return (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-xl overflow-hidden md:max-w-2xl">
            <img className="h-72 w-full object-cover" src={game.img} alt={game.title} />
            <div className="p-6">
                <h2 className="text-2xl font-bold text-gray-800">{game.title}</h2>
                <p className="mt-2 text-gray-600">{game.desc}</p>
            </div>
        </div>
    )
}

GameCard.propTypes = {
    game: PropTypes.object.isRequired
}
