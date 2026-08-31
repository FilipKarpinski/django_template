/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan Python too: class strings often live in code (form widget attrs,
  // helper properties). Tailwind does a plain text scan, so literal class
  // names in .py files are picked up, but computed ones are not.
  content: ["./src/**/*.html", "./src/**/*.py"],
  theme: {
    extend: {},
  },
  plugins: [],
};
