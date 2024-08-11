import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ["var(--font-poppins)"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      typography: {
        DEFAULT: {
          css: {
            h1: {
              fontFamily: "Poppins, var(--font-poppins)", // Ensure the correct font is used
              color: "#000",
              fontSize: "32px",
              fontWeight: "700",
              lineHeight: "normal",
            },
            p: {
              fontFamily: "Poppins, var(--font-poppins)", // Ensure the correct font is used
              color: "#000",
              fontSize: "20px",
              fontWeight: "500",
              lineHeight: "normal",
            },
          },
        },
      },
      animation: {
        walk1: "walk1 1s steps(1) infinite",
        walk2: "walk2 1s steps(1) infinite",
      },
      keyframes: {
        walk1: {
          "0%, 49.9%": { opacity: "1" }, // Show image 1
          "50%, 100%": { opacity: "0" }, // Hide image 1
        },
        walk2: {
          "0%, 49.9%": { opacity: "0" }, // Hide image 2
          "50%, 100%": { opacity: "1" }, // Show image 2
        },
      },
      width: {
        "screen-minus-10": "calc(100vw - 40px)", // Adjust 10px to your desired margin
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#fcf8f3",
          secondary: "#ffd3b6",
          accent: "#dca47c",
          neutral: "#698474",
          "base-100": "#ffffff",

          "--rounded-box": "1rem", // border radius rounded-box utility class, used in card and other large boxes
          "--rounded-btn": "0.5rem", // border radius rounded-btn utility class, used in buttons and similar element
          "--rounded-badge": "1.9rem", // border radius rounded-badge utility class, used in badges and similar
          "--animation-btn": "0.25s", // duration of animation when you click on button
          "--animation-input": "0.2s", // duration of animation for inputs like checkbox, toggle, radio, etc
          "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
          "--border-btn": "1px", // border width of buttons
          "--tab-border": "1px", // border width of tabs
          "--tab-radius": "0.5rem", // border radius of tabs
        },
      },
    ],
  },
};

export default config;
