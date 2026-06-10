<script setup lang="ts">
definePageMeta({ layout: "app", middleware: "auth" });
const auth = useAuthStore();
</script>

<template>
  <div>
    <PageHeader title="Settings" subtitle="Your account information." />
    <div class="card p-6 max-w-lg space-y-4">
      <div>
        <p class="label">Full name</p>
        <p class="text-ink">{{ auth.user?.fullName }}</p>
      </div>
      <div>
        <p class="label">Email</p>
        <p class="text-ink">{{ auth.user?.email }}</p>
      </div>
      <div>
        <p class="label">Roles</p>
        <div class="flex gap-2">
          <UiBadge v-for="r in auth.roles" :key="r" tone="blue">{{ r }}</UiBadge>
        </div>
      </div>
      <div>
        <p class="label">Department</p>
        <p class="text-ink">{{ auth.user?.department || "—" }}</p>
      </div>
      <button class="btn-secondary" @click="auth.logout()">Logout</button>
    </div>
  </div>
</template>
