import type { Config } from "tailwindcss";

// All values below are ported 1:1 from the original Tailwind CDN config
// embedded in index.html (the four static mockup pages). Do not change
// these without checking against the original design — they are the
// source of truth for "do not redesign the UI".
const config: Config = {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "surface-variant": "#d3e4fe",
        "primary-fixed-dim": "#c0c1ff",
        "surface-container-low": "#eff4ff",
        "on-secondary-fixed": "#23005c",
        "surface-container-high": "#dce9ff",
        "outline-variant": "#c7c4d7",
        "secondary-fixed": "#e9ddff",
        surface: "#f8f9ff",
        "on-secondary-fixed-variant": "#5516be",
        "surface-container": "#e5eeff",
        "on-primary-fixed-variant": "#2f2ebe",
        "tertiary-container": "#2170e4",
        primary: "#4648d4",
        "inverse-primary": "#c0c1ff",
        "primary-fixed": "#e1e0ff",
        "surface-container-lowest": "#ffffff",
        "inverse-surface": "#213145",
        outline: "#767586",
        "on-surface-variant": "#464554",
        secondary: "#6b38d4",
        "on-tertiary-fixed-variant": "#004395",
        "on-tertiary-fixed": "#001a42",
        error: "#ba1a1a",
        tertiary: "#0058be",
        "on-tertiary": "#ffffff",
        "tertiary-fixed-dim": "#adc6ff",
        "on-secondary": "#ffffff",
        "on-secondary-container": "#fffbff",
        "on-error": "#ffffff",
        "error-container": "#ffdad6",
        "on-primary-fixed": "#07006c",
        "on-tertiary-container": "#fefcff",
        "tertiary-fixed": "#d8e2ff",
        "secondary-container": "#8455ef",
        "on-error-container": "#93000a",
        "primary-container": "#6063ee",
        "surface-dim": "#cbdbf5",
        "surface-bright": "#f8f9ff",
        "on-primary": "#ffffff",
        "on-background": "#0b1c30",
        background: "#f8f9ff",
        "on-primary-container": "#fffbff",
        "surface-tint": "#494bd6",
        "on-surface": "#0b1c30",
        "secondary-fixed-dim": "#d0bcff",
        "surface-container-highest": "#d3e4fe",
        "inverse-on-surface": "#eaf1ff",

        // ShadCN/Radix component tokens, mapped onto the existing palette
        // so installed ShadCN components (Dialog, Select, etc.) stay on-brand
        // without introducing a second color system.
        border: "#c7c4d7",
        input: "#c7c4d7",
        ring: "#4648d4",
        foreground: "#0b1c30",
        destructive: {
          DEFAULT: "#ba1a1a",
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#eff4ff",
          foreground: "#464554",
        },
        accent: {
          DEFAULT: "#e1e0ff",
          foreground: "#07006c",
        },
        popover: {
          DEFAULT: "#ffffff",
          foreground: "#0b1c30",
        },
        card: {
          DEFAULT: "#ffffff",
          foreground: "#0b1c30",
        },
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem",
        full: "9999px",
      },
      spacing: {
        md: "16px",
        xl: "40px",
        "margin-desktop": "48px",
        lg: "24px",
        "2xl": "64px",
        gutter: "24px",
        "margin-mobile": "16px",
        sm: "8px",
        base: "4px",
        xs: "4px",
      },
      fontFamily: {
        "body-md": ["Inter"],
        "display-xl": ["Inter"],
        "headline-sm": ["Inter"],
        "headline-lg": ["Inter"],
        "body-lg": ["Inter"],
        "display-xl-mobile": ["Inter"],
        "label-md": ["JetBrains Mono"],
        "body-sm": ["Inter"],
      },
      fontSize: {
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "display-xl": [
          "60px",
          { lineHeight: "72px", letterSpacing: "-0.02em", fontWeight: "700" },
        ],
        "headline-sm": ["24px", { lineHeight: "32px", fontWeight: "600" }],
        "headline-lg": [
          "32px",
          { lineHeight: "40px", letterSpacing: "-0.01em", fontWeight: "600" },
        ],
        "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
        "display-xl-mobile": [
          "40px",
          { lineHeight: "48px", letterSpacing: "-0.02em", fontWeight: "700" },
        ],
        "label-md": [
          "12px",
          { lineHeight: "16px", letterSpacing: "0.05em", fontWeight: "500" },
        ],
        "body-sm": ["14px", { lineHeight: "20px", fontWeight: "400" }],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
