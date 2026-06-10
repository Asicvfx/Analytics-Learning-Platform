/** Restore the session from localStorage on app start (client only). */
export default defineNuxtPlugin(async () => {
  const auth = useAuthStore();
  auth.loadToken();
  if (auth.token) {
    await auth.fetchMe();
  } else {
    auth.ready = true;
  }
});
