export default function Modal({ open, children, onClose, title, color, size }) {

    const modalClasses = [
      'overflow-auto relative shadow-lg rounded-xl mx-auto p-4 overflow-auto',
      size === 'sm' && 'max-w-2xl md:max-w-3xl lg:max-w-3xl',
      size === 'md' && 'max-w-3xl md:max-w-4xl lg:max-w-5xl',
      color === 'green' && 'bg-middle',
      color === 'light' && 'bg-light',
      color === 'dark-green' && 'bg-dark'
    ]

    if (!open) return null;

    return (
        <>
          {open && (
            <div className="fixed z-50 inset-0 bg-light bg-opacity-50 backdrop-blur-xs py-4 min-w-[785px] min-h-[1000px] overflow-auto overflow-x-auto">
              <div className={modalClasses.join(' ')}>
                <div>
                    <h3 className="text-lg font-PTSans leading-6 text-middle mb-1 text-center p-1">
                        {title}
                    </h3>

                    <button
                        type="button"
                        className="absolute top-0 right-0 mt-4 mr-4 text-gray-400 hover:text-gray-500 focus:outline-none"
                        onClick={onClose}
                    >
                        <span className="sr-only">Close modal</span>
                        <svg className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                        <path
                            fillRule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10L4.293 5.707a1 1 0 010-1.414z"
                            clipRule="evenodd"
                        />
                        </svg>
                    </button>
                </div>
                {children}
              </div>
            </div>
          )}
        </>
    );
}