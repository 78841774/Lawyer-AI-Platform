import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0F172A",
        muted: "#64748B",
        paper: "#F8FAFC",
        line: "#E2E8F0",
        accent: "#1D4ED8",
        gold: "#C9A227",
        navy: "#0B1220",
        surface: "#111827"
      }
    }
  },
  plugins: []
};

export default config;
