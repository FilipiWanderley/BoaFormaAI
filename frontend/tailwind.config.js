/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Premium dark system
        surface: {
          0: '#080808',   // page background
          1: '#101010',   // sidebar
          2: '#161616',   // card
          3: '#1c1c1c',   // card elevated / inputs
          4: '#242424',   // hover
        },
        border: {
          DEFAULT: 'rgba(255,255,255,0.07)',
          hover:   'rgba(255,255,255,0.12)',
          strong:  'rgba(255,255,255,0.18)',
        },
        text: {
          primary:   '#ffffff',
          secondary: 'rgba(255,255,255,0.5)',
          tertiary:  'rgba(255,255,255,0.28)',
        },
        accent: {
          DEFAULT: '#2563eb',
          hover:   '#3b72f6',
          muted:   'rgba(37,99,235,0.12)',
          border:  'rgba(37,99,235,0.3)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
