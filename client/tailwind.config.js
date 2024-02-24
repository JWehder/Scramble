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
        PTSans: ["PT Sans", 'sans-serif']
      },
      colors: {
        dark: '#115e59',
        middle: '#4ade80',
        light: '#d1fae5'
      }
    }
  },
  plugins: [],
}

