export default function Modal({ open, children, onClose, title }) {

    if (!open) return null;

    return (
        <>
          {open && (
            <div className="fixed z-50 inset-0 bg-gray-400 bg-opacity-50 backdrop-blur-xs overflow-auto py-4">
              <div className="relative mx-auto max-w-2xl bg-white shadow-lg rounded-xl p-4">
                <div>
                    <h3 className="text-lg font-medium leading-6 text-gray-900 mb-1">
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
                    <hr className="mb-2" />
                </div>
                {children}
              </div>
            </div>
          )}
        </>
    );

}