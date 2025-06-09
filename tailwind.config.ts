import type { Config } from 'tailwindcss';
import { kowaiPrimary, kowaiSecondary, kowaiAccent, kowaiBackground, kowaiText, kowaiSuccess, kowaiWarning, kowaiError, kowaiFontBody, kowaiFontHeading, kowaiFontMonospace } from './src/app/theme';

export default {
  content: [
    "./src/**/*.{html,ts,analog}",
  ],
  theme: {
    extend: {
      colors: {
        'kowai-primary': kowaiPrimary,
        'kowai-secondary': kowaiSecondary,
        'kowai-accent': kowaiAccent,
        'kowai-background': kowaiBackground,
        'kowai-text': kowaiText,
        'kowai-success': kowaiSuccess,
        'kowai-warning': kowaiWarning,
        'kowai-error': kowaiError,
        'kowai-surface': '#1E1E1E', // Added surface color
      },
      fontFamily: {
        sans: kowaiFontBody.split(', '), // Assumes kowaiFontBody is a string like "'Roboto', sans-serif"
        heading: kowaiFontHeading.split(', '), // Assumes kowaiFontHeading is a string like "'Orbitron', sans-serif"
        mono: kowaiFontMonospace.split(', '), // Assumes kowaiFontMonospace is a string like "'Fira Code', monospace"
      },
      animation: {
        fadeIn: 'fadeIn 0.5s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
