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
        dark: '#115e59', // teal 800
        middle: '#a3e635', // lime 400
        light: '#ecfccb' // lime 100
      }
    }
  },
  plugins: [],
}

