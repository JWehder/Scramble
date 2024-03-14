export default function Button({ children, type, onClick, size, variant, disabled }) {
    const classes = [
        // Base styles
        'flex justify-center items-center rounded-full focus:outline-none p-2',
        // Size styles (optional)
        size === 'sm' && 'text-sm sm:w-40 md:w-48 lg:w-56 xl:w-64',
        size === 'md' && 'md:text-md text-sm sm:w-12 md:w-14 lg:w-16 xl:w-20',
        size === 'lg' && 'text-lg sm:w-48 md:w-56 lg:w-64 xl:w-80',
        // Variant styles (optional)
        variant === 'primary' && 'bg-middle text-light',
        variant === 'secondary' && 'bg-gray-700 hover:bg-gray-800 text-white',
        // Disabled styles
        disabled && 'opacity-50 cursor-not-allowed',
      ];
    
      return (
        <button type={type} onClick={onClick} className={classes.join(' ')}>
          {children}
        </button>
      );
}