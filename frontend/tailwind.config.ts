import type { Config } from "tailwindcss";

export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#0A84FF",
          deep: "#0057D9",
          cyan: "#25D9FF",
          light: "#EEF7FF",
        },
        ink: "#0F172A",
        muted: "#64748B",
        cardborder: "#D8EAFE",
        ok: "#10B981",
        warn: "#F59E0B",
        danger: "#EF4444",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 4px 20px rgba(10, 132, 255, 0.08)",
      },
    },
  },
};
