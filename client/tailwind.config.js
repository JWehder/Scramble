/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      zIndex: {
        '100': '100',
      },
      fontFamily: {
        lobster: ['Lobster Two', 'sans-serif'],
        PTSans: ["PT Sans", 'sans-serif']
      },
      backgroundImage: {
        'custom-gradient': 'linear-gradient(to right, #15803d, #86efac, #00ffbb)',
      },
      colors: {
        dark: '#115e59', // teal 800
        middle: '#059669', // emerald 600
        light: '#ecfccb', // lime 100
        mint: '#00ffbb',
        sand: '#F6D7B0'
      }
    }
  },
  plugins: [],
}

