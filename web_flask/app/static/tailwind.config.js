/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../templates/*.html', './js/*.js'],
  theme: {
    extend: {
      colors: {
        lightgray: '#4A4A4A',
        lightblue: '#2699eb',
        black: '#000',
        white: '#fff',
        offwhite: '#f5f5f5',
        mediumpurple: '#16101C',
        offset: '#D9D9D9'
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

