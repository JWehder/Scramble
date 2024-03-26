export default function Button({ children, type, onClick, size, variant, disabled }) {
    const classes = [
        // Base styles
        'flex justify-center items-center rounded-full focus:outline-none p-2 mx-2 text-dark',
        // Size styles (optional)
        size === 'sm' && 'text-xs lg:text-sm md:text-xs sm:text-xs sm:w-40 md:w-48 lg:w-56 xl:w-64',
        size === 'md' && 'text-xs lg:text-md md:text-sm sm:text-xs sm:w-24a',
        size === 'spmd' && 'md:text-md text-lg w-min font-lobster text-dark',
        size === 'lg' && 'lg:text-lg md:text-md sm:text-sm text-sm w-36',
        // Variant styles (optional)
        variant === 'primary' && 'bg-middle text-light',
        variant === 'secondary' && 'bg-transparent border-2 border-light hover:border-light text-light hover:bg-middle',
        // Disabled styles
        disabled && 'opacity-50 cursor-not-allowed',
      ];
    
      return (
        <button type={type} onClick={onClick} className={classes.join(' ')}>
          {children}
        </button>
      );
}