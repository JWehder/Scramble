import PropTypes from "prop-types"

export default function GalleryPhoto({ name, imgUrl }) {
    return (
        <div 
        className='flex items-center justify-items-center rounded-md overflow-hidden mx-0.5 h-[75px] w-[80px]'>
              <img 
                  alt={name}
                  src={imgUrl} 
                  className='bg-slate-200 w-full h-full object-cover'
              />
        </div>
    )
}

GalleryPhoto.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    name: PropTypes.string
}
