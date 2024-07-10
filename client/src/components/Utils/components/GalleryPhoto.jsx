import PropTypes from "prop-types"

export default function GalleryPhoto({ caption, imgUrl }) {
    return (
        <div 
        className='flex items-center justify-items-center rounded-md overflow-hidden mx-0.5 h-[75px] w-[80px] py-1'>
              <img 
                  alt={caption}
                  src={imgUrl} 
                  className='bg-slate-200 w-full h-full object-cover rounded-md'
              />
        </div>
    )
}

GalleryPhoto.propTypes = {
    imgUrl: PropTypes.string.isRequired,
    caption: PropTypes.string
}
