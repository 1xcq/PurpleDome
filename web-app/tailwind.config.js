/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js,svelte}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}
