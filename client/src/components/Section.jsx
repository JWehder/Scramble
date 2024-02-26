export default function Section({ desc, img, title }) {


    return (
        <div 
        className="flex items-center"
        >
            <img
            src={img}
            alt={`${title} Fantasy Golf`}
            className="w-12 rounded-lg mr-4"
            />
        <div className="flex-grow">
            <h2 className="text-3xl text-left font-lobster mb-2 text-dark">{title}
            </h2>
            <p className="text-left text-gray-700">
                <span>Placeholder content for {desc} section.</span>
            </p>
        </div>
        </div>
    )
}