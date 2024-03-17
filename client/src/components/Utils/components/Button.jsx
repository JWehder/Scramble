export default function Button({ children, type, onClick, size, variant, disabled }) {
    const classes = [
        // Base styles
        'flex justify-center items-center rounded-full focus:outline-none p-2 mx-2 text-dark',
        // Size styles (optional)
        size === 'sm' && 'text-sm sm:w-40 md:w-48 lg:w-56 xl:w-64',
        size === 'md' && 'md:text-md text-sm w-min',
        size === 'spmd' && 'md:text-md text-lg w-min font-lobster text-dark',
        size === 'lg' && 'text-lg sm:w-48 md:w-56 lg:w-64 xl:w-80',
        // Variant styles (optional)
        variant === 'primary' && 'bg-middle text-light',
        variant === 'secondary' && 'bg-middle border-2 border-middle hover:border-light text-light',
        variant === 'special' && 'text-lg bg-middle text-light relative leading-6 font-lobster',
        // Disabled styles
        disabled && 'opacity-50 cursor-not-allowed',
      ];
    
      return (
        <button type={type} onClick={onClick} className={classes.join(' ')}>
          {children}
        </button>
      );
}