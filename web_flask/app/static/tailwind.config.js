/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../templates/*.html'],
  theme: {
    extend: {
      colors: {
        lightgray: '#4A4A4A',
        lightblue: '2699eb',
        black: '#000',
        white: '#fff',
        offset: 'D9D9D9'
      },
      screens: {
        'sm': '430px',
        'md': '720px',
        'lg': '960px',
        'xlg': '1280px'
      }
    },
  },
  plugins: [],
}

