/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        antokia: {
          red: "#e5322d",
          dark: "#111827",
          light: "#fff5f4"
        }
      },
      boxShadow: {
        soft: "0 10px 40px rgba(15, 23, 42, 0.07)"
      }
    },
  },
  plugins: []
};