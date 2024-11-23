export default function Modal({ open, onClose, bgColor, closeButtonColor, children }) {

    return (
        <div onClick={onClose} className={`
            fixed inset-0 flex justify-center items-center transition-colors
            ${open ? "visible bg-dark/20" : "invisible"}
        `}>
            {/* modal */}
            <div
            onClick={(e) => e.stopPropagation()}
            className={`
            rounded-xl p-6 transition-all ${bgColor}
            ${open ? "scale-100 opacity-100" : "scale-125 opacity-0"}
            `}
            >
                <button
                      type="button"
                      className={`absolute top-2 right-4 p-1 mt-4 mr-4 
                      ${closeButtonColor ? `text-${closeButtonColor} hover: bg-${closeButtonColor}/20`: "text-light hover:bg-light/20"}
                       focus:outline-none hover:bg-light/20 rounded-full h-10 w-10 justify-center items-center flex`}
                      onClick={onClose}
                  >
                      <svg className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                      <path
                          fillRule="evenodd"
                          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10L4.293 5.707a1 1 0 010-1.414z"
                          clipRule="evenodd"
                      />
                      </svg>
                  </button>
                {children}
            </div>

        </div>
    )
}