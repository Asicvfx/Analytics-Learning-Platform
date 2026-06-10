/** Route guard: redirect unauthenticated users to /login. */
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return;
  const auth = useAuthStore();
  if (!auth.token) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`);
  }
});
