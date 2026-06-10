import type { ApiEnvelope } from "~/types";

/**
 * Thin wrapper around $fetch that injects the JWT and returns the
 * unified {success, data, message} envelope.
 */
export function useApi() {
  const config = useRuntimeConfig();
  const base = config.public.apiBase as string;

  function authHeader(): Record<string, string> {
    const token = import.meta.client ? localStorage.getItem("alp_token") : null;
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async function api<T>(
    path: string,
    options: Parameters<typeof $fetch>[1] = {},
  ): Promise<ApiEnvelope<T>> {
    return await $fetch<ApiEnvelope<T>>(`${base}${path}`, {
      ...options,
      headers: { ...authHeader(), ...(options.headers || {}) },
    });
  }

  function exportUrl(path: string): string {
    return `${base}${path}`;
  }

  return { api, exportUrl, authHeader };
}
