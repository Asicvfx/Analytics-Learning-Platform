import { defineStore } from "pinia";
import type { User } from "~/types";

const TOKEN_KEY = "alp_token";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
    ready: false,
  }),
  getters: {
    isAuthenticated: (s) => !!s.token,
    roles: (s) => s.user?.roles ?? [],
    isAdmin: (s) => (s.user?.roles ?? []).includes("ADMIN"),
    isAnalyst: (s) => (s.user?.roles ?? []).includes("ANALYST"),
    canManage: (s) =>
      (s.user?.roles ?? []).some((r) => r === "ADMIN" || r === "ANALYST"),
  },
  actions: {
    loadToken() {
      if (import.meta.client) {
        this.token = localStorage.getItem(TOKEN_KEY);
      }
    },
    setToken(token: string | null) {
      this.token = token;
      if (import.meta.client) {
        if (token) localStorage.setItem(TOKEN_KEY, token);
        else localStorage.removeItem(TOKEN_KEY);
      }
    },
    async login(email: string, password: string) {
      const { api } = useApi();
      const res = await api<{ token: string; user: User }>("/auth/login", {
        method: "POST",
        body: { email, password },
      });
      this.setToken(res.data.token);
      this.user = res.data.user;
      return res;
    },
    async fetchMe() {
      if (!this.token) return;
      try {
        const { api } = useApi();
        const res = await api<User>("/auth/me");
        this.user = res.data;
      } catch {
        this.setToken(null);
        this.user = null;
      } finally {
        this.ready = true;
      }
    },
    async logout() {
      try {
        const { api } = useApi();
        await api("/auth/logout", { method: "POST" });
      } catch {
        /* ignore */
      }
      this.setToken(null);
      this.user = null;
      navigateTo("/login");
    },
  },
});
