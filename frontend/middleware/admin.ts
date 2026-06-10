/** Route guard: only ADMIN/ANALYST may enter admin pages. */
export default defineNuxtRouteMiddleware(() => {
  if (import.meta.server) return;
  const auth = useAuthStore();
  if (!auth.token) return navigateTo("/login");
  if (!auth.canManage) return navigateTo("/home");
});
