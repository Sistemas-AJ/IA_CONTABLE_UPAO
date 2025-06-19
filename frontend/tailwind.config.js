module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        upaoBlue: '#2056C7',
        upaoGold: '#FFC107',
        upaoGray: '#F8F9FA',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};

