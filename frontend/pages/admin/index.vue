<script setup lang="ts">
definePageMeta({ layout: "app", middleware: "admin" });
const auth = useAuthStore();

const cards = [
  { title: "Dashboards", text: "Create, edit, and archive dashboards.", to: "/admin/dashboards", admin: false },
  { title: "Categories", text: "Manage dashboard categories.", to: "/admin/categories", admin: false },
  { title: "Users", text: "Manage users and roles.", to: "/admin/users", admin: true },
  { title: "Audit Logs", text: "Review important platform actions.", to: "/admin/audit-logs", admin: true },
];

const visible = computed(() => cards.filter((c) => !c.admin || auth.isAdmin));
</script>

<template>
  <div>
    <PageHeader
      title="Admin panel"
      subtitle="Manage platform content and access."
    />
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <NuxtLink
        v-for="c in visible"
        :key="c.to"
        :to="c.to"
        class="card p-6 hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-ink text-lg">{{ c.title }}</h3>
        <p class="text-sm text-muted mt-1">{{ c.text }}</p>
        <p class="text-sm text-brand-deep font-medium mt-3">Open →</p>
      </NuxtLink>
    </div>
  </div>
</template>
