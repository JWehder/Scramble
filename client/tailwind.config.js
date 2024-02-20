/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        lobster: ['Lobster Two', 'sans-serif'],
      },
      colors: {
        primary: '#202225',
        secondary: '#5865f2'
      }
    }
  },
  plugins: [],
}

