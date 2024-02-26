import PropTypes from 'prop-types';

export default function Section({ desc, img, title }) {

    return (
        <div 
        className="flex items-center justify-content"
        >
            <div className="w-3/4">
                <h2 className="text-3xl text-left font-lobster mb-2 text-light">{title}
                </h2>
                <p className="text-left text-light">
                    <span>Placeholder content for {desc} section.</span>
                </p>
            </div>
            <div className="w-1/4">
                <img
                src={img}
                alt={`${title} Fantasy Golf`}
                className="object-cover"
                />
            </div>
        </div>
    )
}

Section.propTypes = {
    desc: PropTypes.string.isRequired,
    img: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired
}