export default function Button({ children, type, onClick, size, variant, disabled }) {
    const classes = [
        // Base styles
        'flex justify-center items-center rounded-full focus:outline-none p-2 text-dark',
        // Size styles (optional)
        size === 'sm' && 'text-xs lg:text-sm md:text-xs sm:text-xs sm:w-16 md:w-16 lg:w-24 xl:w-32',
        size === 'md' && 'text-xs lg:text-md md:text-sm sm:text-xs sm:w-28',
        size === 'spmd' && 'md:text-md text-lg w-min font-lobster text-dark',
        size === 'lg' && 'lg:text-lg md:text-md sm:text-sm text-sm w-36',
        // Variant styles (optional)
        variant === 'primary' && 'bg-dark text-light py-2 px-4 rounded-md hover:bg-dark/90 shadow-lg',
        variant === 'secondary' && "bg-light text-dark py-2 px-4 rounded-md hover:bg-light/90 shadow-lg",
        // Disabled styles
        disabled && 'opacity-50 cursor-not-allowed',
      ];
    
      return (
        <button type={type} onClick={onClick} className={classes.join(' ')}>
          {children}
        </button>
      );
}