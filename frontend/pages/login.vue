<script setup lang="ts">
const auth = useAuthStore();
const route = useRoute();

const email = ref("admin@example.com");
const password = ref("admin123");
const error = ref("");
const loading = ref(false);

const demoAccounts = [
  ["admin@example.com", "admin123", "ADMIN"],
  ["analyst@example.com", "analyst123", "ANALYST"],
  ["manager@example.com", "manager123", "MANAGER"],
  ["employee@example.com", "employee123", "EMPLOYEE"],
];

function fill(e: string, p: string) {
  email.value = e;
  password.value = p;
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    const redirect = (route.query.redirect as string) || "/home";
    await navigateTo(redirect);
  } catch (e: any) {
    error.value = e?.data?.message || "Invalid email or password.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div
    class="min-h-screen grid lg:grid-cols-2 bg-gradient-to-br from-brand-deep
           to-brand-primary"
  >
    <div class="hidden lg:flex flex-col justify-center px-16 text-white">
      <NuxtLink to="/" class="text-2xl font-extrabold mb-6">
        Analytics &amp; Learning Platform
      </NuxtLink>
      <h1 class="text-4xl font-bold leading-tight">
        One internal platform for dashboards, analytics, and learning.
      </h1>
      <p class="mt-4 text-white/85 max-w-md">
        Sign in to browse the dashboard catalog, explore demo business data, and
        learn how to use every report.
      </p>
    </div>

    <div class="flex items-center justify-center p-6">
      <div class="card w-full max-w-md p-8">
        <h2 class="text-2xl font-bold text-ink">Sign in</h2>
        <p class="text-muted text-sm mt-1">Use a demo account to continue.</p>

        <form class="mt-6 space-y-4" @submit.prevent="submit">
          <div>
            <label class="label">Email</label>
            <input v-model="email" type="email" class="input" required />
          </div>
          <div>
            <label class="label">Password</label>
            <input v-model="password" type="password" class="input" required />
          </div>

          <p v-if="error" class="text-sm text-danger">{{ error }}</p>

          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? "Signing in…" : "Login" }}
          </button>
        </form>

        <div class="mt-6">
          <p class="text-xs font-semibold text-muted uppercase mb-2">
            Demo accounts
          </p>
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="acc in demoAccounts"
              :key="acc[0]"
              class="text-left rounded-lg border border-cardborder px-3 py-2
                     hover:bg-brand-light"
              @click="fill(acc[0], acc[1])"
            >
              <p class="text-xs font-semibold text-ink">{{ acc[2] }}</p>
              <p class="text-[11px] text-muted truncate">{{ acc[0] }}</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
